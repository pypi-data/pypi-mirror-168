#!/usr/bin/env python3

# formal lib
import numpy as np
import pandas as pd
import warnings
from ase.db import connect
from typing import List
from ase.db.row import AtomsRow
# my lib
from .reaction_for_db import ReactionForDB
from .reactions_base import ReactionsBase
from .dump_json import PropertyDumpMixin

# gas constant [kJ/mol/K]
R = 8.314 * 1.0e-3
eVtokJ = 96.487
VIBZERO_KEY = "vib_zero_e"


class ReactionsForDB(ReactionsBase, PropertyDumpMixin):
    """
    Set of elementary reactions.
    Overrides the method in ReactionsBase, which is empty.
    """
    @property
    def ase_db(self):
        return self._ase_db

    @ase_db.setter
    def ase_db(self, db_str: str):
        self._ase_db = db_str

    @property
    def uniq_species(self):
        if not hasattr(self, "_tot_uniq_species"):
            self._tot_uniq_species = self.get_unique_species()
        return self._tot_uniq_species

    @property
    def react_e_dict(self):
        if not hasattr(self, "_react_e_dict"):
            w_mes = "set react_e_dict by default state_key and select_key.\n"\
                    "state_key: chem_react_symbol, select_key: add_vib."
            warnings.warn(w_mes)
            self.set_react_e_dict_from_asedb()
        return self._react_e_dict

    def set_react_e_dict_from_asedb(self,
                                    state_key: str = "chem_react_symbol",
                                    select_key: str = "add_vib"):
        assert hasattr(self, "_ase_db")
        # invalid log list.
        self._invalid_chemstr_list = []
        e_dict = {}
        self._state_key = state_key
        self._select_key = select_key
        for uniq_sym in self.uniq_species:
            query_dict = {}
            query_dict[self._state_key] = str(uniq_sym)
            query_dict[self._select_key] = True
            rows_list = list(connect(self._ase_db).select(**query_dict))

            if len(rows_list) == 1:
                row = rows_list[0]
                E = row.energy
                if self.vibE_option:
                    zero_vE = self._get_zero_vib_e_from_row(row)
                    E = E + zero_vE
            elif len(rows_list) == 0:
                self._invalid_chemstr_list.append(uniq_sym)
                wmes = "invalid uniq_sym in asedb: {}".format(uniq_sym)
                warnings.warn(wmes)
                raise AssertionError(wmes)
            else:
                raise NotImplementedError("")
            e_dict[uniq_sym] = E
        self._react_e_dict = e_dict
        self.show_react_e_status()

    def _get_zero_vib_e_from_row(self, row: AtomsRow) -> float:
        zib_e = row.data[VIBZERO_KEY]
        return zib_e

    def show_react_e_status(self):
        if self.vibE_option:
            print("E including zero point energy.")
        else:
            print("E is simple Energy.")

    @property
    def vibE_option(self) -> bool:
        if hasattr(self, "_vibE_option"):
            return self._vibE_option
        else:
            return False

    def set_vibE_option(self, vibE_option: bool):
        self._vibE_option = vibE_option

    @property
    def invalid_chemstr_list(self) -> List[str]:
        return self._invalid_chemstr_list

    def get_reaction_energies(self) -> np.ndarray:
        """
        get the reaction energies (deltaEs) for asedb.

        Returns:
            deltaEs: numpy array
        """
        assert hasattr(self, "_ase_db")
        deltaEs = np.zeros(len(self.reaction_list))
        for i, reaction in enumerate(self.reaction_list):
            assert isinstance(reaction, ReactionForDB)
            deltaEs[i] = reaction.get_delta_e(self.react_e_dict)
        return deltaEs

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
            reaction = ReactionForDB.from_dict(ddict)
            reaction_list.append(reaction)
        ReactionForDB.id_iterator.reset()
        return cls(reaction_list)
