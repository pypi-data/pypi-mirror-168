#!/usr/bin/env python3

import re
import numpy as np
import textwrap
from tinydb import Query
from ase.units import create_units
from ase.db import connect


# physical constants
units = create_units('2014')
kB = units['_k']             # Boltzman's constant [J/K]
Nav = units['_Nav']          # Avogadro's constant [mole/mol]
amu = units['_amu']          # atomic mass unig (1.66e-27) [kg]
hplanck = units['_hplanck']  # Plank's constant (6.63e-34) [J*s]
R = kB*Nav                   # R (gas constant) [J/mol/K]

# unit conversion
eVtokJ = 96.487
eVtoJ = eVtokJ*1.0e3

# database containing informations for adsorbates
# home = os.environ["HOME"]
# lib  = home + "/" + "microkinetic_toolkit"
# MOLECULE_DB = lib + "/" + "molecules.json"


class Reaction:
    """
    Elemetary reaction class.
    """
    class IdIterator(object):
        def __init__(self):
            self.num = 0

        def __next__(self):
            num = self.num
            self.num += 1
            return num

        def reset(self):
            self.num = 0

    id_iterator = IdIterator()

    def __init__(self, reaction_str, reaction_id=None):
        self._reaction_str = reaction_str.lstrip()  # delete spaces
        if reaction_id is None:
            reaction_id = next(self.id_iterator)
        self._reaction_id = reaction_id
        self._parse_reaction_str()

    def _set_Ea_dict(self, Ea_dict: dict):
        self._Ea_dict = Ea_dict

    def _set_molecules_db(self, molecules_db):
        self._molecules_db = molecules_db

    def reverse(self):
        reactants_str, products_str = self._reaction_str.split("->")
        new_r_str = products_str.strip() + " -> " + reactants_str.strip()
        return type(self)(new_r_str)

    def _parse_reaction_str(self):
        reactants_str, products_str = self._reaction_str.split("->")
        self.reactants = self._from_halfside_to_nsp_list(reactants_str)
        self.products = self._from_halfside_to_nsp_list(products_str)

    def _from_halfside_to_nsp_list(self, halfside_str):
        terms = halfside_str.split("+")
        species = [self._change_term_to_coef_and_species(term) for term in terms]

        # Check dupulicate. If same compound is found, increase the coefficient.
        list_species = []
        for spe in species:
            if spe in list_species:
                new = (spe[0]+1, spe[1], spe[2])
                list_species.remove(spe)
                list_species.append(new)
            else:
                list_species.append(spe)

        return list_species

    def _change_term_to_coef_and_species(self, term):
        term = term.strip()

        # coefficient
        re_coef = re.compile("^[0-9]+")
        re_coef_search = re_coef.search(term)

        # site
        re_site = re.compile("_(atop|fcc|hcp|br|surf)")
        re_site_search = re_site.search(term)

        # coef
        if re_coef_search is None:  # has no coefficient
            coef = 1
        else:  # has coefficient
            coef = int(re_coef_search[0])

        # site
        if re_site_search is None:  # has no site -- gas
            site = "gas"
        else:  # has site
            site = re_site_search[1]

        spe = re_site.sub("", re_coef.sub("", term))
        spe = spe.strip()

        # add "_surf" for surface species
        if re_site_search is not None:  # has site
            spe += "_surf"

        return (coef, spe, site)

    def to_dict(self):
        """
        convert to dict.

        Returns:
            base_key (dict)
        """
        def extract_attribute_dict(instance, keys, default=None):
            ddict = {}
            for key in keys:
                val = getattr(instance, key, default)
                ddict[key] = val
            return ddict
        return extract_attribute_dict(self, self.base_keys)

    @classmethod
    def from_dict(cls, ddict):
        reaction_str = ddict["_reaction_str"]
        reaction_id = ddict["_reaction_id"]
        return cls(reaction_str, reaction_id)

    # tinyDB
    def to_tinydb(self, tinydb):
        tinydb.insert(self.to_dict())

    def update_tinydb(self, tinydb):
        ddict = self.to_dict()
        query = Query()
        q_ins = getattr(query, "_reaction_id")
        tinydb.update(ddict, q_ins == ddict["_reaction_id"])

    @property
    def base_keys(self):
        base_keys = ["_reaction_str", "_reaction_id"]
        return base_keys

    @property
    def reactant_species(self):
        """
        Get reactant chemical species.

        Returns:
            reactant species in the list of strings
        """
        lst = []
        for i in self.reactants:
            lst.append(i[1])
        return lst

    @property
    def product_species(self):
        """
        Get product chemical species.

        Returns:
            product species in the list of strings
        """
        lst = []
        for i in self.products:
            lst.append(i[1])
        return lst

    @property
    def unique_species(self):
        """
        Get unique species in an elementary reaction.

        Returns:
            Unique chemical species -- list of strings.
        """
        reac = self.reactant_species
        prod = self.product_species
        return list(set(reac).union(set(prod)))

    def _get_openfoam_react_str(self, direction="forward"):
        str = {"reac": None, "prod": None}
        for side in ["reac", "prod"]:
            from_ = self.reactants if side == "reac" else self.products
            terms = []
            for coef, species, site in from_:
                if species == "surf":
                    species_ = "X(S)"  # to be replaced
                elif "_surf" in species:
                    species_ = species.replace("_surf", "(S)")
                else:
                    species_ = species

                term = species_ if coef == 1 else "{}{}".format(coef, species_)
                terms.append(term)

            str[side] = " + ".join(terms)

        if direction == "forward":
            openfoam_reaction_str = str["reac"] + " = " + str["prod"]
        elif direction == "reverse":
            openfoam_reaction_str = str["prod"] + " = " + str["reac"]
        else:
            raise ValueError("direction should be forward or reverse")

        return openfoam_reaction_str

    def to_openfoam_paramdict(self, deltaE=None, bep_param=None, direction="forward"):
        """
        Get openfoam paramter as dict.

        Args:
            deltaE:
            bep_param:
            direction:
        Returns:
            param_dict:
        """
        param_dict = {}
        param_dict["type"] = "irreversibleSurfaceSiteArrheniusSolidReaction"
        param_dict["reaction"] = self._get_openfoam_react_str(direction=direction)
        param_dict["A"] = self.get_preexponential(direction=direction)
        param_dict["beta"] = 0
        param_dict["Ta"] = self.get_activation_barrier(deltaE=deltaE, bep_param=bep_param,
                                                       direction=direction)*eVtoJ/R  # in [K]
        return param_dict

    def get_openfoam_reaction(self, deltaE=None, bep_param=None, direction="forward"):
        """
        Get openFOAM reaction.

        Args:
            deltaE:
            bep_param:
            direction:
        Returns:
            react_info:
        """
        if direction == "forward":
            num = 2*self._reaction_id
        elif direction == "reverse":
            num = 2*self._reaction_id + 1
            pass
        else:
            raise ValueError("direction should be forward or reverse")

        paramdict = self.to_openfoam_paramdict(deltaE=deltaE, bep_param=bep_param, direction=direction)
        ini = "TestReaction{}\n".format(num)
        ini += "{\n"
        param = "type       {0[type]:s};\n" \
                "reaction   \"{0[reaction]:s}\";\n" \
                "A          {0[A]:.5e};\n" \
                "beta       {0[beta]:.5f};\n" \
                "Ta         {0[Ta]:.3f};\n"
        param = param.format(paramdict)
        param = textwrap.indent(param, prefix="    ")
        fin = "}\n"

        react_info = ini + param + fin
        return react_info

    def get_atoms_from_adsorbate(self, specie, site, surface=None):
        """
        Returns Atoms(X) from X_site string.

        Args:
            specie:
            site:
            surface:
        Returns:
            Atoms
        """
        # MOLECULE_DB is global variables.
        # db = connect(MOLECULE_DB)
        db = connect(self._molecules_db)

        if site == "gas":
            if specie == "surf":
                return surface  # already atoms
            else:
                return db.get_atoms(name=specie)
        else:
            spe = specie.split("_")[0]
            return db.get_atoms(name=spe)

    def get_reaction_energy(self, surface=None, calculator=None, ase_db=None, rxn_num=0):
        """
        Calculate reaction energy for an elementary reaction.

        Args:
            surface: Atoms
            calculator: currently Vasp or EMT
            ase_db: ASE database file for existing calculation.
            rxn_num: i-th elementary reaction. Just for printing POSCAR
        Returns:
            deltaE [eV] (float)
        """
        from ase.calculators.emt import EMT

        def search_energy_from_ase_db(atom, ase_db):
            db = connect(ase_db)
            formula = atom.get_chemical_formula()
            try:
                energy = db.get(name=formula).data.energy
            except KeyError:
                print("{0:} is not found in {1:}.".format(formula, db))
                energy = 0.0

            return energy

        def adsorb_on_surface(ads=None, site=None, surface=None, height=1.8):
            """
            Adsorb molecule on surface.

            Args:
                ads:
                site:
                surface:
                height:
            Returns:
                atoms
            """
            from ase.build import add_adsorbate
            from ase.visualize.plot import plot_atoms
            from ase.io import write
            # from .preparation.rot_control import make_atoms_with_standard_alignment
            import matplotlib.pyplot as plt

            surf_copy = surface.copy()
            bare_surf = surface.copy()
            surf_copy.calc = surface.calc

            # adjust height
            shift = min(ads.positions[:, 2])
            ads.translate([0, 0, -shift])

            # TODO: rotate atom
            # ads = make_atoms_with_standard_alignment(ads)
            if site == "atop":
                offset = (0, 0)
                height = 1.8
            elif site == "fcc":
                offset = (0.45, 0.45)
                height = 1.2
            elif site == "hcp":
                offset = (0.23, 0.23)
                height = 1.2

            add_adsorbate(surf_copy, ads, offset=offset, position=(0, 0), height=height)
            surf_copy.pbc = True

            poscar = True
            snapshot = False

            if snapshot:
                fig, ax = plt.subplots()
                plot_atoms(surf_copy)
                ax.set_axis_off()
                fig.savefig(surf_copy.get_chemical_formula() + ".png")
                plt.close()
            if poscar:
                filename = "rxn" + str(rxn_num) + "_" + bare_surf.get_chemical_formula() \
                                                + "_" + ads.get_chemical_formula() + "_POSCAR"
                write(filename, surf_copy)

            return surf_copy

        def optimize_geometry(atoms):
            import ase.optimize

            atoms_copy = atoms.copy()
            atoms_copy.calc = atoms.calc
            opt = ase.optimize.bfgs.BFGS(atoms_copy, maxstep=0.1)
            opt.run(steps=30)

            return atoms_copy

        # main
        # set calculator
        if calculator == "vasp":
            # TODO: do vasp setting
            pass
        elif calculator == "emt":
            calc = EMT()
        else:
            raise Exception("use vasp or emt for calculator")

        energy_dict = {"reactants": 0.0, "products": 0.0}
        for side in ["reactants", "products"]:
            sequence = self.reactants if side == "reactants" else self.products
            for i in sequence:
                _, mol, site = i
                atoms = self.get_atoms_from_adsorbate(mol, site, surface=surface)

                if site != "gas":
                    atoms = adsorb_on_surface(ads=atoms, site=site, surface=surface, height=1.8)

                # look up ase database
                if ase_db is not None:
                    energy = search_energy_from_ase_db(atoms, ase_db)
                else:
                    atoms.set_calculator(calc)
                    atoms = optimize_geometry(atoms)
                    energy = atoms.get_potential_energy()

                energy_dict[side] += energy

        deltaE = energy_dict["products"] - energy_dict["reactants"]

        return deltaE

    def get_entropy_difference(self, x_dict=None):
        """
        Calculate entropy difference (deltaS) along the reaction.
        Moleclar entropy should be prepared beforehand.

        Args:
            x_dict: molar fraction dict [-]

        Returns:
            deltaS [eV/K] (float)
        """
        db = connect(self._molecules_db)

        entropies = {"reactants": 0.0, "products": 0.0}
        warn_list = []
        for side in ["reactants", "products"]:
            sequence = getattr(self, side)
            for mol in sequence:
                coef, spe, site = mol

                if site != "gas" or spe == "surf":
                    # surface species
                    entropy = 0.0
                else:
                    # gas species
                    try:
                        atoms = db.get(name=spe)
                        entropy = atoms.key_value_pairs["molecular_entropy"]  # [eV/K]
                    except KeyError:
                        warn = "{}\n".format(spe)
                        warn = warn + "set default entropy 1.0e-3 meV/K"
                        warn_list.append(warn)
                        entropy = 1.0e-3  # rough entropy estimation ... 1 meV/K

                    # partial pressure correction
                    x_sum = sum(x_dict.values())  # normalize x, just in case
                    if spe in x_dict.keys():
                        correction  = -1.0*R*x_dict[spe]*np.log(x_dict[spe]/x_sum)  # [J/mol/K]
                        correction /= eVtoJ  # [J/mol/K] --> [eV/K]
                        entropy += correction

                entropies[side] += coef*entropy

        deltaS = entropies["products"] - entropies["reactants"]
        if len(warn_list) != 0:
            print("\n=== molecular entropy not found ===")
            for line in warn_list:
                print(line)
            print("===================================")

        return deltaS

    def get_coefficient_of_species(self, species=None):
        """
        Get coefficient of species.

        Args:
            species:

        Returns:
            coef: coefficient
        """
        coef = 0.0
        for side in ["reactants", "products"]:
            sequence = getattr(self, side)
            for mol in sequence:
                coef_, spe, site = mol
                if species == spe:
                    # found
                    if side == "reactants":
                        coef = -coef_
                    else:
                        coef = coef_
                    break
            else:
                # getting out from nested for-loop by break
                continue

        return coef

    def get_nu(self, species="CH3_surf"):
        """
        Get difference in stoichiometric coefficients of reactants and products.
        Nu is defined as sto_coef[product_side] - sto_coef[reactant_side] (C(3.3)).

        Returns:
            nu (list, 0...gas-phase species, 1...surface species)
        """
        coefs  = {"reactants": 0.0, "products": 0.0}
        for side in ["reactants", "products"]:
            mols = getattr(self, side)
            for mol in mols:
                coef, spe, site = mol
                if spe == species:
                    coefs[side] += coef

        nu = coefs["products"] - coefs["reactants"]
        return nu

    def get_deltaV(self):
        """
        Get difference in the gas-phase volume of reactants and products.
        The value has contribution on deltaG as P*deltaV*nu(gas).

        Returns:
            deltaV (float) [m^3/mol]
        """
        # db = connect(MOLECULE_DB)
        db = connect(self._molecules_db)

        V = {"reactants": 0.0, "products": 0.0}
        warn_list = []
        for side in ["reactants", "products"]:
            sequence = getattr(self, side)
            for mol in sequence:
                coef, spe, site = mol

                if site != "gas" or spe == "surf":
                    # surface species
                    volume = 0.0
                else:
                    try:
                        atoms  = db.get(name=spe)
                        volume = atoms.key_value_pairs["molecular_volume"]  # Angstrom^3
                        volume = volume*1.0e-30*Nav  # Angstrom^3 --> m^3/mol
                    except KeyError:
                        warn = "{}\n".format(spe)
                        warn = warn + "set default volume 100 Angstrom^3"
                        warn_list.append(warn)
                        volume = 100.0  # rough volume estimation ... 100 Angstrom^3
                        volume = volume*1.0e-30*Nav  # Angstrom^3 --> m^3/mol

                V[side] += coef*volume

        deltaV = V["products"] - V["reactants"]
        if len(warn_list) != 0:
            print("\n=== molecular volume not found ===")
            for line in warn_list:
                print(line)
            print("==================================")
        return deltaV

    def get_activation_barrier(self, deltaE=None, bep_param: dict = None, direction="forward"):
        """
        Calculate activation barrier (Ea) from reaction energy (deltaE).

        Args:
            deltaE: reaction energy [eV]
            bep_param: BEP alpha and beta (for eV unit)
            direction: forward or reverse
        Returns:
            Ea: activation barrier [eV]
        """
        rxn_type = self.get_reaction_type()

        if rxn_type == "surface_rxn":
            if direction == "forward":
                Ea = bep_param["alpha"]*deltaE + bep_param["beta"]
            elif direction == "reverse":
                Ea = bep_param["alpha"]*deltaE + bep_param["beta"] + deltaE
            else:
                raise ValueError("direction should be forward or reverse")
        else:
            # gas-rxn, adsorption, desorption
            Ea = max(deltaE, 0.0)

        Ea = max(Ea, 0.0)  # avoid negative value

        return Ea

    def get_rate_coefficient(self, deltaE=None, T=300.0, bep_param: dict = None, sden=1e-5, reaction_id=None):
        """
        Calculate rate coefficient from reaction energy (deltaE).

        Args:
            deltaE: reaction energy [eV]
            T: temperature [K]
            bep_param: BEP alpha and beta (for eV unit)
            sden: site density [mol/m^2]
            reaction_id: specify when overwriting Ea
        Returns:
            rate coefficient
        """
        # calculate Ea from deltaE
        if hasattr(self, "_Ea_dict"):
            num_str = str(reaction_id)
            if num_str in self._Ea_dict:
                Ea = self._Ea_dict[num_str]
                print("Ea[{}] is overwritten.".format(num_str))
            else:
                Ea = self.get_activation_barrier(deltaE=deltaE, bep_param=bep_param)
        else:
            Ea = self.get_activation_barrier(deltaE=deltaE, bep_param=bep_param)

        self.Ea_eV = Ea

        Ea *= eVtoJ

        A = self.get_preexponential(T=T, sden=sden)
        exp = np.exp(-Ea/R/T)
        rateconst = A*exp

        return rateconst

    def get_preexponential(self, T=300.0, sden=1.0e-5, direction="forward"):
        """
        Calculate pre-exponential factor.
        Note on revserse reaction:
        Pre-exponential factor for reverse reaction is generally not needed
        since reverse pre-exponential is calculated from forward one and equilibrium constant.
        Reverse pre-exponential is only used for openFOAM purpose.

        Args:
            T: temperature [K]
            sden: site density [mol/m^2]
            direction: forward or reverse
        Returns:
            A: pre-exponential factor (float)
        """
        rad_all = 0
        d_ave   = 0
        s_fac = 1.0  # structural factor
        stick = 1.0e0  # sticking coefficient

        rxn_type = self.get_reaction_type()

        if rxn_type == "surface-rxn" or rxn_type == "desorption":
            # Langmuir-Hinshelwood reaction or desorption --- apply Eyring's transition state theory

            A = kB*T/hplanck/sden  # [J/K*K]*[J/s]^-1*[mol/m^2] = [s]*[mol/m^2] = [mol/m^2/s]
        else:
            # calculate mean diameter
            mass_sum  = 0
            mass_prod = 1

            if direction == "forward":
                target = self.reactants
            elif direction == "reverse":
                target = self.products
            else:
                raise ValueError("direction should be forward or reverse")

            for mol in target:
                coef, spe, site = mol

                if spe == "surf":
                    # bare surface
                    sigma = coef  # site occupation number
                else:
                    # molecular radius (in Angstrom) calculated from volume
                    vol = 100.0  # TODO: molecule volume in Angstrom**3
                    rad = 3.0/(4.0*np.pi)*np.cbrt(vol)
                    rad *= 1.0e-10  # Angstrom --> m

                    nmol = len(target)
                    if nmol == 1 and coef != 1:  # reacion among same species
                        rad_all = coef*rad
                        nmol = coef
                    else:
                        rad_all += rad

                    d_ave += 2*(rad_all/nmol)  # mean diameter

                    spe_atom = self.get_atoms_from_adsorbate(spe, site)
                    if spe_atom is None:
                        pass  # bare surface
                    else:
                        mass = sum(spe_atom.get_masses())

                    mass_sum  += mass*coef
                    mass_prod *= mass**coef

            if rxn_type == "gas-rxn":
                red_mass = mass_prod/mass_sum
                red_mass *= amu

                # Collision theory -- C(3.22)
                A  = Nav*d_ave**2*np.sqrt(8.0*np.pi*kB*T/red_mass)
                A *= s_fac

            elif rxn_type == "adsorption":
                mass *= amu  # should be single molecule [amu -> kg]

                # Hertz-Knudsen (in concentration form) -- C(4.14)
                A = sigma*np.sqrt(kB*T/(2.0*np.pi*mass))
                # ([J/K*K][kg]^-1)^1/2 = [J/kg]^1/2 = [kg*m^2*s^-2/kg]^1/2 = [m/s]

                # multiplying sticking probability and site density: [m/s] --> [m^3/mol/s]
                A *= (stick/sden)

        return A

    def get_reaction_type(self):
        """
        Get reaction type of Reaction.

        Returns:
            rxn_type: string(gas-rxn, surface-rxn, adsorption, or desorption)
        """
        spe_types = {"reactants": [], "products": []}

        for side in ["reactants", "products"]:
            mols = self.reactants if side == "reactants" else self.products

            for mol in mols:
                coef, spe, site = mol

                if spe == "surf":
                    # bare surface
                    spe_types[side].append("surf")
                else:
                    # gas-phase species or surface adsorbates
                    if site == "gas":
                        spe_types[side].append("gas")
                    else:
                        spe_types[side].append("surf")

        if all(spe_type == "gas" for spe_type in spe_types["reactants"]+spe_types["products"]):
            # gas reaction --- collision theory expression
            rxn_type = "gas-rxn"
        elif all(spe_type == "surf" for spe_type in spe_types["reactants"]+spe_types["products"]):
            # Langmuir-Hinshelwood reaction or desorption
            rxn_type = "surface-rxn"
        else:
            if any(spe_type == "gas" for spe_type in spe_types["reactants"]):
                # adsorption (or Eley-Rideal reaction)
                rxn_type = "adsorption"
            elif any(spe_type == "gas" for spe_type in spe_types["products"]):
                # desorption
                rxn_type = "desorption"

        return rxn_type
