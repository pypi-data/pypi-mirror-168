from qaoa import QAOA
import scipy.linalg as la
import numpy as np
import scipy.optimize as opt


class VQITE(QAOA):
    """Variational QITE ansatz

    Use the QITE ansatz to solve the optimization problem. Here, the ansatz is the complete;
    As opposed to the compact ansatz, which is a low rank approximation the complete ansatz.
    """

    def __init__(self, physics_system, q, ham_pool_length, N_c):
        self._name = 'v-QITE'
        self.physics_system = physics_system
        self._extract_physics_system()
        self.q = q
        self.ham_pool_length = ham_pool_length
        self._pre_process()
        self.params = None
    
    def generate_ham_pool(self):
        """Generate the pool of hamiltonians.
        """
        # self.H_pool = []
        # for i in range(self.ham_pool_length):
        #     self.H_pool.append(self._generate_random_hamiltonian())

        # hamiltonian pool 
        self.ham_pool = []

    def evolve(self, params):
        """Evolve the system with the given parameters.

        Args:
            variational_ansatz (tuple): the ordering of the hamiltonians
            params (np.ndarray): the parameters of the variational ansatz.
        """
        u = np.copy(self.psi_initial)

        assert len(params) % self.ham_pool_length == 0, "The number of parameters should be the multiple of hamiltonian pool length."
        N_q = len(params) // self.ham_pool_length
        
        for i in range(N_q):
            mat = sum([ c * h for c, h in zip(params[i * self.ham_pool_length: (i + 1) * self.ham_pool_length], self.ham_pool)])
            expmat = la.expm(-1j * mat)
            u = np.dot(expmat, u)
        return u

    def fidelity(self, params):
        """Compute the fidelity between the target state and the evolved state.
        """
        u = self.evolve(params)
        return self._compute_fidelity(u)

    def expected_energy(self, params):
        """Compute the expected energy of the evolved state.
        """
        u = self.evolve(params)
        return self._compute_expected_energy(u)

    def get_reward(self, params, reward_type='fidelity'):
        """Compute the reward of the evolved state.
        """
        if reward_type == 'fidelity':
            return self.fidelity(params)
        elif reward_type == 'energy':
            return - self.expected_energy(params)
        else:
            raise NotImplementedError("The reward type is not supported.")

    # TODO: add the noise reward (maybe to the noise module, which is supposed to add more method to the class)

    @property
    def name(self):
        return self._name