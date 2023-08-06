from optimizer import optimizer

import math
import numpy as np
import scipy.linalg as la
import scipy.optimize as opt


class ScipyOptimizer(optimizer):
    """Solver class for VQA model.
    
    The solver wraps the scipy optimizer.
    """
    def __init__(self, variational_ansatz, optimizer, **kwargs):
        """Initialize the solver.
        
        Args:
            variational_ansatz (variational_ansatz): the variational ansatz.
            optimizer (str): the name of the optimizer.
            **kwargs: the arguments of the optimizer.
        """
        self.variational_ansatz = variational_ansatz
        self.optimizer = optimizer
        self.kwargs = kwargs

    def optimize(self):
        """Optimize the variational ansatz.
        """
        # TODO (jimmy): add more options for the contraints.
        sol = self._solve(self.variational_ansatz.get_reward)
        return self.variational_ansatz.get_reward(sol.x), sol.x

    def _solve(self, func, x0, bounds=None, constraints=None, **kwargs):
        """Solve the optimization problem.
        
        Args:
            func (callable): the objective function.
            x0 (np.ndarray): the initial guess.
            bounds (list): the bounds of the parameters.
            constraints (list): the constraints of the parameters.
            **kwargs: the arguments of the optimizer.
        """
        if self.optimizer == 'L-BFGS-B':
            return opt.minimize(func, x0, method=self.optimizer, jac=True, bounds=bounds, constraints=constraints, **kwargs)
        elif self.optimizer == 'SLSQP':
            return opt.minimize(func, x0, method=self.optimizer, jac=True, bounds=bounds, constraints=constraints, **kwargs)
        elif self.optimizer == 'COBYLA':
            return opt.minimize(func, x0, method=self.optimizer, constraints=constraints, **kwargs)
        elif self.optimizer == 'Nelder-Mead':
            return opt.minimize(func, x0, method=self.optimizer, **kwargs)
        elif self.optimizer == 'Powell':
            return opt.minimize(func, x0, method=self.optimizer, **kwargs)
        elif self.optimizer == 'CG':
            return opt.minimize(func, x0, method=self.optimizer, **kwargs)
        elif self.optimizer == 'BFGS':
            return opt.minimize(func, x0, method=self.optimizer, **kwargs)
        elif self.optimizer == 'Newton-CG':
            return opt.minimize(func, x0, method=self.optimizer, jac=True, hess=True, **kwargs)
        elif self.optimizer == 'trust-constr':
            return opt.minimize(func, x0, method=self.optimizer, jac=True, hess=la.inv, bounds=bounds, constraints=constraints, **kwargs)
        elif self.optimizer == 'dogleg':
            return opt.minimize(func, x0, method=self.optimizer, jac=True, hess=la.inv, **kwargs)
        elif self.optimizer == 'trust-ncg':
            return opt.minimize(func, x0, method=self.optimizer, jac=True, hesse=la.inv, **kwargs)
        elif self.optimizer == 'trust-exact':
            return opt.minimize(func, x0, method=self.optimizer, jac=True, hess=la.inv, **kwargs)
        elif self.optimizer == 'trust-krylov':
            return opt.minimize(func, x0, method=self.optimizer, jac=True, hess=la.inv, **kwargs)
        else:
            raise ValueError('Unknown optimizer: {}'.format(self.optimizer))
    


    