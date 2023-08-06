from .reactions_base import ReactionsBase
import numpy as np

# gas constant [kJ/mol/K]
R = 8.314 * 1.0e-3
eVtokJ = 96.487


class Reactions(ReactionsBase):
    """
    Set of elementary reactions.
    Overrides the method in ReactionsBase, which is empty.
    """
    def get_reaction_energies(self):
        """
        Calculate the reaction energies (deltaEs)
        for all the elementary reactions.

        Returns:
            deltaEs: numpy array
        """
        # freeze surface here
        surface = self.freeze_surface()

        deltaEs = np.zeros(len(self.reaction_list))
        for i, reaction in enumerate(self.reaction_list):
            deltaEs[i] = reaction.get_reaction_energy(surface=surface, calculator=self._calculator,
                                                      ase_db=self._ase_db, rxn_num=i)
        return deltaEs
