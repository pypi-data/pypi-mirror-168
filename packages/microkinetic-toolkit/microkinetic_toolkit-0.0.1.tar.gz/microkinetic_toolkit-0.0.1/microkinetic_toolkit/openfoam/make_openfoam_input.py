import numpy as np
import os
import shutil
import textwrap
from ase import Atoms
import collections
from microkinetic_toolkit.reactions import Reactions

class OpenfoamInputMaker(Reactions):
    """
    Class to control the input-making-procedure for openFOAM.
    """
    def __init__(self, reaction_list, inert=None):
        self.reaction_list = reaction_list
        self.foamfile = "version   2.0;\n" \
                        "format    ascii;\n" \
                        "class     {0:};\n" \
                        "location  {1:};\n" \
                        "object    {2:};\n"
        if inert is None:
            self.inert = "He"
        else:
            self.inert = inert

    def copy_template_dir(self, templatedir=None, targetdir=None):
        pwd = os.getcwd()
        dir = os.path.join(pwd, targetdir)
        if os.path.isdir(dir):
            shutil.rmtree(dir)
        os.makedirs(dir)

        shutil.copytree(os.path.join(templatedir, "constant"), os.path.join(dir, "constant"))
        shutil.copytree(os.path.join(templatedir, "system"), os.path.join(dir, "system"))
        shutil.copytree(os.path.join(templatedir, "0.orig"), os.path.join(dir, "0.orig"))
        shutil.copytree(os.path.join(templatedir, "mesh_orig"), os.path.join(dir, "mesh_orig"))
        shutil.copy(os.path.join(templatedir, "Allrun"), dir)
        shutil.copy(os.path.join(templatedir, "Allclean"), dir)

        return None

    def _get_mass_fraction_from_p_ratio(self, p_ratio=None):
        if self.inert is not None:
            p_ratio.update({self.inert: 100})

        p_sum = 0.0
        for v in p_ratio.values():
            p_sum += v

        mol_frac = {}
        for ispe in p_ratio.keys():
            mol_frac.update({ispe: p_ratio[ispe]/p_sum})

        mol_weight = {}
        mol_weight_avg = 0.0
        for ispe in p_ratio.keys():
            weight  = np.sum(Atoms(ispe).get_masses())
            mol_weight.update({ispe: weight})
            mol_weight_avg += mol_frac[ispe]*weight

        mass_fractions = {}
        for key in p_ratio.keys():
            mass_fraction = (p_ratio[key]/p_sum) * (mol_weight[key]/mol_weight_avg)
            mass_fractions.update({key: mass_fraction})

        return mass_fractions

    def make_speciesfiles(self, directory=None, surface_atoms=None, p_ratio=None):
        """
        Make openFOAM species file in specified directory.

        Args:
            directory:
            surface_atoms:
            p_ratio: partial pressure ratio
        """
        species = self.get_unique_species()
        gas = list(filter(lambda x: "surf" not in x, species))
        gas.append(self.inert)

        inlet =   "type         fixedValue;\n" \
                  "value        $internalField;\n"
        outlet =  "type         inletOutlet;\n" \
                  "inletValue   $internalField;\n" \
                  "value        $internalField;\n"
        inner  =  "type         zeroGradient;\n"
        center =  "type         zeroGradient;\n"
        zmin =    "type         symmetry;\n"
        region0 = "type         nimsMappedMassFluxFraction;\n" \
                  "massFluxName {0:s}_Flux;\n" \
                  "value        $internalField;\n"

        if surface_atoms is None:
            # gas
            mass_fractions = self._get_mass_fraction_from_p_ratio(p_ratio=p_ratio)
            for spe in gas:
                file = os.path.join(directory, spe)
                with open(file, "w") as f:
                    f.write("")

                self._write_speciesinfo(file=file, species=spe, inlet=inlet, outlet=outlet,
                                        inner=inner, center=center, zmin=zmin, region0=region0,
                                        mass_fractions=mass_fractions)
        else:
            # surface
            elements = list(set(surface_atoms.get_chemical_symbols()))
            elements = "".join(elements)
            spe = elements + "(S)"
            file = os.path.join(directory, spe)

            with open(file, "w") as f:
                f.write("")

            self._write_speciesinfo(file=file, species=spe, inlet=inlet, outlet=outlet,
                                    inner=inner, center=center, zmin=zmin, region0=region0, is_surface=True)

        return None

    def _write_speciesinfo(self, file=None, species=None, inlet=None, outlet=None,
                                 inner=None, center=None, zmin=None, region0=None, is_surface=False,
                                 mass_fractions=None):

        if not is_surface:
            try:
                mass_fraction = mass_fractions[species]
            except:
                mass_fraction = 0.0

            foamfile_ = self.foamfile.format("volScalarField", "\"0\"", species)
        else:
            mass_fraction = 1.0
            foamfile_ = self.foamfile.format("volScalarField", "\"0/panelRegion\"", species)

        self._write_section(file=file, sectionname="FoamFile", string=foamfile_, indentlevel=0)

        with open(file, "a") as f:
            zerolist = [0]*7
            info  = "dimensions {0:};\n\n"
            info += "internalField uniform {1:};\n\n"
            info_ = info.format(zerolist, mass_fraction)
            info_ = info_.replace(",", "")
            f.write(info_)

        with open(file, "a") as f:
            ini = "boundaryField\n{\n"
            f.write(ini)

        if not is_surface:
            self._write_section(file=file, sectionname="inlet", string=inlet)
            self._write_section(file=file, sectionname="outlet", string=outlet)
            self._write_section(file=file, sectionname="\"innerWall|outerWall\"", string=inner)
            self._write_section(file=file, sectionname="center", string=center)
            self._write_section(file=file, sectionname="\"zmin|zmax\"", string=zmin)
            region0_ = region0.format(species)
            self._write_section(file=file, sectionname="region0_to_panelRegion_panel",
                                string=region0_)
        else:
            top     = "type   zeroGradient;\n"
            region0 = "type   fixedValue;\n" \
                      "value  $internalField;\n"
            side    = "type   empty;\n"

            self._write_section(file=file, sectionname="panel_top", string=top)
            self._write_section(file=file, sectionname="region0_to_panelRegion_panel", string=region0)
            self._write_section(file=file, sectionname="panel_side", string=side)

        with open(file, "a") as f:
            fin = "}\n"
            f.write(fin)

        return None

    def _makedir(self, dirname=None, subdirname=None, clean=False):
        if subdirname is None:
            dir = dirname
        else:
            dir = os.path.join(dirname, subdirname)

        if not os.path.isdir(dir):
            os.makedirs(dir)
        else:
            if clean:
                shutil.rmtree(dir)
                os.makedirs(dir)

        return None

    def make_Ufile(self, file=None, u_vec=None):
        """
        Make openFOAM U file.

        Args:
            file:
            u_vec: velocity vector [m/sec?]
        """
        if u_vec is None:
            u_vec = [0.0, 0.0, 0.0]
        with open(file, "w") as f:
            f.write("")

        dim = [0, 1, -1, 0, 0, 0, 0]
        zerovec = [0]*3

        inlet =   "type       fixedValue;\n" \
                  "value      uniform ({0[0]:10.2e}{0[1]:10.2e}{0[2]:10.2e});\n"
        outlet =  "type       inletOutlet;\n" \
                  "inletValue $internalField;\n" \
                  "value      $internalField;\n"
        inner  =  "type       fixedValue;\n" \
                  "value      uniform (0 0 0);\n"
        center =  "type       slip;\n"
        zmin =    "type       symmetry;\n"
        region0 = "type       nimsMappedFlowRate;\n" \
                  "nbrPhi     phiGas;\n" \
                  "value      uniform (0 0 0);\n"

        foamfile_ = self.foamfile.format("volVectorField", "\"0\"", "U")
        self._write_section(file=file, sectionname="FoamFile", string=foamfile_, indentlevel=0)

        with open(file, "a") as f:
            info  = "dimensions {0:};\n\n"
            info += "internalField uniform ({1[0]:} {1[1]:} {1[2]:});\n\n"
            info_ = info.format(dim, zerovec)
            info_ = info_.replace(",", "")
            f.write(info_)

        with open(file, "a") as f:
            ini = "boundaryField\n{\n"
            f.write(ini)

        inlet_ = inlet.format(u_vec)
        self._write_section(file=file, sectionname="inlet", string=inlet_)
        self._write_section(file=file, sectionname="outlet", string=outlet)
        self._write_section(file=file, sectionname="\"innerWall|outerWall\"", string=inner)
        self._write_section(file=file, sectionname="center", string=center)
        self._write_section(file=file, sectionname="\"zmin|zmax\"", string=zmin)
        self._write_section(file=file, sectionname="region0_to_panelRegion_panel", string=region0)

        with open(file, "a") as f:
            fin = "}\n"
            f.write(fin)

        return None

    def make_Tfile(self, file=None, T=300.0, is_surface=False):
        """
        Make openFOAM T file.

        Args:
            file:
            T:
            is_surface:
        """
        with open(file, "w") as f:
            f.write("")

        dim = [0, 0, 0, 1, 0, 0, 0]

        if not is_surface:
            inlet =   "type       fixedValue;\n" \
                      "value      uniform {0:.2f};\n"
            outlet =  "type       inletOutlet;\n" \
                      "inletValue $internalField;\n" \
                      "value      $internalField;\n"
            inner =   "type       zeroGradient;\n"
            center =  "type       zeroGradient;\n"
            zmin =    "type       symmetry;\n"
            region0 = "type       nimsMappedHeatFlux;\n" \
                      "qName      qGas;\n" \
                      "value      $internalField;\n"

            foamfile_ = self.foamfile.format("volScalarField", "\"0\"", "T")
            self._write_section(file=file, sectionname="FoamFile", string=foamfile_, indentlevel=0)

            with open(file, "a") as f:
                info = "dimensions {0:};\n\n"
                info += "internalField uniform {1:};\n\n"
                info_ = info.format(dim, T)
                info_ = info_.replace(",", "")
                f.write(info_)

            with open(file, "a") as f:
                ini = "boundaryField\n{\n"
                f.write(ini)

            inlet_ = inlet.format(T)
            self._write_section(file=file, sectionname="inlet", string=inlet_)
            self._write_section(file=file, sectionname="outlet", string=outlet)
            self._write_section(file=file, sectionname="\"innerWall|outerWall\"", string=inner)
            self._write_section(file=file, sectionname="center", string=center)
            self._write_section(file=file, sectionname="\"zmin|zmax\"", string=zmin)
            self._write_section(file=file, sectionname="region0_to_panelRegion_panel", string=region0)

            with open(file, "a") as f:
                fin = "}\n"
                f.write(fin)

        else:
            top     = "type zeroGradient;\n"
            side    = "type empty;\n"
            region0 = "type zeroGradient;\n"

            foamfile_ = self.foamfile.format("volScalarField", "\"0/panelRegion\"", "T")
            self._write_section(file=file, sectionname="FoamFile", string=foamfile_, indentlevel=0)

            with open(file, "a") as f:
                info = "dimensions {0:};\n\n"
                info += "internalField uniform {1:};\n\n"
                info_ = info.format(dim, T)
                info_ = info_.replace(",", "")
                f.write(info_)

            with open(file, "a") as f:
                ini = "boundaryField\n{\n"
                f.write(ini)

            self._write_section(file=file, sectionname="panel_top",  string=top)
            self._write_section(file=file, sectionname="panel_side", string=side)
            self._write_section(file=file, sectionname="region0_to_panelRegion_panel", string=region0)

            with open(file, "a") as f:
                fin = "}\n"
                f.write(fin)

        return None

    def make_Pfile(self, file=None, is_surface=False, P=1.0):
        """
        Make openFOAM p file.

        Args:
            file:
            is_surface:
            P: Pressure [bar]
        """
        with open(file, "w") as f:
            f.write("")

        dim = [1, -1, -2, 0, 0, 0, 0]
        P_pa = P * 1.0e5

        if not is_surface:
            inlet =   "type      calculated;\n" \
                      "value     $internalField;\n"
            outlet =  "type      calculated;\n" \
                      "value     $internalField;\n"
            inner =   "type      calculated;\n" \
                      "value     $internalField;\n"
            center =  "type      calculated;\n" \
                      "value     $internalField;\n"
            zmin =    "type      symmetry;\n"
            region0 = "type      calculated;\n" \
                      "value     $internalField;\n"

            foamfile_ = self.foamfile.format("volScalarField", "\"0\"", "p")
            self._write_section(file=file, sectionname="FoamFile", string=foamfile_, indentlevel=0)

            with open(file, "a") as f:
                info  = "dimensions {0:};\n\n"
                info += "internalField uniform {1:};\n\n"
                info_ = info.format(dim, P_pa)
                info_ = info_.replace(",", "")
                f.write(info_)

            with open(file, "a") as f:
                ini = "boundaryField\n{\n"
                f.write(ini)

            self._write_section(file=file, sectionname="inlet", string=inlet)
            self._write_section(file=file, sectionname="outlet", string=outlet)
            self._write_section(file=file, sectionname="\"innerWall|outerWall\"", string=inner)
            self._write_section(file=file, sectionname="center", string=center)
            self._write_section(file=file, sectionname="\"zmin|zmax\"", string=zmin)
            self._write_section(file=file, sectionname="region0_to_panelRegion_panel", string=region0)

            with open(file, "a") as f:
                fin = "}\n"
                f.write(fin)

        else:
            all = "type zeroGradient;\n"

            foamfile_ = self.foamfile.format("volScalarField", "\"0/panelRegion\"", "p")
            self._write_section(file=file, sectionname="FoamFile", string=foamfile_, indentlevel=0)

            with open(file, "a") as f:
                info  = "dimensions {0:};\n\n"
                info += "internalField uniform {1:};\n\n"
                info_ = info.format(dim, P_pa)
                info_ = info_.replace(",", "")
                f.write(info_)

            with open(file, "a") as f:
                ini = "boundaryField\n{\n"
                f.write(ini)

            self._write_section(file=file, sectionname="\".*\"",  string=all)

            with open(file, "a") as f:
                fin = "}\n"
                f.write(fin)

        return None

    def make_P_rgh_file(self, file=None, P=1.0):
        """
        Make openFOAM p_rgh file.

        Args:
            file:
            P: Pressure [bar]
        """
        with open(file, "w") as f:
            f.write("")

        dim = [1, -1, -2, 0, 0, 0, 0]
        P_pa = P*1.0e5

        inlet =   "type     fixedFluxPressure;\n"
        outlet =  "type     totalPressure;\n" \
                  "p0       $internalField;\n"
        inner =   "type     fixedFluxPressure;\n"
        center =  "type     fixedFluxPressure;\n"
        zmin =    "type     symmetry;\n"
        region0 = "type     fixedFluxPressure;\n"

        foamfile_ = self.foamfile.format("volScalarField", "\"0\"", "p_rgh")
        self._write_section(file=file, sectionname="FoamFile", string=foamfile_, indentlevel=0)

        with open(file, "a") as f:
            info  = "dimensions {0:};\n\n"
            info += "internalField uniform {1:};\n\n"
            info_ = info.format(dim, P_pa)
            info_ = info_.replace(",", "")
            f.write(info_)

        with open(file, "a") as f:
            ini = "boundaryField\n{\n"
            f.write(ini)

        self._write_section(file=file, sectionname="inlet", string=inlet)
        self._write_section(file=file, sectionname="outlet", string=outlet)
        self._write_section(file=file, sectionname="\"innerWall|outerWall\"", string=inner)
        self._write_section(file=file, sectionname="center", string=center)
        self._write_section(file=file, sectionname="\"zmin|zmax\"", string=zmin)
        self._write_section(file=file, sectionname="region0_to_panelRegion_panel", string=region0)

        with open(file, "a") as f:
            fin = "}\n"
            f.write(fin)

        return None

    def make_Ydefault_file(self, file=None, is_surface=False):
        """
        Make openFOAM Ydefault file.

        Args:
            file:
            is_surface:
        """
        with open(file, "w") as f:
            f.write("")

        dim = [0] * 7
        Ydefault = 0

        if not is_surface:
            inlet =   "type       fixedValue;\n" \
                      "value      $internalField;\n"
            outlet =  "type       inletOutlet;\n" \
                      "inletValue $internalField;\n" \
                      "value      $internalField;\n"
            inner =   "type       zeroGradient;\n"
            center =  "type       zeroGradient;\n"
            zmin =    "type       symmetry;\n"
            region0 = "type       zeroGradient;\n"

            foamfile_ = self.foamfile.format("volScalarField", "\"0\"", "Ydefault")
            self._write_section(file=file, sectionname="FoamFile", string=foamfile_, indentlevel=0)

            with open(file, "a") as f:
                info = "dimensions {0:};\n\n"
                info += "internalField uniform {1:};\n\n"
                info_ = info.format(dim, Ydefault)
                info_ = info_.replace(",", "")
                f.write(info_)

            with open(file, "a") as f:
                ini = "boundaryField\n{\n"
                f.write(ini)

            self._write_section(file=file, sectionname="inlet", string=inlet)
            self._write_section(file=file, sectionname="outlet", string=outlet)
            self._write_section(file=file, sectionname="\"innerWall|outerWall\"", string=inner)
            self._write_section(file=file, sectionname="center", string=center)
            self._write_section(file=file, sectionname="\"zmin|zmax\"", string=zmin)
            self._write_section(file=file, sectionname="region0_to_panelRegion_panel", string=region0)

            with open(file, "a") as f:
                fin = "}\n"
                f.write(fin)

        else:
            top     = "type  zeroGradient;\n"
            side    = "type  empty;\n"
            region0 = "type  fixedValue;\n" \
                      "value uniform 0;\n"

            foamfile_ = self.foamfile.format("volScalarField", "\"0/panelRegion\"", "Ydefault")
            self._write_section(file=file, sectionname="FoamFile", string=foamfile_, indentlevel=0)

            with open(file, "a") as f:
                info  = "dimensions {0:};\n\n"
                info += "internalField uniform {1:};\n\n"
                info_ = info.format(dim, Ydefault)
                info_ = info_.replace(",", "")
                f.write(info_)

            with open(file, "a") as f:
                ini = "boundaryField\n{\n"
                f.write(ini)

            self._write_section(file=file, sectionname="panel_top",  string=top)
            self._write_section(file=file, sectionname="panel_side", string=side)
            self._write_section(file=file, sectionname="region0_to_panelRegion_panel", string=region0)

            with open(file, "a") as f:
                fin = "}\n"
                f.write(fin)

        return None

    def _write_section(self, file=None, sectionname=None, string=None, indentlevel=1, addsemicolon=False):
        """
        write section of openFOAM
        """
        ini   = "{0:s}\n".format(sectionname)
        ini  += "{\n"
        prefix = "    "*indentlevel
        fin   = "}\n\n" if not addsemicolon else "};\n\n"
        str   = textwrap.indent(string, prefix="    ")
        info  = ini + str + fin
        info_ = textwrap.indent(info, prefix=prefix)

        with open(file, "a") as f:
            f.write(info_)

        return None

    def make_reactionfile(self, file=None, deltaEs=None, bep_param=None, surface_atoms=None):
        """
        Make openFOAM reaction file.

        Args:
            deltaEs:
            bep_param:
            file: name of the generated openFOAM reaction file
            surface_atoms:
        """
        with open(file, "w") as f:
            f.write("")

        with open(file, "a") as f:
            if surface_atoms is not None:
                elements = list(set(surface_atoms.get_chemical_symbols()))
                elements = "".join(elements)
                f.write(self._get_elements(surface_element=elements))
                surf = list(filter(lambda x: "surf" in x, self.get_unique_species()))
                f.write(self._get_species(species=surf, surface_element=elements))
                gas = list(filter(lambda x: "surf" not in x, self.get_unique_species()))
                gas.append(self.inert)
                f.write(self._get_species(species=gas, add_gaseous=True))
                for info in self._get_openfoam_reactions(deltaEs=deltaEs, bep_param=bep_param,
                                                         surface_element=elements):
                    f.write(info)
            else:
                # currently gas-phase reaction is not supported
                f.write(self._get_elements())
                gas = list(filter(lambda x: "surf" not in x, self.get_unique_species()))
                gas.append(self.inert)
                f.write(self._get_species(species=gas))
                f.write("reactions\n{\n}\n")

    def _get_elements(self, surface_element=None):
        species = self.get_unique_species()
        species = list(filter(lambda x: "surf" not in x, species))
        species.append(self.inert)

        element_set = []
        for spe in species:
            element_set += Atoms(spe).get_chemical_symbols()

        if surface_element is not None:
            element_set.append(surface_element)

        element_set = set(element_set)

        num = len(element_set)
        ini = "elements        {0:d}(".format(num)
        fin = ");\n"
        elements = ""
        for iel, el in enumerate(element_set):
            elements += str(el) + " "
            if iel % 5 == 4:
                elements += "\n\t\t\t"

        elements = elements.rstrip()
        elements = ini + elements + fin
        return elements

    def _get_species(self, species=None, add_gaseous=False, surface_element=None):
        if add_gaseous:
            ini = "gaseousSpecies  {0:d}(".format(len(species))
        else:
            ini = "species         {0:d}(".format(len(species))
        fin   = ");\n"

        info  = ""
        if surface_element is not None:
            info += surface_element + "(S)" + " "

        for isp, sp in enumerate(species):
            sp_ = str(sp)
            if sp_ == "surf":
                continue

            if "surf" in sp_:
                info += sp_.replace("_surf", "(S)") + " "  # chemkin notation
            else:
                info += sp_ + " "

            # change line
            if isp % 5 == 4:
                info += "\n\t\t\t"

        info = info.rstrip()
        info = ini + info + fin
        return info

    def _get_openfoam_reactions(self, deltaEs=None, bep_param=None, surface_element=None):
        ini = "reactions\n{\n"
        yield ini

        for irxn, rxn in enumerate(self.reaction_list):
            # forward
            deltaE = deltaEs[irxn]
            react = rxn.get_openfoam_reaction(deltaE=deltaE, bep_param=bep_param, direction="forward")
            if surface_element is not None:
                react = react.replace("X", surface_element)
            react = textwrap.indent(react, prefix="    ")
            yield react

            # reverse
            react = rxn.get_openfoam_reaction(deltaE=deltaE, bep_param=bep_param, direction="reverse")
            if surface_element is not None:
                react = react.replace("X", surface_element)
            react = textwrap.indent(react, prefix="    ")
            yield react

        fin = "}\n"
        yield fin

    def make_thermofile(self, file=None, surface_atoms=None):
        """
        Make openFOAM thermo file.

        Args:
            file:
            surface_atoms:
        """
        with open(file, "w") as f:
            f.write("")

        species = self.get_unique_species()
        if surface_atoms is None:
            gas = list(filter(lambda x: "surf" not in x, species))
            gas.append(self.inert)
            for i in gas:
                self._add_thermo_data(species=i, file=file)
        else:
            surf     = list(filter(lambda x: "surf" in x, species))
            elements = list(set(surface_atoms.get_chemical_symbols()))
            elements = "".join(elements)
            for spe in surf:
                if spe == "surf":
                    self._add_thermo_data_puresurface(surface_element=elements, file=file)
                else:
                    spe_ = spe.replace("_surf", "")
                    self._add_thermo_data(species=spe_, surface_element=elements, file=file)

        return None

    def _add_thermo_data(self, species=None, surface_element=None, file=None):
        thermodata = "/Volumes/openfoam/therm.dat"
        datafile = open(thermodata, "r")

        # skip lines
        n_skip = 15
        for _ in range(n_skip):
            datafile.readline()

        data = []
        go = True
        while go:
            coefs = [""]*14
            for i in range(4):
                line = datafile.readline()
                if not line:
                    # reached EOF
                    go = False
                else:
                    line = line.rstrip()
                    step = 15

                    if i == 0:
                        line_ = line.replace(",", ".")
                        line_ = line_.split(" ")
                        line_ = list(filter(lambda x: x != "", line_))
                        elem  = line_[0]
                        try:
                            Tlow  = float(line_[-4])
                            Thigh = float(line_[-3])
                            Tcom  = float(line_[-2])
                        except:
                            Tlow  = float(line_[-6])
                            Thigh = float(line_[-5])
                            Tcom  = float(line_[-4])
                    else:
                        if i == 1:
                            coefs[0:5]   = line[0:step], line[step:2*step], \
                                           line[2*step:3*step], line[3*step:4*step], line[4*step:5*step]
                        elif i == 2:
                            coefs[5:10]  = line[0:step], line[step:2*step], \
                                           line[2*step:3*step], line[3*step:4*step], line[4*step:5*step]
                        elif i == 3:
                            coefs[10:15] = line[0:step], line[step:2*step], \
                                           line[2*step:3*step], line[3*step:4*step], line[4*step:5*step]

                            # transform coefs
                            coefs = list(filter(lambda x: x != "", coefs))
                            coefs = list(map(lambda x: x.replace("E ", "E+"), coefs))
                            for icoef, coef in enumerate(coefs):
                                tmp = list(coef)
                                if tmp[-4] == " ":
                                    coefs[icoef] = "0.0"
                                else:
                                    tmp[-4] = "E"
                                    coefs[icoef] = "".join(tmp)

                            coefs = list(map(lambda x: float(x), coefs))
                            tmp = {"elem": elem, "Tlow": Tlow, "Thigh": Thigh, "Tcom": Tcom, "coefs": coefs}
                            data.append(tmp)

        # writing to file
        ini = "{\n"
        fin = "}\n"
        for i in data:
            if i["elem"] == species:
                # getting information
                atoms = Atoms(species)
                Tlow  = i["Tlow"]
                Thigh = i["Thigh"]
                Tcom  = i["Tcom"]

                name = species
                if surface_element is not None:
                    name += "(S)"
                    atoms.append(surface_element)
                weight = sum(atoms.get_masses())

                with open(file, "a") as f:
                    f.write(name + "\n" + ini)

                    sec  = "specie\n" + ini
                    info = "molWeight {0:5.3f};\n".format(weight)
                    info = textwrap.indent(info, prefix="    ")
                    all  = sec + info + fin
                    all  = textwrap.indent(all, prefix="    ")
                    f.write(all)

                    if surface_element is None:
                        low  = "highCpCoeffs\t({0:})".format(i["coefs"][0:7])
                        low  = low.replace("[", "")
                        low  = low.replace("]", "")
                        low  = low.replace(",", "")
                        low += ";\n"

                        high  = "lowCpCoeffs\t({0:})".format(i["coefs"][7:14])
                        high  = high.replace("[", "")
                        high  = high.replace("]", "")
                        high  = high.replace(",", "")
                        high += ";\n"
                    else:
                        low  = "highCpCoeffs\t({0:})".format([1.0e-100, 0, 0, 0, 0, 0, 0])
                        low  = low.replace("[", "")
                        low  = low.replace("]", "")
                        low  = low.replace(",", "")
                        low += ";\n"

                        high  = "lowCpCoeffs\t({0:})".format([1.0e-100, 0, 0, 0, 0, 0, 0])
                        high  = high.replace("[", "")
                        high  = high.replace("]", "")
                        high  = high.replace(",", "")
                        high += ";\n"

                    sec   = "thermodynamics\n" + ini
                    info  = "Tlow\t{0:.3f};\nThigh\t{1:.3f};\nTcommon\t{2:.3f};\n".format(Tlow, Thigh, Tcom)
                    info += low
                    info += high
                    info  = textwrap.indent(info, prefix="    ")
                    all   = sec + info + fin
                    all   = textwrap.indent(all, prefix="    ")
                    f.write(all)

                    if surface_element is None:
                        As    = 1.67212e-6
                        Ts    = 170.672
                        info  = "As\t\t{0:8.5e};\n".format(As)
                        info += "Ts\t\t{0:7.3f};\n".format(Ts)
                    else:
                        kappa = 0.6
                        Ts    = 0.0
                        info  = "kappa\t\t{0:7.3f};\n".format(kappa)
                        info += "Ts\t\t{0:7.3f};\n".format(Ts)

                    info  = textwrap.indent(info, prefix="    ")

                    sec = "transport\n" + ini
                    all = sec + info + fin
                    all = textwrap.indent(all, prefix="    ")
                    f.write(all)

                    symbols = atoms.get_chemical_symbols()
                    counter = collections.Counter(symbols)
                    sec = "elements\n" + ini
                    info = ""
                    for j in counter.items():
                        info += "{0:} {1:};\n".format(j[0], j[1])
                    info = textwrap.indent(info, prefix="    ")
                    all  = sec + info + fin
                    all  = textwrap.indent(all, prefix="    ")
                    all += "}\n\n"  # final
                    f.write(all)

                break  # prevent multiple output
        return None

    def _add_thermo_data_puresurface(self, surface_element=None, file=None):
        # writing to file
        ini = "{\n"
        fin = "}\n"

        atoms  = Atoms(surface_element)
        name   = surface_element + "(S)"
        weight = sum(atoms.get_masses())
        Tlow, Thigh, Tcom = 200, 3000, 1000

        with open(file, "a") as f:
            f.write(name + "\n" + ini)

            sec  = "specie\n" + ini
            info = "molWeight {0:5.3f};\n".format(weight)
            info = textwrap.indent(info, prefix="    ")
            all  = sec + info + fin
            all  = textwrap.indent(all, prefix="    ")
            f.write(all)

            low  = "highCpCoeffs\t({0:})".format([1.0e-100, 0, 0, 0, 0, 0, 0])
            low  = low.replace("[", "")
            low  = low.replace("]", "")
            low  = low.replace(",", "")
            low += ";\n"

            high  = "lowCpCoeffs\t({0:})".format([1.0e-100, 0, 0, 0, 0, 0, 0])
            high  = high.replace("[", "")
            high  = high.replace("]", "")
            high  = high.replace(",", "")
            high += ";\n"

            sec   = "thermodynamics\n" + ini
            info  = "Tlow\t{0:.3f};\nThigh\t{1:.3f};\nTcommon\t{2:.3f};\n".format(Tlow, Thigh, Tcom)
            info += low
            info += high
            info  = textwrap.indent(info, prefix="    ")
            all   = sec + info + fin
            all   = textwrap.indent(all, prefix="    ")
            f.write(all)

            kappa = 0.6
            Ts    = 0.0
            info  = "kappa\t\t{0:7.3f};\n".format(kappa)
            info += "Ts\t\t{0:7.3f};\n".format(Ts)

            info  = textwrap.indent(info, prefix="    ")

            sec   = "transport\n" + ini
            all = sec + info + fin
            all = textwrap.indent(all, prefix="    ")
            f.write(all)

            symbols = atoms.get_chemical_symbols()
            counter = collections.Counter(symbols)
            sec = "elements\n" + ini
            info = ""
            for j in counter.items():
                info += "{0:} {1:};\n".format(j[0], j[1])
            info = textwrap.indent(info, prefix="    ")
            all  = sec + info + fin
            all  = textwrap.indent(all, prefix="    ")
            all += "}\n\n"  # final
            f.write(all)

        return None

    def make_thermophysicalProperties(self, file=None, gas=None, is_surface=False, sdens=1.0e-7):
        """
        Generate openFOAM thermophysicalProperties file.

        Args:
            file:
            gas: gas species (string list)
            is_surface:
            sdens: site density [mol/m^2]
        """
        with open(file, "w") as f:
            f.write("")

        if not is_surface:
            thermotype = "type            hePsiThermo;\n" \
                         "mixture         reactingMixture;\n" \
                         "transport       sutherland;\n" \
                         "thermo          janaf;\n" \
                         "energy          sensibleEnthalpy; \n" \
                         "equationOfState perfectGas;\n" \
                         "specie          specie;\n"

            foamfile_ = self.foamfile.format("dictionary", "\"constant\"", "thermophysicalProperties")
            self._write_section(file=file, sectionname="FoamFile", string=foamfile_, indentlevel=0)
            self._write_section(file=file, sectionname="thermoType", string=thermotype, indentlevel=0)

            with open(file, "a") as f:
                f.write("inertSpecie {:};\n\n".format(self.inert))

            with open(file, "a") as f:
                f.write("chemistryReader foamChemistryReader;\n")
                f.write("foamChemistryFile \"<constant>/reactions\";\n")
                f.write("foamChemistryThermoFile \"<constant>/thermo.compressibleGas\";\n")

        else:
            thermotype = "type            heSolidThermo;\n" \
                         "mixture         reactingMixture;\n" \
                         "transport       constIso;\n" \
                         "thermo          janaf;\n" \
                         "energy          sensibleEnthalpy; \n" \
                         "equationOfState perfectGas;\n" \
                         "specie          specie;\n"

            foamfile_ = self.foamfile.format("dictionary", "\"constant/panelRegion\"", "thermophysicalProperties")
            self._write_section(file=file, sectionname="FoamFile", string=foamfile_, indentlevel=0)
            self._write_section(file=file, sectionname="thermoType", string=thermotype, indentlevel=0)

            with open(file, "a") as f:
                f.write("chemistryReader foamChemistryReader;\n")
                f.write("foamChemistryFile \"<constant>/panelRegion/reactions\";\n")
                f.write("foamChemistryThermoFile \"<constant>/panelRegion/thermo.solid\";\n\n")
                f.write("siteDensity\t{0:5.3e};\n\n".format(sdens))

            gasthermo = "transport       sutherland;\n" \
                        "thermo          janaf;\n" \
                        "equationOfState perfectGas;\n" \
                        "specie          specie;\n" \
                        "energy          sensibleEnthalpy;\n"

            self._write_section(file=file, sectionname="gasThermoType", string=gasthermo, indentlevel=0)
            gas.append(self.inert)
            for spe in gas:
                self._add_thermo_data(species=spe, file=file)

        return None

    def make_fvSchemes(self, file=None):
        """
        Make openFOAM fvSchemes file.

        Args:
            file:
        """
        with open(file, "w") as f:
            f.write("")

        ddt  = "default        Euler;\n"
        grad = "default        Gauss linear;\n"
        div  = "default        none;\n" \
               "div(phi,U)     Gauss linear;\n" \
               "div(phi,K)     Gauss limitedLinear 1;\n" \
               "div(phi,k)     Gauss limitedLinear 1;\n" \
               "div(phi,Yi_h)  Gauss multivariateSelection\n"

        # set for species
        species = self.get_unique_species()
        gas = list(filter(lambda x: "surf" not in x, species))
        gas_and_inert = gas + [self.inert]

        div += "{\n"
        for i in gas_and_inert:
            div += "\t{0:s}\tlinearUpwind grad({0:s});\n".format(i)
        div += "\th\tlinearUpwind grad(h);\n"

        # set for elements of gas specpes (inert not needed)
        element_set = []
        for ispe in gas:
            element_set += Atoms(ispe).get_chemical_symbols()
        element_set = set(element_set)
        for i in element_set:
            div += "\t{0:s}\tlinearUpwind grad({0:s});\n".format(i)
        div += "};\n"

        div += "div(((rho*nuEff)*dev2(T(grad(U))))) Gauss linear;\n" \
               "div(phiU,p)   Gauss linear;\n" \
               "div(Ji,Ii_h)  Gauss upwind grad(Ii_h);\n"

        lap = "default   Gauss linear corrected;\n"
        int = "default   linear;\n"
        sn  = "default   corrected;\n"

        foamfile_ = self.foamfile.format("dictionary", "\"system\"", "fvSchemes")
        self._write_section(file=file, sectionname="FoamFile", string=foamfile_, indentlevel=0)

        self._write_section(file=file, sectionname="ddtSchemes",  string=ddt,  indentlevel=0)
        self._write_section(file=file, sectionname="gradSchemes", string=grad, indentlevel=0)
        self._write_section(file=file, sectionname="divSchemes",  string=div,  indentlevel=0)
        self._write_section(file=file, sectionname="laplacianSchemes", string=lap, indentlevel=0)
        self._write_section(file=file, sectionname="interpolationSchemes", string=int, indentlevel=0)
        self._write_section(file=file, sectionname="snGradSchemes", string=sn, indentlevel=0)

        return None

    def make_fvSolution(self, file=None):
        """
        Make openFOAM fvSolution file.

        Args:
            file:
        """
        with open(file, "w") as f:
            f.write("")

        rho =    "solver          PCG;\n" \
                 "preconditoner   DIC;\n" \
                 "tolerance       1.0e-6;\n" \
                 "relTol          0.0;\n"
        p_rgh =  "solver          PCG;\n" \
                 "preconditioner  DIC;\n" \
                 "tolerance       1.0e-5;\n" \
                 "relTol          0.01;\n"
        p_rghF = "solver          PCG;\n" \
                 "preconditioner  DIC;\n" \
                 "tolerance       1.0e-6;\n" \
                 "relTol          0.0;\n"
        Yi =     "solver          PBiCGStab;\n" \
                 "preconditioner  DILU;\n" \
                 "tolerance       1.0e-8;\n" \
                 "relTol          0.0;\n"
        U =      "solver          PBiCGStab;\n" \
                 "preconditioner  DILU;\n" \
                 "tolerance       1.0e-6;\n" \
                 "relTol          0.0;\n"
        UF =     "solver          PBiCGStab;\n" \
                 "preconditioner  DILU;\n" \
                 "tolerance       1.0e-7;\n" \
                 "relTol          0.0;\n"
        k =      "solver          PBiCGStab;\n" \
                 "preconditioner  DILU;\n" \
                 "tolerance       1.0e-8;\n" \
                 "relTol          0.0;\n"
        h =      "solver          PBiCGStab;\n" \
                 "preconditioner  DILU;\n" \
                 "tolerance       1.0e-8;\n" \
                 "relTol          0.0;\n"
        hF =     "solver          PBiCGStab;\n" \
                 "preconditioner  DILU;\n" \
                 "tolerance       1.0e-8;\n" \
                 "relTol          0.0;\n"
        Ii =     "solver          PBiCGStab;\n" \
                 "preconditioner  DILU;\n" \
                 "tolerance       1.0e-8;\n" \
                 "relTol          0.0;\n"
        G =      "solver          PCG;\n" \
                 "preconditioner  DIC;\n" \
                 "tolerance       1.0e-6;\n" \
                 "relTol          0.0;\n"

        foamfile_ = self.foamfile.format("dictionary", "\"system\"", "fvSolution")
        self._write_section(file=file, sectionname="FoamFile", string=foamfile_, indentlevel=0)

        with open(file, "a") as f:
            ini = "solvers\n{\n"
            f.write(ini)

        self._write_section(file=file, sectionname="\"rho.*\"", string=rho, addsemicolon=True)
        self._write_section(file=file, sectionname="p_rgh", string=p_rgh, addsemicolon=True)
        self._write_section(file=file, sectionname="p_rghFinal", string=p_rghF, addsemicolon=True)
        self._write_section(file=file, sectionname="Yi", string=Yi, addsemicolon=True)
        self._write_section(file=file, sectionname="U", string=U, addsemicolon=True)
        self._write_section(file=file, sectionname="UFinal", string=UF, addsemicolon=True)
        self._write_section(file=file, sectionname="k", string=k, addsemicolon=True)
        self._write_section(file=file, sectionname="h", string=h, addsemicolon=True)
        self._write_section(file=file, sectionname="hFinal", string=hF, addsemicolon=True)
        self._write_section(file=file, sectionname="Ii", string=Ii, addsemicolon=True)
        self._write_section(file=file, sectionname="G", string=G, addsemicolon=True)

        with open(file, "a") as f:
            fin = "}\n\n"
            f.write(fin)

        pimple = "momentumPredictor         yes;\n" \
                 "nOuterCorrectors          1;\n"\
                 "nCorrectors               2;\n" \
                 "nNonOrthogonalCorrectors  0;\n"
        self._write_section(file=file, sectionname="PIMPLE", string=pimple, indentlevel=0)

        eqn = "\"(U|k).*\"    0.7;\n" \
              "\"({0:s}).*\"  0.7;\n"

        species = self.get_unique_species()
        gas = list(filter(lambda x: "surf" not in x, species))

        gas_ = ""
        for i in gas:
            gas_ += i + "|"
        gas_ += "h"

        eqn_ = eqn.format(gas_)

        with open(file, "a") as f:
            ini = "relaxationFactors\n{\n"
            f.write(ini)
        self._write_section(file=file, sectionname="equations", string=eqn_)
        with open(file, "a") as f:
            fin = "}\n"
            f.write(fin)

    def make_dockercompose_file(self, file=None, dir=None):
        """
        Make docker-compose.yaml file.

        Args:
            file: filename
            dir: directory name
        """
        with open(file, "w") as f:
            f.write("")

            info  = "services:\n"
            info += "  openfoam:\n"
            info += "    image: ubuntu:18.04-softflow\n"
            info += "    volumes:\n"
            info += "      - \"{0:s}:/openfoam\"\n"
            info += "    working_dir: /openfoam\n"
            info += "    command: >\n" \
                    "      sh -c\n" \
                    "      '\n" \
                    "      . /usr/lib/openfoam/openfoam2012/etc/bashrc &&\n" \
                    "      ./Allclean\n" \
                    "      # ./Allrun\n" \
                    "      '\n\n"

        with open(file, "a") as f:
            info_ = info.format(dir)
            f.write(info_)

        return None
