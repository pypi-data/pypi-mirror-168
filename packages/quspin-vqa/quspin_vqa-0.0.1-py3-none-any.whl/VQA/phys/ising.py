from physics_system import PhysicsSystem
from quspin.basis import spin_basis_1d
from quspin.operators import hamiltonian
import numpy as np

class Ising(PhysicsSystem):
    """
    Returns the Hamiltonian of the Ising model.

    The Ising model is specified as Ising spin-1/2 model and uses 
    the spin-1/2 operators. We use the symmetries of pblock=1 and
    kblock=0 to reduce the Hilbert space dimension.
    """
    def __init__(self, L, J=1, h_x=0.4045, h_z=0.45225, bc='pbc'):
        """Initialize the Ising Hamiltonian class. 

        the default configuration for the trasverse ising model
        J, h_x, h_z = 1, 0.4045, 0.45225
        
        Hamiltonian:
        H = -J \sum_{<i,j>} S_i^z S_j^z - h_x \sum_i S_i^x - h_z \sum_i S_i^z

        Args:
            L (int): The number of spins.
            J (float): The coupling constant.
            h_x (float): The transverse field.
            h_z (float): The longitudinal field.
            bc (str): The boundary condition. 'pbc' or 'obc'.
        """

        self.L = L
        self.J = J
        self.h_x = h_x
        self.h_z = h_z

        # compute Hilbert space basis
        basis = spin_basis_1d(L=L, pauli=0, pblock=1, kblock=0)

        # initial state
        psi_initial = np.zeros(basis.Ns)
        psi_initial[basis.index(int("1" * L, 2))] = 1

        if bc == 'pbc':
            # define operators
            zz_term = [[1.0, i, (i + 1) % L] for i in range(L)]
            z_term = [[1.0, i] for i in range(L)]
        else:
            raise NotImplementedError("Only PBC is implemented.")


        # compute operator string lists
        static_zz = [["zz", zz_term]]
        static_z = [["z", z_term]]
        static_x = [["x", z_term]]
        static_y = [["y", z_term]]
        static_yz = [["yz", zz_term], ["zy", zz_term]]
        static_yx = [["yx", zz_term], ["xy", zz_term]]

        H_zz = hamiltonian(static_zz, [], basis=basis, dtype=np.float64)
        H_z = hamiltonian(static_z, [], basis=basis, dtype=np.float64)
        H_x = hamiltonian(static_x, [], basis=basis, dtype=np.float64)
        H_y = hamiltonian(static_y, [], basis=basis, dtype=np.complex64)
        H_yz = hamiltonian(static_yz, [], basis=basis, dtype=np.complex64)
        H_yx = hamiltonian(static_yx, [], basis=basis, dtype=np.complex64)

        H_1 = J * H_zz + h_z * H_z
        H_2 = h_x * H_x

        H_target = H_1 + H_2

        # target state
        E_GS, psi_target = H_target.eigsh(k=1, which="SA")

        print("ground state energy per spin: ", E_GS / L)

        psi_initial = psi_initial.reshape((-1,))
        psi_target = psi_target.reshape((-1,))

        self.psi_intial = psi_initial.astype(complex)
        self.psi_target = psi_target.astype(complex)
        self.H_target = H_target
        self.E_GS = E_GS

        H_1 = H_1.toarray()
        H_2 = H_2.toarray()
        H_y = H_y.toarray()
        H_yz = H_yz.toarray()
        H_yx = H_yx.toarray()

        self.H_dict = {
            int("0"): H_1,
            int("1"): H_2,
            int("2"): H_y,
            int("3"): H_yz,
            int("4"): H_yx,
        }

        self.sym_dict = {
            0: "Z|Z + Z",
            1: "X",
            2: "Y",
            3: "Y|Z",
            4: "X|Y",
        }
    
    @property
    def hamiltonian(self):
        return self.H_target
    
    @property
    def ground_state_energy(self):
        return self.E_GS
    
    @property
    def initial_state(self):
        return self.psi_intial
    
    @property
    def target_state(self):
        return self.psi_target
