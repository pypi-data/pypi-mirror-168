#!/usr/bin/env python3

from .reaction import Reaction
from tinydb import TinyDB
import copy
import os
import numpy as np
import pandas as pd
import pickle
from pandas import DataFrame
from scipy.integrate import ode
from scipy.integrate import solve_ivp
from abc import abstractmethod, ABCMeta
import h5py
import matplotlib.pyplot as plt
import seaborn
import warnings
import json
from typing import List
from .visualization.colors import gene_20color_4lstyle

R = 8.314 * 1.0e-3  # gas constant [kJ/mol/K]
eVtokJ = 96.487
LOAD_DELTA_G = False
Ncstr = 1
tiny = 1.0e-20  # tiny number


def get_obj_from_script(pyscript: str, obname: str) -> object:
    with open(pyscript, "r") as read:
        content = read.read()
    object_dict = {}
    exec(content, object_dict)
    obj = object_dict[obname]
    return obj


class ReactionsBase(metaclass=ABCMeta):
    """
    Set of elementary reactions.
    This is a metaclass, and modules
    other than get_reaction_energy is defined here.
    """
    def __init__(self, reaction_list: list):
        self.reaction_list = reaction_list
        self._ase_db = None
        self._calculator = None
        self._surface = None
        self._bep_param = None
        self._deltaGs = None
        self._TdeltaSs = None
        self._sden = None
        self._v0 = None
        self._wcat = None
        self._area = None
        self._phi = None
        self._rho_b = None
        self._Vr = None
        self._tau = None
        self._Ea_dict = None
        self._ode_solver = "LSODA"
        self._ode_rtol = 1.0e-3
        self._ode_atol = 1.0e-6
        self._ncstr = None
        self._total_tau = None
        self._sens_matrix = None
        self._conversion_info = None
        self._gas_flow_info = None
        self._reduced_discarded_rxns_info = None
        self._reduced_rxns_info = None

    def set_Ncstr(self, ncstr: int = None):
        self._ncstr = ncstr

    @property
    def Ncstr(self) -> int:
        if self._ncstr is None:
            # default Ncstr is global variable.
            return Ncstr
        else:
            return self._ncstr

    @property
    def reaction_symbols(self) -> List[str]:
        reactions_symbols = []
        for reaction in self.reaction_list:
            reactions_symbols.append(reaction._reaction_str)
        return reactions_symbols

    def set_Ea_json(self, Ea_dict_fp: str):
        assert os.path.exists(Ea_dict_fp)
        assert "json" in Ea_dict_fp
        with open(Ea_dict_fp, "r") as read:
            Ea_dict = json.load(read)
        self._Ea_dict = Ea_dict

        for reaction in self.reaction_list:
            assert isinstance(reaction, Reaction)
            reaction._set_Ea_dict(self._Ea_dict)

    def set_molecules_db(self, molecules_db: str = None):
        if molecules_db is None:
            m_kintic_dpath = os.path.dirname(__file__)
            molecules_db = os.path.join(m_kintic_dpath, "data", "molecules.json")
            print("using default molecules.json in microkinetic_tool")
        if not os.path.exists(molecules_db):
            raise ValueError("molecules db {} not exist".format(molecules_db))
        if "json" not in molecules_db and ".db" not in molecules_db:
            raise ValueError("use json file for molecules db")

        for reaction in self.reaction_list:
            assert isinstance(reaction, Reaction)
            reaction._set_molecules_db(molecules_db)

    def __getitem__(self, index):
        return self.reaction_list[index]

    def __len__(self):
        return len(self.reaction_list)

    @property
    def calculator(self):
        return self._calculator

    @calculator.setter
    def calculator(self, calculator_str: str):
        self._calculator = calculator_str

    @property
    def ase_db(self):
        return self._ase_db

    @ase_db.setter
    def ase_db(self, db_file: str):
        self._ase_db = db_file

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, surface):
        # shift
        zmin = np.min(surface.positions[:, 2])
        surface.translate([0, 0, -zmin + 0.1])

        # sort
        surface = self.sort_atoms_by_z(surface)
        self._surface = surface

    def set_ode_solver(self, ode_solver: str):
        solver_list = ["Radau", "LSODA", "RK45", "RK23", "DOP853", "BDF"]
        if ode_solver not in solver_list:
            emes = "available options: {}".format(solver_list)
            raise AssertionError(emes)
        else:
            print("ode solver {} is selected".format(ode_solver))
        self._ode_solver = ode_solver

    def set_ode_solver_threshold(self, rtol: float = 1.0e-3, atol: float = None):
        """
        In default setting, rtol = 1.0e-3, atol = rtol*1.0-6,
        which are default for scipy.
        """
        self._ode_rtol = rtol
        if atol is not None:
            self._ode_atol = atol
            warnings.warn("atol < rtol * abs(y) are constantly expcted.")
        else:
            warnings.warn("atol = rtol * 1.0e-3 is set automatically.")
            self._ode_atol = rtol * 1.0e-3

    def set_kinetic_parameters(self, bep_param=None, sden=1.0e-5, v0=1.0e-5, wcat=1.0e-3,
                               area=1.0e-3, phi=0.5, rho_b=1.0e3, tau: float = None):
        """
        Set various parameters.

        Args:
            bep_param: BEP alpha and beta (dict)
            sden: side density [mol/m^2]
            v0: volumetric flowrate [m^3/sec]. 1 [m^2/sec] = 1.0e6 [mL/sec] = 6.0e7 [mL/min]
            wcat: catalyst weight [kg]
            area: surface area [m^2/kg]
            phi: porosity
            rho_b: density of catalyst [kg/m^3]. typical is 1.0 g/cm^3 = 1.0*10^3 kg/m^3
            tau: residence time [sec]
        Returns:
            None:
        """
        if bep_param is None:
            self._bep_param = {"alpha", 1.0, "beta", 1.0}
        else:
            self._bep_param = bep_param

        self._sden = sden
        self._v0 = v0
        self._wcat = wcat
        self._area = area
        self._phi = phi
        self._rho_b = rho_b
        self._Vr = (wcat/rho_b)*(1-phi)  # reactor volume [m^3], calculated from w_cat.
        # self._Vr  = 0.01e-6  # [m^3]

        if tau is None:
            self._tau = self._Vr/self._v0
        else:
            self._tau = tau

        self._total_tau = self._tau
        self._tau = self._tau/self.Ncstr

        return None

    def to_tdb(self, db_file: str, update=False):
        tdb = TinyDB(db_file)
        for reaction in self.reaction_list:
            if update:
                reaction.update_tdb(tdb)
            else:
                reaction.to_tdb(tdb)
        return None

    def get_unique_species(self):
        """
        Get the list of chemical species, covering all elementary reactions.

        Returns:
            list of string
        """
        species = set([])
        for reaction in self.reaction_list:
            species.update(reaction.unique_species)
        species = list(species)
        species = sorted(species)

        # gas species list then surface species list
        gas  = list(filter(lambda x: "surf" not in x, species))
        surf = list(filter(lambda x: "surf" in x, species))
        species = sum([gas, surf], [])  # flatten

        # move "surf" to last
        if "surf" in species:
            species.remove("surf")
            species.append("surf")

        return species

    def get_index_of_species(self, some_species=None):
        """
        Get index of species.

        Args:
            some_species: string
        Returns:
            species_index: int
        """
        species = self.get_unique_species()
        species_index = species.index(some_species)
        return species_index

    # csv
    def _generate_reactions_dict(self):
        for reaction in self.reaction_list:
            ddict = reaction.to_dict()
            yield ddict

    def to_csv(self, file: str):
        """
        Generate csv file containing elemtary reactions.

        Args:
            file: csv file name
        """
        df = DataFrame(self._generate_reactions_dict())
        df.to_csv(file)

    @classmethod
    def from_csv(cls, csv_file: str):
        """
        Read elementary reactions from CSV.

        Args:
            csv_file: CSV file with elementary reactions
        Returns:
            Reactions
        """
        df = pd.read_csv(csv_file, index_col=0)
        reaction_list = []
        for i, row in df.iterrows():
            ddict = row.to_dict()
            reaction = Reaction.from_dict(ddict)
            reaction_list.append(reaction)
        Reaction.id_iterator.reset()
        return cls(reaction_list)

    # end csv

    def freeze_surface(self):
        """
        Freeze surface.

        Returns:
            surface: ASE Atoms
        """
        def set_tags(surface):
            tags = surface.get_tags()
            surface_copy = copy.deepcopy(surface)
            maxval = max(tags)
            newtags = list(map(lambda x: 0 if x > maxval//2 else 1, tags))
            newtags = np.array(newtags)
            surface_copy.set_tags(newtags)
            return surface_copy

        import ase.constraints
        surface = copy.deepcopy(self._surface)
        surface = set_tags(surface)
        c = ase.constraints.FixAtoms(indices=[atom.index for atom in surface if atom.tag == 0])
        surface.set_constraint(c)
        return surface

    def get_nus(self):
        """
        Get nus, the stoichiometric coefficient matrix: nus[k(species), i(rxn)].
        Each element is defined as the difference of product and reactant sides.

        Returns:
            nus: [2-dim numpy array]
        """
        rxn_num = len(self.reaction_list)
        spe_num = len(self.get_unique_species())
        nus = np.zeros((spe_num, rxn_num))

        species = self.get_unique_species()
        for i, reaction in enumerate(self.reaction_list):
            for spe in species:
                spe_idx = self.get_index_of_species(spe)
                nus[spe_idx][i] = reaction.get_nu(species=spe)

        return nus

    def get_deltaVs(self):
        """
        Calculate the difference in the molecular volume.

        Returns:
            deltaVs: numpy array
        """
        deltaVs = np.zeros(len(self.reaction_list))
        for i, reaction in enumerate(self.reaction_list):
            deltaVs[i] = reaction.get_deltaV()
        return deltaVs

    def get_rate_coefficients(self, deltaEs=None, T=300.0):
        """
        Calculate rate coefficient for all the elementary reactions.

        Args:
            deltaEs: reaction energies [eV]
            T: temperature [K]
        Returns:
            kfor: forward rate coefficients (numpy array)
        """
        kfor = np.zeros(len(self.reaction_list))
        for i, reaction in enumerate(self.reaction_list):
            deltaE = deltaEs[i]
            kfor[i] = reaction.get_rate_coefficient(deltaE, T, bep_param=self._bep_param,
                                                    sden=self._sden, reaction_id=i)

        return kfor

    def do_microkinetics(self, deltaEs=None, kfor=None, T=300.0, P=1.0, p_ratio=None, verbose: bool = False,
                         plot: bool = True):
        """
        Do microkinetic analysis.

        Args:
            deltaEs: reaction energies.
            kfor: rate coefficients in forward direction.
            T: temperature [K]
            P: total pressure [bar]
            p_ratio: partial pressure ratio of inlet (dict) [-]
            verbose:
            plot:
        Returns:
            OdeResult
        """
        if kfor is None:
            raise ValueError("rate coefficient not found")
        
        cudir = os.getcwd()
        odefile = os.path.join(cudir, "tmpode.py")
        self.make_rate_equation(odefile=odefile)
        t, C = self.solve_rate_equation(odefile=odefile, deltaEs=deltaEs, kfor=kfor, T=T, P=P,
                                        p_ratio=p_ratio, verbose=verbose, plot=plot)
        return t, C

    def make_rate_equation(self, odefile=None):
        """
        Make rate equation file

        Args:
            odefile: filename to write ODE equations.
        """
        if odefile is None:
            raise ValueError("ODE file not found")

        # r_ads and p_ads are species list of ALL the elementary reactions.
        # e.g. if inputfile contains
        #  (1) A1 + B1 --> C1 + D1
        #  (2) A2 + B2 --> C2 + D2
        # it gives
        # r_ads = [ [['A1'],['B1']] , [['A2'],['B2']] ]
        # p_ads = [ [['C1'],['D1']] , [['C2'],['D2']] ]

        curdp = os.getcwd()
        fout = open(os.path.join(curdp, odefile), "w")

        fout.write('import numpy as np\n')
        fout.write("\n")
        fout.write('def rate_eqn(t, C, C0, kfor, Kc, sden, area, Vr, tau, ngas, ncomp):\n')
        fout.write("\n")

        # template - start
        # theta [-]*sdens [mol/m^2] --> [mol/m^2]
        lines = [
            "\tkrev = kfor / Kc\n",
            "\ttheta = C.copy()\n",
            "\ttheta[0:ngas] = 0\n",
            "\ttheta *= sden\n",
        ]
        fout.writelines(lines)
        # template - end

        ncomp = len(self.get_unique_species())
        fout.write("\trate = np.zeros(" + str(ncomp) + ")\n\n")

        dict1 = {}
        dict2 = {}

        for irxn, reaction in enumerate(self.reaction_list):
            # hash-tag based reactant and product species list
            # FOR THIS REACTION
            list_r = []
            list_p = []

            # making dict1, a dictionary with hash of species-number
            # and molecule
            for side in ["reactant", "product"]:
                if side == "reactant":
                    terms = reaction.reactants
                    list = list_r
                elif side == "product":
                    terms = reaction.products
                    list = list_p
                else:
                    raise ValueError("asdf")

                for term in terms:
                    spe, site = term[1], term[2]
                    spe_idx = self.get_index_of_species(spe)
                    list.append(spe_idx)
                    dict1[spe_idx] = spe
            # done for dict1

            # making dict2
            for side in ["reactant", "product"]:
                for direction in ["forward", "reverse"]:
                    if side == "reactant" and direction == "forward":
                        mol_list1 = reaction.reactants
                        current_list = list_r
                        # list corresponding to current_list
                        mol_list2 = reaction.reactants
                        coefs = [i[0] for i in mol_list2]
                        term = "kfor[" + str(irxn) + "]"
                        sign = " - "
                    elif side == "reactant" and direction == "reverse":
                        mol_list1 = reaction.products
                        current_list = list_r
                        mol_list2 = reaction.reactants
                        coefs = [i[0] for i in mol_list2]
                        term = "krev[" + str(irxn) + "]"
                        sign = " + "
                    elif side == "product" and direction == "forward":
                        mol_list1 = reaction.reactants
                        current_list = list_p
                        mol_list2 = reaction.products
                        coefs = [i[0] for i in mol_list2]
                        term = "kfor[" + str(irxn) + "]"
                        sign = " + "
                    elif side == "product" and direction == "reverse":
                        mol_list1 = reaction.products
                        current_list = list_p
                        mol_list2 = reaction.products
                        coefs = [i[0] for i in mol_list2]
                        term = "krev[" + str(irxn) + "]"
                        sign = " - "

                    # making single term
                    for mol in mol_list1:
                        coef, spe, site = mol[0], mol[1], mol[2]
                        spe_idx = self.get_unique_species().index(spe)

                        if site == "gas" and spe != "surf":
                            # gas-phase molecule
                            theta = "C[" + str(spe_idx) + "]"
                        else:
                            # adsorbed species or bare surface
                            theta = "theta[" + str(spe_idx) + "]"

                        power = coef
                        if power != 1:
                            theta += "**" + str(power)

                        term += "*" + theta

                    for i in current_list:
                        if dict1[i] == "surf":
                            continue  # bare surface ... skip

                        coef = 0
                        for imol, mol in enumerate(mol_list2):
                            spe = mol[1]
                            adsorbate = dict1[i]
                            if spe == adsorbate:
                                coef = coefs[imol]

                        if coef == 0:
                            raise ValueError("something wrong")

                        sto_coef = str(float(coef))

                        if i in dict2:
                            dict2[i] += sign + sto_coef + \
                                "*" + term  # NEGATIVE
                        else:
                            dict2[i] = sign + sto_coef + "*" + term

                        if "theta" in dict2[i]:
                            dict2[i] += "*" + "(area/Vr)"

                    # loop for current_list
                # direction
            # side
        # loop over elementary reactions

        # term for the vacant site
        #   formation/consumption rates for all the surface species should be
        #   subtracted from the vacant site.
        if "surf" in dict1.values():
            # surface reaction
            tmp = ""
            ind = [key for key, value in dict1.items() if value == "surf"][0]  # index for "surf"

            for imol, mol in enumerate(dict1):
                comp = dict1[imol]
                if "surf" in comp and comp != "surf":
                    # surface reaction but not surface itself
                    tmp += " -rate[" + str(imol) + "]"

            dict2[ind] = tmp

        comment = "\n\t# species --- "

        for imol, mol in enumerate(dict2):
            fout.write("\trate[{0}] ={1}  # {2}\n".format(imol, dict2[imol], dict1[imol]))
            comment += "%s = %s " % (imol, dict1[imol])
        comment += "\n"

        fout.write(comment)

        # template - start
        # Divide by site density to make it fractional occupation, according to C(8.6).
        lines = [
            "\trate[0:ngas] = (1/tau)*(C0[0:ngas] - C[0:ngas]) + rate[0:ngas]\n",
            "\tif ncomp > ngas:\n",
            "\t\trate[ngas:ncomp] *= (1/sden)  # surface\n"
        ]
        # template - end
        fout.writelines(lines)

        fout.write("\treturn rate\n")
        fout.write("\n")
        fout.close()

        return None

    def get_entropy_differences(self, x_dict=None):
        """
        Calculate the entropy difference (deltaS, in eV/K) for all the elementary reactions.

        Args:
            x_dict:
        Returns:
            deltaSs: numpy array
        """
        deltaSs = np.zeros(len(self.reaction_list))
        for i, reaction in enumerate(self.reaction_list):
            deltaSs[i] = reaction.get_entropy_difference(x_dict=x_dict)
        return deltaSs

    def get_equilibrium_constant_from_deltaEs(self, deltaEs=None, T=300.0, P=1.0, x_dict=None, verbose=False):
        """
        Get deltaGs by adding entropy and work (PV) contributions to deltaEs,
        and convert it to Kc (equilibriums constant in concentration unit).

        Args:
            deltaEs: reaction energy [eV]
            T: temperature [K]
            P: total pressure [bar]
            x_dict:
            verbose: print deltaG [in eV] or not
        Returns:
            Kc: equilibrium constant of elementary reactions as array, in concentration unit [numpy array]
        """
        deltaEs = deltaEs.copy()
        deltaSs = self.get_entropy_differences(x_dict=x_dict)
        deltaSs = deltaSs.copy()
        TdeltaSs = T*deltaSs

        deltaVs = self.get_deltaVs()
        P_Pa = P*1.0e5  # [bar] --> [Pa]
        PVs  = P_Pa*deltaVs*1.0e-3  # [Pa]*[m^3/mol] = [J/mol] --> [kJ/mol]
        PVs  = PVs/eVtokJ  # [kJ/mol] --> [eV], convert for printing
        deltaGs = deltaEs - TdeltaSs + PVs
        self._deltaEs_eV  = deltaEs
        self._deltaGs_eV  = deltaGs
        self._TdeltaSs_eV = TdeltaSs

        if verbose:
            print("TdeltaSs [in eV]")
            self.print_for_all_the_reactions(self._TdeltaSs_eV)
            print("deltaGs [in eV]")
            self.print_for_all_the_reactions(self._deltaGs_eV)

        self._deltaGs = self._deltaGs_eV * eVtokJ

        if os.path.exists("deltaGs.pickle"):
            with open("deltaGs.pickle", "rb") as read:
                self._deltaGs = pickle.load(read)
                print("=======================================================")
                print("loaded deltaGs from deltaGs.pickle as a external source")
                print("=======================================================")

        Kp = np.exp(-self._deltaGs/R/T)  # in pressure unit

        nus = self.get_nus()  # nus[species][rxn]

        rxn_num  = len(self.reaction_list)
        nus_gas  = np.zeros(rxn_num)
        nus_surf = np.zeros(rxn_num)

        for i in range(rxn_num):
            tmp_surf = 0
            tmp_gas  = 0
            for k, species in enumerate(self.get_unique_species()):
                spe_ind = self.get_index_of_species(species)
                if "surf" in species:
                    tmp_surf += nus[spe_ind][i]
                else:
                    tmp_gas += nus[spe_ind][i]

            nus_gas[i]  = tmp_gas
            nus_surf[i] = tmp_surf

        # convert to concentration unit (note: R is in kJ/mol/K)
        # Eq. C(4.6) in p.41
        P0 = 1.0e5    # standard state pressure [Pa]
        factor_gas  = np.power(P0/(R*1.0e3*T), nus_gas)
        factor_surf = np.power(self._sden, nus_surf)
        Kc = factor_gas*factor_surf*Kp
        return Kc

    def solve_rate_equation(self, odefile=None, deltaEs=None, kfor=None, T=300.0, P=1.0, p_ratio=None,
                            verbose=False, plot=False):
        """
        Solve rate equations.

        Args:
            odefile: ODE file
            deltaEs: reaction energy [eV]
            kfor: rate coefficients in forward direction
            T: temperature [K]
            P: total pressure [bar]
            p_ratio: pressure ratio of inlet (dict) [-]
            verbose: whether to do verbose output
            plot:
        Returns:
            t: time [sec]
            C: molar concentration [mol/m^3]
        """
        if p_ratio is None:
            p_ratio = {}

        curdir = os.getcwd()
        tmpode_path = os.path.join(curdir, odefile)

        if os.path.exists(tmpode_path):
            rate_eqn = get_obj_from_script(tmpode_path, "rate_eqn")
        else:
            raise AssertionError("tmpode.py is needed")

        if kfor is None:
            raise ValueError("rate coefficients not found")
        if odefile is None:
            raise ValueError("ODE file not found")

        np.set_printoptions(precision=4, linewidth=100)

        # read species
        species = self.get_unique_species()
        ncomp = len(species)
        ngas = len(list(filter(lambda x: "surf" not in x, species)))

        # output results here
        if verbose:
            print("deltaEs [in eV]")
            self.print_for_all_the_reactions(deltaEs)
            print("res. time [sec]: {0:5.3e}, GHSV [hr^-1]: {1:3d}".format(self._tau, int(60**2/self._tau)))

        # now solve the ODE
        t0, tf = 0, self._tau
        dt = tf * 1.0e-3
        t_span = (t0, tf)
        t_eval = np.arange(t0, tf, dt)

        x0 = np.ones(ncomp)*tiny  # molar fraction [-]
        C0 = np.ones(ncomp)*tiny  # molar concentration [mol/m^3]

        for ispe, spe in enumerate(species):
            val = p_ratio.get(spe)
            x0[ispe] = val if val is not None else tiny

        # normalize x0 gas part
        tot = np.sum(x0[:ngas])
        x0[0:ngas] /= tot

        # surface site fraction: the last term is vacant site
        x0[-1] = 1.0 - np.sum(x0[ngas:ncomp-1])

        # normalize surface part
        tot = np.sum(x0[ngas:ncomp])
        x0[ngas:ncomp] /= tot

        # density calculated from pressure. Note: R is in [kJ/mol/K].
        P_Pa = P * 1e5  # [bar] -> [Pa]
        C0[0:ngas] = (P_Pa/((R*1e3)*T))*x0[0:ngas]
        C0[ngas:ncomp] = x0[ngas:ncomp]

        # self.print_C_sum(C0)

        area_ = self._area * self._wcat  # [m^2/kg]*[kg] --> [m^2]

        t = np.zeros(1)
        y = np.empty((ncomp, 0))
        y = np.append(y, C0.reshape(ncomp, 1), axis=1)   # set C0 to initial position

        use_solve_ivp = True

        for icstr in range(self.Ncstr):
            print("-- icstr = {}".format(icstr))

            # calculate molar fraction dict
            x_dict = self.calculate_x_dict(C0=C0, T=T)

            # recalculate Gibbs energy
            Kc = self.get_equilibrium_constant_from_deltaEs(deltaEs, T=T, P=P, x_dict=x_dict, verbose=verbose)

            # TODO: include adsorbate-adsorbate interaction

            if use_solve_ivp:
                # new scipy code
                soln = solve_ivp(fun=lambda t, C: rate_eqn(t, C, C0, kfor, Kc, self._sden, area_,
                                 self._Vr, self._tau, ngas, ncomp), t_span=t_span, t_eval=t_eval,
                                 y0=C0, rtol=self._ode_rtol, atol=self._ode_atol, method=self._ode_solver)
                print(soln.nfev, "evaluations requred.")
                t_ = soln.t
                y_ = soln.y
            else:
                # old scipy code
                ntime = 1000  # number of timesteps to output
                dt = float(self._tau / ntime)

                t_ = np.empty(ntime)
                y_ = np.empty((ncomp, ntime))

                solver = ode(rate_eqn)
                solver.set_integrator(name="lsoda", rtol=self._ode_rtol, atol=self._ode_atol, nsteps=1000)
                solver.set_initial_value(C0, t=0.0)
                solver.set_f_params(C0, kfor, Kc, self._sden, area_, self._Vr, self._tau, ngas, ncomp)

                index = 0
                while index < ntime:
                    solver.integrate(solver.t + dt)
                    y_[:, index] = solver.y[:]
                    t_[index] = solver.t
                    index += 1

            if icstr == 0:
                t = np.append(t, t_, axis=0)
                y = np.append(y, y_, axis=1)
            else:
                t = np.append(t, t[-1] + t_, axis=0)
                y = np.append(y, y_, axis=1)

            # set C0 for next CSTR
            if use_solve_ivp:
                C0[0:ngas]  = soln.y[0:ngas, -1]
                #C0[0:ncomp] = soln.y[0:ncomp, -1]
            else:
                C0[0:ngas] = y[0:ngas, -1]
                #C0[0:ncomp] = y[0:ncomp, -1]

        C = y  # y is actually molar concentration ... change variable name to C
        if plot:
            self.draw_molar_concentration_change(t=t, C=C, filename=None)

        self.save_coverage(t=t, C=C)
        self.get_conversion(C=C)

        # self.print_C_sum(C[:, -1])  # molar fraction

        return t, C

    def calculate_x_dict(self, C0=None, T=300.0, P_Pa=1e5):
        """
        Calculate molar fraction dict (with no dimension).

        Args:
            C0: molar concentration [mol/m^3]
            T: temperature [K]
            P_Pa: total pressure [Pa]
        Returns:
            x_dict: molar fraction of species [-]
        """
        species = self.get_unique_species()

        x_dict = {}
        for k, spe in enumerate(species):
            spe_ind = self.get_index_of_species(spe)
            if "surf" in spe:
                continue
                #x_dict.update({spe: C0[spe_ind]})
            else:
                x_dict.update({spe: C0[spe_ind]*(R*1e3*T/P_Pa)})  # to molar fraction

        return x_dict

    def print_C_sum(self, x0=None):
        species = self.get_unique_species()
        ngas = len(list(filter(lambda x: "surf" not in x, species)))

        C_sum = 0.0
        for ispe in range(ngas):
            if "C" in species[ispe]:
                C_sum += x0[ispe]
                print("{0:s}: {1:5.3e}".format(species[ispe], x0[ispe]))

        print("C_sum: {:5.3e}".format(C_sum))
        return None

    def save_coverage(self, t=None, C=None):
        """
        Save surface coverage: for time-independent, output the coverage at the last time step

        Args:
            t: time
            C: molar concentration and coverage
        """
        fac = 1.0e-6

        species = self.get_unique_species()
        ncomp = len(species)
        ngas  = len(list(filter(lambda x: "surf" not in x, species)))
        maxtime = len(t)

        tcov = []  # time-dependent coverage: tcov[species][time]
        for i in range(ngas):
            tcov.append(C[i])
        for i in range(ngas, ncomp):
            # multiply scaling factor for surface species
            tcov.append(C[i]*fac)
        tcov = np.array(tcov)

        with h5py.File("coverage.h5", "w") as h5file:
            h5file.create_dataset("time", shape=(maxtime,), dtype=np.float, data=t)
            h5file.create_dataset("concentration", (ncomp, maxtime), dtype=np.float, data=tcov)

        return None

    def get_conversion(self, C=None, verbose=True):
        """
        Get conversion.

        Args:
            C: molar concentration [mol/m^3] and coverage
            verbose: verbose or not
        """
        species = self.get_unique_species()
        gas_sp_ids = [isp for isp, sp in enumerate(species) if "surf" not in sp]

        self._conversion_info = {}
        self._gas_flow_info = {}
        self._gas_flow_info["input[mol/m^3]"] = {}
        self._gas_flow_info["output[mol/m^3]"] = {}
        self._gas_flow_info["rate[mol/(g*s)]"] = {}

        if verbose:
            print("---- conversion (%) ----")

        for ispe in gas_sp_ids:
            xin  = C[ispe][0]
            xout = C[ispe][-1]
            self._gas_flow_info["input[mol/m^3]"][species[ispe]]  = xin
            self._gas_flow_info["output[mol/m^3]"][species[ispe]] = xout
            self._gas_flow_info["rate[mol/(g*s)]"][species[ispe]] = self._get_macro_rate(xin=xin, xout=xout)

            if xin < tiny*1e2:  # sometimes becomes larger than tiny
                conversion = 0.0
            else:
                conversion = (xin - xout)/xin
            self._conversion_info.update({species[ispe]: conversion})

            if verbose:
                print("{0:12s}: conversion = {1:>8.2f}".format(species[ispe], 100*conversion))

        return None

    def _get_macro_rate(self, xin: float, xout: float) -> float:
        diff = xout - xin
        macro_rate = diff / (self._wcat * 1.0e3) / self._total_tau
        return macro_rate

    def draw_molar_concentration_change(self, t=None, C=None, filename=None, thre=1.0e-4):
        """
        Draw molar fraction change with time.

        Args:
            t: time
            C: molar concentration and coverage
            filename: file name when saving figure
            thre: threshold to plot
        """
        import matplotlib.pyplot as plt

        species = self.get_unique_species()
        ncomp = len(species)
        ngas = len(list(filter(lambda x: "surf" not in x, species)))

        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 4))
        cl_iter1 = gene_20color_4lstyle()
        cl_iter2 = gene_20color_4lstyle()

        print("\n{0:12s}{1:14s}{2:12s}".format("species", "inlet", "outlet"))
        for i, ispe in enumerate(species):
            print("{0:12s}{1:5.3e} --> {2:5.3e}".format(ispe, C[i][0], C[i][-1]))

            if max(C[i]) < thre:
                continue
            else:
                if "surf" in ispe:
                    color, lstyle = next(cl_iter2)
                    ad_label = "theta{}".format(ispe.replace("_", "").replace("surf", ""))
                    ax2.plot(t, C[i], label=ad_label, color=color, ls=lstyle)
                else:
                    color, lstyle = next(cl_iter1)
                    ax1.plot(t, C[i], label="{}".format(ispe), color=color, ls=lstyle)

        ax1.set_xlabel("time [sec]")
        ax1.set_ylabel("concentration [mol/m^3]")
        ax1.set_ylim([-C[0:ngas].max()*0.1, C[0:ngas].max()*1.1])
        ax1.grid()

        ax2.set_xlabel("time [sec]")
        ax2.set_ylabel("fractional coverage [-]")
        ax2.set_ylim([-C[ngas:ncomp].max()*0.1, C[ngas:ncomp].max()*1.1])
        ax2.grid()

        ax1.legend()
        ax2.legend(bbox_to_anchor=(1.05, 1), fontsize=8)

        fig.tight_layout()
        if filename is not None:
            plt.figure(fig.number)
            plt.savefig(filename)
            plt.close()
        else:
            plt.figure(fig.number)
            plt.show()
        return None

    def get_rate_for_graph(self, T=300.0, P=1.0):
        """
        Get total rate.

        Args:
            T: temperature [K]
            P: total pressure [bar]
        Returns:
            total_rate: numpy array
        """
        conc_h5 = "coverage.h5"
        deltaEs_pickle = "deltaEs.pickle"

        rxn_num = len(self.reaction_list)

        with h5py.File(conc_h5, "r") as h5file:
            time = h5file["time"][:]
            cov = h5file["concentration"][:]

        max_time = len(time)

        # read deltaEs
        with open(deltaEs_pickle, "rb") as file:
            deltaEs = pickle.load(file)

        kfor = self.get_rate_coefficients(deltaEs=deltaEs, T=T)
        Kc = self.get_equilibrium_constant_from_deltaEs(deltaEs, T=T, P=P, verbose=False)
        krev = kfor / Kc

        print("In get_rate_for_graph, set self._kfor, ._krev, and ._Kc")
        self._kfor = kfor
        self._krev = krev
        self._Kc = Kc

        AoverV = self._area / self._Vr

        # output information for graph
        rates = {"forward": None, "reverse": None}
        for direction in ["forward", "reverse"]:
            rate = np.zeros((max_time, rxn_num))
            for irxn, reaction in enumerate(self.reaction_list):
                if direction == "forward":
                    sequence = reaction.reactants
                    k = kfor
                elif direction == "reverse":
                    sequence = reaction.products
                    k = krev

                for istep in range(max_time):
                    conc_all = 1.0
                    for mol in sequence:
                        coef, spe, site = mol
                        spe_idx = self.get_index_of_species(spe)
                        conc = cov[spe_idx][istep]
                        if site != "gas":  # surface species
                            conc *= self._sden * AoverV
                        if coef != 1:
                            conc = conc ** coef

                        conc_all = conc_all * conc

                    rate[istep][irxn] = k[irxn] * conc_all

            rates[direction] = rate

        total_rate = np.zeros(rxn_num)
        for irxn in range(rxn_num):
            total_rate[irxn] = rates["forward"][-1][irxn] - rates["reverse"][-1][irxn]

        print("rate [in -]")
        self.print_for_all_the_reactions(total_rate)

        with open("rate.pickle", "wb") as file:
            pickle.dump(total_rate, file)

        return total_rate

    def print_for_all_the_reactions(self, property=None):
        """
        Print function.

        Args:
            property:
        """
        print("{0:^42.40s}{1:^12s}".format("reaction", "value"))
        for irxn, reaction in enumerate(self.reaction_list):
            print("{0:<42.40s}{1:>10.2e}".format(reaction._reaction_str, property[irxn]))
        print("")

    def do_preparation(self):
        from .preparation import preparation
        # should pass the adsorbate set
        preparation.prepare(self.get_unique_species())
        pass

    def sort_atoms_by_z(self, atoms):
        import ase
        import copy

        dtype = [("idx", int), ("z", float)]

        # get set of chemical symbols
        atoms_copy = copy.deepcopy(atoms)
        symbols = atoms_copy.get_chemical_symbols()
        elements = sorted(set(symbols), key=symbols.index)
        num_elem = []
        for i in elements:
            num_elem.append(symbols.count(i))

        iatm = 0
        newatoms = ase.Atoms()
        for inum in num_elem:
            zlist = np.array([], dtype=dtype)
            for idx in range(inum):
                tmp = np.array([(iatm, atoms_copy[iatm].z)], dtype=dtype)
                zlist = np.append(zlist, tmp)
                iatm += 1

            zlist = np.sort(zlist, order="z")

            for i in zlist:
                idx = i[0]
                newatoms.append(atoms[idx])

        newatoms.tags = atoms_copy.get_tags()
        newatoms.pbc = atoms_copy.get_pbc()
        newatoms.cell = atoms_copy.get_cell()

        return newatoms

    def get_sensitivity(self, deltaEs=None, kfor=None, T=300, P=1.0, p_ratio=None, delta=0.01,
                        npoints=3, plot: bool = True, sensitivity_figure: str = None, species_list=None):
        """
        Get sensitivity.

        Args:
            deltaEs:
            kfor:
            T:
            P:
            p_ratio:
            delta:
            npoints:
            plot:
            sensitivity_figure:
            species_list:

        Returns:
        """
        import matplotlib.pyplot as plt
        import copy

        if p_ratio is None:
            p_ratio = {}

        cudir = os.getcwd()
        odefile = os.path.join(cudir, "tmpode.py")
        self.make_rate_equation(odefile=odefile)

        nrxn = len(self.reaction_list)
        species = self.get_unique_species()
        gas  = list(filter(lambda x: "surf" not in x, species))
        ngas = len(gas)

        sens = np.zeros((ngas, nrxn))  # need surface species?
        for irxn in range(nrxn):
            print("evaluating sensitivity for rxn = {0:d}/{1:d}".format(irxn, nrxn-1))
            M0 = np.zeros(ngas)
            Mp = np.zeros(ngas)
            Mm = np.zeros(ngas)

            # unperturbated
            kfor_tmp = copy.copy(kfor)
            k0 = kfor_tmp[irxn]
            t, C = self.solve_rate_equation(odefile=odefile, deltaEs=deltaEs, kfor=kfor_tmp, T=T, P=P,
                                            p_ratio=p_ratio, verbose=False, plot=False)
            for ispe in range(ngas):
                # xin  = y[ispe][0]
                xout = C[ispe][-1]
                if species[ispe] in p_ratio:
                    #M0[ispe] = (xin - xout)/xin
                    M0[ispe] = -xout
                else:
                    M0[ispe] = xout

            # perturbated - plus
            kfor_tmp = copy.copy(kfor)
            kfor_tmp[irxn] = kfor_tmp[irxn]*(1+delta)
            kp = kfor_tmp[irxn]
            t, C = self.solve_rate_equation(odefile=odefile, deltaEs=deltaEs, kfor=kfor_tmp,
                                            T=T, P=P, p_ratio=p_ratio, verbose=False, plot=False)
            for ispe in range(ngas):
                # xin  = y[ispe][0]
                xout = C[ispe][-1]
                if species[ispe] in p_ratio:
                    # Mp[ispe] = (xin - xout)/xin
                    Mp[ispe] = -xout
                else:
                    Mp[ispe] = xout

            # perturbated - minus, only measured at npoints = 3
            if npoints == 3:
                kfor_tmp = copy.copy(kfor)
                kfor_tmp[irxn] = kfor_tmp[irxn]*(1-delta)
                km = kfor_tmp[irxn]
                t, C = self.solve_rate_equation(odefile=odefile, deltaEs=deltaEs, kfor=kfor_tmp,
                                                T=T, P=P, p_ratio=p_ratio, verbose=False, plot=False)
                for ispe in range(ngas):
                    # xin  = y[ispe][0]
                    xout = C[ispe][-1]
                    if species[ispe] in p_ratio:
                        #Mm[ispe] = (xin - xout)/xin
                        Mm[ispe] = -xout
                    else:
                        Mm[ispe] = xout

            # form delta_M and delta_k
            if npoints == 2:
                delta_M = Mp - M0  # array
                delta_k = kp - k0  # scalar
            elif npoints == 3:
                delta_M = Mp - Mm  # array
                delta_k = kp - km  # scalar
            else:
                raise ValueError("Something wrong in get_sensitivity")

            for ispe in range(ngas):
                #sens[ispe, irxn] = (delta_M[ispe]/M0[ispe])*(k0/delta_k)  # normalized -- better
                sens[ispe, irxn] = (delta_M[ispe]/delta_k)*k0  # semi-normalized

        ylabels = []
        react_str_li = [reaction._reaction_str for reaction in self.reaction_list]
        for ispe in range(ngas):
            ylabels.append(species[ispe])
        seaborn.heatmap(sens, cbar=True, xticklabels=react_str_li, yticklabels=ylabels)
        plt.yticks(rotation=0,  fontsize=8)
        plt.xticks(rotation=90, fontsize=8)
        plt.tight_layout()
        plt.show()
        plt.close()

        # plot
        if species_list is None:
            species_list = gas

        small = 0.1
        plt.rcParams['axes.axisbelow'] = True
        for spe in species_list:
            idx = self.get_index_of_species(spe)
            plt.bar(x=range(nrxn), height=sens[idx, :], tick_label=react_str_li)
            plt.ylim([min(sens[idx, :])*(1+small), max(sens[idx, :])*(1+small)])
            plt.xlabel("Elementary reactions (-)")
            plt.ylabel("Sensitivity for {0:s} (-)".format(spe))
            plt.xticks(rotation=90, fontsize=8)
            plt.tight_layout()
            plt.grid(axis="x", linestyle="dotted")
            if sensitivity_figure is not None:
                png_name = "sensitiviy_for_{}.png".format(spe)
                out_png = os.path.join(sensitivity_figure, png_name)
                plt.savefig(out_png)
            if plot:
                plt.show()
            plt.close()
        self._sens_matrix = sens
        return sens

    def get_error_propagation(self, total_rate=None, plot=True):
        """
        Get error propagation.

        Args:
            total_rate:
            plot:
        Returns:
            rAB: DataFrame
        """
        import seaborn

        species = self.get_unique_species()
        rAB = np.zeros((len(species), len(species)))

        for ispeA, speA in enumerate(species):
            for ispeB, speB in enumerate(species):
                if speA == speB:
                    continue

                numer = 0.0
                denom = 0.0
                for irxn, rxn in enumerate(self.reaction_list):
                    coef = rxn.get_coefficient_of_species(species=speA)
                    if (speB in rxn.reactant_species) or (speB in rxn.product_species):
                        delta = 1.0
                    else:
                        delta = 0.0
                    numer = numer + abs(coef*total_rate[irxn]*delta)
                    denom = denom + abs(coef*total_rate[irxn])

                rAB[ispeA, ispeB] = numer/denom

        index   = species
        columns = species

        rAB = pd.DataFrame(data=rAB, index=index, columns=columns)
        # rAB[rAB > 1.0e-20] = 1.0

        if plot:
            seaborn.heatmap(rAB, linewidth=0.5, xticklabels=True, yticklabels=True, square=True)
            plt.tight_layout()
            plt.show()

        return rAB

    def make_reduced_mechanism(self, csvfile="reduced.csv", reactants=None, products=None, keep=None,
                               rAB=None, thre=1.0e-5, verbose=False):
        """
        Do mechanism reduction by directed related graph.

        Args:
            csvfile:
            reactants:
            products:
            keep:
            rAB:
            thre:
            verbose:
        Returns:
            None
        """
        if verbose:
            print(" === doing mechanism reduction with thre = {0:5.3e}===".format(thre))

        def find_root_species(species=None, rAB=None):
            """
            Function to find root species from given one.

            Args:
                species:
                rAB:
            Returns:

            """
            li = []
            for spe in species:
                series = pd.Series(rAB.loc[spe, :])
                series = series.iloc[:-1]  # remove vacant site, as it is always important
                series = series.sort_values(ascending=False)
                remain = series[series > thre]

                if len(remain) == 0:  # Oops! All species are dropped! Add the most important one.
                    ind = series.argmax()
                    val = series.iloc[ind]
                    remain = series[series > val-tiny]

                idx = remain.index
                for i in idx:
                    li.append(i)

            li = list(set(li))
            return li

        max_counter = 10
        need = []

        # from reactants
        new_spe = reactants

        counter = 0
        while counter < max_counter:
            print("original_1: ", new_spe)
            new_spe = find_root_species(species=new_spe, rAB=rAB)
            new_spe = list(filter(lambda x: x not in need, new_spe))
            print("found_1: ", new_spe)
            need += new_spe
            products = list(filter(lambda x: x not in new_spe, products))  # rm species from reactant

            if len(new_spe) == 0:
                break

            counter += 1

        # from products
        new_spe = products

        counter = 0
        while counter < max_counter:
            print("original_2: ", new_spe)
            new_spe = find_root_species(species=new_spe, rAB=rAB)
            new_spe = list(filter(lambda x: x not in need, new_spe))
            print("found_2: ", new_spe)
            need += new_spe
            reactants = list(filter(lambda x: x not in new_spe, reactants))  # rm species from reactant

            if len(new_spe) == 0:
                break

            counter += 1

        need = list(set(need))
        need = need + reactants + products + keep
        species = self.get_unique_species()
        do_not_need = list(filter(lambda x: x not in need, species))
        do_not_need.remove("surf")

        reactions = []
        self._reduced_discarded_rxns_info = []
        for reaction in self.reaction_list:
            all_species = reaction.reactant_species + reaction.product_species
            if set(all_species).isdisjoint(set(do_not_need)):
                reactions.append(reaction)
            else:
                # skip this elementary reaction
                if verbose:
                    id  = reaction.to_dict()["_reaction_id"]
                    str = reaction.to_dict()["_reaction_str"]
                    ddict = reaction.to_dict()
                    self._reduced_discarded_rxns_info.append(ddict)
                    print("discarding {0:3d}-th rxn: {1:s}".format(id, str))
                continue

        new_rxns = self.make_reactions_from_list(reaction_list=reactions)
        self._reduced_rxns_info = list(new_rxns._generate_reactions_dict())
        new_rxns.to_csv(file=csvfile)

        if verbose:
            print("reduced mechanism written to {0:s}".format(csvfile))
            print(" === mechanism reduction finished ===")

        return None

    @property
    def deltaGs_eV(self):
        if hasattr(self, "_deltaGs_eV"):
            return self._deltaGs_eV
        else:
            mes = "Use get_equilibrium_constant_from_deltaEs to set deltaGs(T, P)"
            raise AttributeError(mes)

    @property
    def TdeltaSs_eV(self) -> np.ndarray:
        if hasattr(self, "_TdeltaSs_eV"):
            return self._TdeltaSs_eV
        else:
            mes = "Use get_equilibrium_constant_from_deltaEs to set TdeltaSs(T, P)"
            raise AttributeError(mes)

    @property
    def dEas_eV(self) -> np.ndarray:
        dEas_li = []
        for reaction in self.reaction_list:
            assert isinstance(reaction, Reaction)
            dEas_li.append(reaction.Ea_eV)
        dEas_ar = np.array(dEas_li)
        return dEas_ar

    @property
    def dEs_eV(self) -> np.ndarray:
        if hasattr(self, "_deltaEs_eV"):
            return self._deltaEs_eV
        else:
            mes = "Use get_equilibrium_constant_from_deltaEs to set _dEs_eV"
            raise AttributeError(mes)

    @classmethod
    def make_reactions_from_list(cls, reaction_list):
        return cls(reaction_list)

    @classmethod
    @abstractmethod
    def get_reaction_energies(cls):
        raise NotImplementedError("must overwrite this method.")
