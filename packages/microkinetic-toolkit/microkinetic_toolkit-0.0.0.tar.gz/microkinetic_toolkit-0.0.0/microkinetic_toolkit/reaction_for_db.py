#!/usr/bin/env python3


import re
from typing import List, Union, Tuple
from sympy import Symbol
from sympy import Expr
from ase.units import create_units
# my lib
from .reaction import Reaction

INT_NONE_TYPE = Union[int, None]
F_NONE_TYPE = Union[float, None]
N_SPECIE_TYPE = Tuple[int, str]
H_SIDE_TYPE = List[N_SPECIE_TYPE]
SPECIE_TYPE = Union[str, Symbol]
units = create_units('2014')
kB = units['_k']        # Boltzman's constant [J/K]
Nav = units['_Nav']      # Avogadro's constant [mole/mol]
amu = units['_amu']      # atomic mass unig (1.66e-27) [kg]
hplanck = units['_hplanck']  # Plank's constant (6.63e-34) [J*s]
R = kB*Nav             # R (gas constant) [J/mol/K]
# unit conversion
eVtoJ = 96.487*1.0e3
eVtokJ = 96.487
MOLECULE_DB = "molecules.json"


class ReactionForDB(Reaction):
    def __init__(self, reaction_str, reaction_id=None):
        super().__init__(reaction_str, reaction_id=None)
        self._parse_reaction_str_for_sympy()
        self._set_sympy_products()
        self._set_sympy_reactants()

    def _parse_reaction_str_for_sympy(self):
        r_tuples, p_tuples = self._get_reactans_products_for_sympy()
        self.reactants_for_sympy = r_tuples
        self.products_for_sympy = p_tuples

    def _get_reactans_products_for_sympy(self) -> Tuple:
        products = []
        for num, sp, _ in self.products:
            products.append((num, sp))
        reactants = []
        for num, sp, _ in self.reactants:
            reactants.append((num, sp))
        return reactants, products

    def _hside_to_nspli_for_sympy(self, hside_str: str) -> List[N_SPECIE_TYPE]:
        terms = hside_str.split("+")
        list_nspiecie = [self._term_to_num_spiecie_for_sympy(term)
                         for term in terms]
        return list_nspiecie

    def _term_to_num_spiecie_for_sympy(self, term: str) -> N_SPECIE_TYPE:
        term = term.strip()
        reins = re.compile("^[0-9]+")
        re_match = reins.match(term)
        if re_match is None:
            sp = term.strip()
            return (1, sp)
        else:
            num = int(re_match[0])
            sp = reins.sub("", term)
            sp = sp.strip()
            return (num, sp)

    def get_delta_e(self, e_dict: dict) -> float:
        """set_react_e.

        Args:
            e_dict (dict): e_dict
        """
        lh_E = self._sympy_reactants.subs(
            e_dict)
        rh_E = self._sympy_products.subs(
            e_dict)
        try:
            react_e = float(rh_E - lh_E)
        except TypeError:
            emes = "reactants_E and products_E can't be completely "\
                   "subsituted.\nrh_E:{}, lh_E:{}".format(rh_E, lh_E)
            raise TypeError(emes)
        return react_e

    def _set_sympy_products(self):
        sympy_products = self._get_sympy_hside(
            self.products_for_sympy)
        self._sympy_products = sympy_products

    def _set_sympy_reactants(self):
        sympy_reactants = self._get_sympy_hside(
            self.reactants_for_sympy)
        self._sympy_reactants = sympy_reactants

    def _get_sympy_hside(self,
                         list_nsp: List[N_SPECIE_TYPE]) -> Expr:
        hside_expr = 0.0
        for num, sym in list_nsp:
            spiecie = Symbol(sym)
            term = num * spiecie
            hside_expr = hside_expr + term
        return hside_expr
