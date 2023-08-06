from .dft import orth
from .energies import get_Eewald
from .minimizer import sd
from .operators import PWBasis
from .potentials import coulomb
from .utils import pseudo_uniform


class SCF:
    '''SCF class to handle direct minimizations.'''

    def __init__(self, atoms):
        self.atoms = atoms
        self.op = PWBasis(atoms)
        self.pot = coulomb(self.atoms, self.op)
        self._init_W()

    def run(self, Nit=1001, etol=1e-6):
        '''Run the self-consistent field (SCF) calculation.'''
        self.Eewald = get_Eewald(self.atoms)
        return sd(self, Nit, etol)

    def _init_W(self, seed=1234):
        '''Generate random initial-guess coefficients as starting values.
        Thesis: List. 3.18
        '''
        W = pseudo_uniform((len(self.atoms.G2c), self.atoms.Nstate), seed)
        self.W = orth(self.atoms, self.op, W)
