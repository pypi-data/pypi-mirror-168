from variaotional_algorithm import VariationalAlgorithm
import scipy.linalg as la
import numpy as np
import scipy.optimize as opt


class QAOA(VariationalAlgorithm):
    """Quantum Alternating Optimization Algorithms
    """

    def __init__(self, physics_system, p):
        self._name = 'QAOA'
        self.physics_system = physics_system
        self._extract_physics_system()
        self.p = p
        self.ham_pool_length = 2
        self.variational_ansatz = self._gen_qaoa(p)
        self._pre_process()
        self.params = None

    def _gen_qaoa(self):
        """generate the qaoa ansatz
        """
        return tuple([0, 1] * self.p)

    def _extract_physics_system(self):
        """Extract the variables from the physics system.
        """
        self.L = self.physics_system.L
        self.basis = self.physics_system.basis

        self.psi_initial = self.physics_system.psi_initial
        self.psi_target = self.physics_system.psi_target
        self.psi_target_conjugate_transpose = self.psi_target.conjugate().transpose()
        self.H_target = self.physics_system.H_target
        self.H_dict = self.physics_system.H_dict
        self.sym_dict = self.physics_system.sym_dict


    def _pre_process(self):
        """Pre-process the Hamiltonian for the Hamiltonian class.

        precomputing: eigen-decompose the matrix 
        """
        self.H_eval_list = list()
        self.H_evec_list = list()
        self.H_evec_conj_t_list = list()
        self.H_norm_list = list()
        self.H_evec_ij_list = list()

        assert len(self.H_dict) >= self.ham_pool_length, "There is not many hamiltonians to match the length of the Hamiltonian pool"

        for i in range(self.ham_pool_length):
            ham = self.H_dict[i]
            H_eval, H_evec = la.eigh(ham)
            H_eval = np.expand_dims(H_eval, axis=-1)

            self.H_eval_list.append( (self.imag_unit * H_eval).copy() )
            self.H_evec_list.append( H_evec )
            self.H_evec_conj_t_list.append( H_evec.conj().T.copy() )
            self.H_norm_list.append( np.linalg.norm(H_eval) )

        for i in range(self.ham_pool_length):
            sub_H_evec_ij_list = list()
            for j in range(self.ham_pool_length):
                sub_H_evec_ij_list.append(np.matmul(
                    self.H_evec_conj_t_list[i], self.H_evec_list[j]
                ))
                
            self.H_evec_ij_dict.append( sub_H_evec_ij_list )

    def evolve(self, params):
        """Evolve the system with the given parameters.
        """
        u = np.copy(self.psi_initial)
        np.matmul(self.H_evec_conj_t_dict[self.variational_ansatz[0]], u, out=u)
        np.multiply(np.exp(-params[0] * self.H_eval_dict[self.variational_ansatz[0]]), u, out=u)

        for i in range(2 * self.p - 1):
            pt_i = self.variational_ansatz[i]
            pt_ip1 = self.variational_ansatz[i + 1]
            np.matmul(self.H_evec_ij_dict[pt_ip1][pt_i], u, out=u)
            np.multiply(np.exp(-params[i + 1] * self.H_eval_dict[pt_ip1]), u, out=u)

        np.matmul(self.H_evec_dict[pt_ip1], u, out=u)
        return u

    def _compute_fidelity(self, u):
        """Compute the fidelity between the target state and the evolved state.
        """
        return np.absolute(np.matmul(self.psi_target_conjugate_transpose, u)[0, 0]) ** 2

    def fidelity(self, params):
        """Compute the fidelity between the target state and the evolved state.
        """
        u = self.evolve(params)
        return self._compute_fidelity(u)

    def _compute_expected_energy(self, u):
        """Compute the expected energy of the evolved state.
        """
        return np.real(self.H_target.expt_value(u)) / self.L

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