from qaoa import QAOA
import scipy.linalg as la
import numpy as np
import scipy.optimize as opt


class GQAOA(QAOA):
    """Generalized Quantum Alternating Optimization Algorithms
    """

    def __init__(self, physics_system, q, ham_pool_length):
        self._name = 'g-QAOA'
        self.physics_system = physics_system
        self._extract_physics_system()
        self.q = q
        self.ham_pool_length = ham_pool_length
        self._pre_process()
        self.params = None

    def evolve(self, variational_ansatz, params):
        """Evolve the system with the given parameters.

        Args:
            variational_ansatz (tuple): the ordering of the hamiltonians
            params (np.ndarray): the parameters of the variational ansatz.
        """
        u = np.copy(self.psi_initial)
        np.matmul(self.H_evec_conj_t_dict[variational_ansatz[0]], u, out=u)
        np.multiply(np.exp(-params[0] * self.H_eval_dict[variational_ansatz[0]]), u, out=u)

        for i in range(2 * self.p - 1):
            pt_i = variational_ansatz[i]
            pt_ip1 = variational_ansatz[i + 1]
            np.matmul(self.H_evec_ij_dict[pt_ip1][pt_i], u, out=u)
            np.multiply(np.exp(-params[i + 1] * self.H_eval_dict[pt_ip1]), u, out=u)

        np.matmul(self.H_evec_dict[pt_ip1], u, out=u)
        return u

    def fidelity(self, variational_ansatz, params):
        """Compute the fidelity between the target state and the evolved state.
        """
        u = self.evolve(variational_ansatz, params)
        return self._compute_fidelity(u)

    def expected_energy(self, variational_ansatz, params):
        """Compute the expected energy of the evolved state.
        """
        u = self.evolve(variational_ansatz, params)
        return self._compute_expected_energy(u)

    def get_reward(self, variational_ansatz, params, reward_type='fidelity'):
        """Compute the reward of the evolved state.
        """
        if reward_type == 'fidelity':
            return self.fidelity(variational_ansatz, params)
        elif reward_type == 'energy':
            return - self.expected_energy(variational_ansatz, params)
        else:
            raise NotImplementedError("The reward type is not supported.")

    # TODO: add the noise reward (maybe to the noise module, which is supposed to add more method to the class)

    @property
    def name(self):
        return self._name