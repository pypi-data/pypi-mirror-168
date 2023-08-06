import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

from mloptm.utils import EvalExpr
from mloptm.methods import Golden
from mloptm.exceptions import NotOptimizedError


class GradientMethod:
    @property
    def minima(self):
        return self._minima

    @minima.setter
    def minima(self, val):
        raise ValueError("minima cannot be set. only calculated")

    def PlotError(self, **kw):
        """
        Generate a Line Plot of the Errors.

        Parameters
        ----------
         - **kw : 

        Returns
        -------
         - fig (plt.Figure) : the figure created.

        Raises
        ------
         - NotOptimizedError
        """

        if self.minima is None:
            raise NotOptimizedError("function did not minimized yet.")

        iterations = range(1, self.errors.shape[0]+1)
        
        fig, ax = plt.subplots(nrows=1, figsize=(10, 6))
        ax.plot(iterations, self.errors, marker="o", color="k",
                markerfacecolor="w", markeredgecolor="k", markersize=8, linewidth=2.)
        ax.set_title(f"Error Over Iterations using {type(self).__name__}", fontsize=15)
        ax.set_xlabel("Iterations", fontsize=15)
        ax.set_ylabel(r"$ \frac{|X^{k+1} - X^k|}{\max(1, |X^k|)} $", fontsize=16)
        ax.set_xticks(iterations)

        plt.show()

        if kw.get("save", None) and kw.get("filename", None):
            fig.savefig(kw.get("filename"), dpi=200)

        return fig

    def PlotContour(self, xdomain, ydomain, contours=60, alpha=1.0, **kw):
        """
        Generate a Contour Plot of the Function and Plot the Steps on it.

        Parameters
        ----------
         - xdomain (list) : the lower and upper bound in the x axis.
         - ydomain (list) : the lower and upper bound in the y axis.
         - **kw : 

        Returns
        -------
         - fig (plt.Figure) : the figure created.

        Raises
        ------
         - NotOptimizedError
         - ValueError
        """


        if self.minima is None:
            raise NotOptimizedError("function did not minimized yet.")

        if len(self.symbols) != 2:
            raise ValueError("Can only be used to 3D systems, where symbols are just 2.")

        self.x_steps = self.steps[:, 0]
        self.y_steps = self.steps[:, 1]

        xmid, ymid = self.x0

        xs = np.linspace( *xdomain, 500 )
        ys = np.linspace( *ydomain, 500 )

        xx, yy = np.meshgrid(xs, ys)
        zz = self.expr_lambda([xx, yy])

        fig, ax = plt.subplots(nrows=1, figsize=(9, 7))
        cs = ax.contour(xx, yy, zz, cmap="viridis", alpha=alpha, levels=contours)
        ax.plot(self.x_steps, self.y_steps, marker="o", color="k",
                markerfacecolor="w", markeredgecolor="k", markersize=7, linewidth=1.5)
        ax.plot(self.x_steps[-1], self.y_steps[-1], marker="o", markerfacecolor="r",
                markeredgecolor="k", markersize=15, alpha=0.4)
        ax.set_title(f"Minimization using {type(self).__name__}")
        ax.set_xlabel(self.symbols[0])
        ax.set_ylabel(self.symbols[1])
        cbar = plt.colorbar(cs)
        cbar.ax.set_ylabel("Z Values")
        # ax.axis("square")

        plt.show()

        if kw.get("save", None) and kw.get("filename", None):
            fig.savefig(kw.get("filename"), dpi=200)

        return fig

    def Plot3D(self, xdomain, ydomain, contours=60, alpha=0.2, **kw):
        """
        Generate a 3D Plot of the Function and Plot the Steps on it.

        Parameters
        ----------
         - xdomain (list) : the lower and upper bound in the x axis.
         - ydomain (list) : the lower and upper bound in the y axis.
         - **kw : 

        Returns
        -------
         - fig (plt.Figure) : the figure created.

        Raises
        ------
         - NotOptimizedError
         - ValueError
        """

        if self.minima is None:
            raise NotOptimizedError("function did not minimized yet.")

        if len(self.symbols) != 2:
            raise ValueError("Can only be used to 3D systems, where symbols are just 2.")

        self.x_steps = self.steps[:, 0]
        self.y_steps = self.steps[:, 1]

        xmid, ymid = self.x0

        xs = np.linspace( *xdomain, 200 )
        ys = np.linspace( *ydomain, 200 )

        xx, yy = np.meshgrid(xs, ys)
        zz = self.expr_lambda([xx, yy])

        fig = plt.figure(figsize=(9, 7))
        ax = fig.add_subplot(projection="3d")

        surf = ax.plot_surface(xx, yy, zz, cstride=3, rstride=3, cmap="coolwarm", alpha=alpha)
        
        ax.contour(xx, yy, zz, zdir='z', offset=np.min(zz), alpha=alpha, levels=contours, cmap="coolwarm")

        ax.plot(self.x_steps, self.y_steps, np.min(zz), marker="o", color="k",
                markerfacecolor="w", markeredgecolor="k", markersize=7, linewidth=1.5)

        ax.plot3D(self.x_steps[-1], self.y_steps[-1], self.expr_lambda([self.x_steps[-1], self.y_steps[-1]]), 
                marker="o", markerfacecolor="r", markeredgecolor="k", markersize=15, alpha=0.4)

        ax.plot(self.x_steps, self.y_steps, self.expr_lambda([self.x_steps, self.y_steps]), marker="o",
                color="k", markerfacecolor="w", markeredgecolor="k", markersize=7, linewidth=1.5)

        ax.set_title(f"Minimization using {type(self).__name__}")
        ax.set_xlabel(self.symbols[0])
        ax.set_ylabel(self.symbols[1])
        ax.set_zlabel(f"f({self.symbols[0]},{self.symbols[1]})")

        plt.show()

        if kw.get("save", None) and kw.get("filename", None):
            fig.savefig(kw.get("filename"), dpi=200)

        return fig



class SteepestDescent(GradientMethod):
    """
    Steepeset Descent Minimizing Algorithm Implemenetation in Python

    Attrs
    -----
     - f (str) : string representation of the function to minimize
     - variables (list): list of the variables used in the function.
     - maxiters (int): maximum number of iterations to run if we fail to converge.
     - minima (list) : list of the minimum value for each variable.
     - steps (list) : list of each step make in the minimizing process
     - errors (list) : list of the errors at each step made.

    Methods
    -------
     - Minimize
     - PlotError
     - PlotContour
     - Plot3D
     - _HessianMatrix

    Examples
    --------
    >>> from mloptm.grads import SteepestDescent

    >>> f = "cos(x^2 - 3*y) + sin(x^2 + y^2)"
    >>> steepest = SteepestDescent(f=f, variables=("x", "y"))
    >>> minima = steepest.Minimize(x0=(1, 1), eps=1e-7, verbose=True)
    Running with Tolerance of [0.0000001000] for Max Iterations of [50]
    Error at Iter [  1] = 0.424159602445
    Error at Iter [  2] = 0.300241800580
    Error at Iter [  3] = 0.020752222087
    Error at Iter [  4] = 0.003268755730
    Error at Iter [  5] = 0.000366715852
    Error at Iter [  6] = 0.000049562070
    Error at Iter [  7] = 0.000005521282
    Error at Iter [  8] = 0.000000746351

    >>> minima
    ... array([[1.37638495],
    ...        [1.67867607]])

    >>> fig = steepest.PlotError(save=True, filename="errors.jpg")
    >>> steepest.PlotContour(xdomain=(-3, 3), ydomain=(-3, 3), save=True, filename="contour.jpg")
    >>> steepest.Plot3D(xdomain=(-3, 3), ydomain=(-3, 3), save=True, filename="3d.jpg")


    >>> from mloptm.grads import SteepestDescent

    >>> f = "x1^2 + x2^2 + x3^2 + x4^2"
    >>> steepest = SteepestDescent(f=f, variables=("x1", "x2", "x3", "x4"))
    >>> minima = steepest.Minimize(x0=(10, 10, 10, 10), eps=1e-7, verbose=False)

    >>> minima
    ... array([[-1.18032373e-16],
    ...        [-1.18032373e-16],
    ...        [-1.18032373e-16],
    ...        [-1.18032373e-16]]

    >>> fig = steepest.PlotError(save=True, filename="errors.jpg")
    """

    def __init__(self, f, variables, maxiters=50):
        self.f = f
        self.variables = variables
        self.maxiters = maxiters

        self.expr, self.symbols = EvalExpr(self.f, self.variables)
        self.expr_lambda = sp.lambdify([self.symbols], self.expr)

        self.errors = []
        self.steps = []
        self._minima = None


    def Minimize(self, x0, eps=1e-7, verbose=True):
        """
        Actual Minimization Implementation of the Steepest Descent Method.
        
        Parameters
        ----------
         - x0 (list) : the initial point of the minimizing process
         - eps (float) : the tolerance to compare to the error from the minimizing process.
         - verbose (bool) : whether to print information about each step or not.

        Rerturns
        --------
         - minima (list) : the minimum value of the function after the minimizing process.
        """

        self.errors = []
        self.steps = []
        self._minima = None

        self.x0 = x0

        ## define the alpha
        alpha = sp.Symbol("alpha", positive=True)
        
        ## compute the gradient and convert to matrix
        grad = sp.Matrix( [self.expr.diff(v).n() for v in self.symbols] ).n()
        
        ## convert initial point to Matrix
        X0 = sp.Matrix(x0)
        self.steps.append(np.array(X0.T.tolist()[0], dtype=np.float64))

        ## evaulate the alpha expression
        alpha_evaluated = (X0 - alpha * grad).subs([ (var, val) for var, val in zip(self.symbols, x0) ]).n()

        ## create a lambda function of the alpha expr to minimze it.
        alpha_lambda = sp.lambdify([alpha], self.expr.subs(
                                    [ (var, val) for var, val in 
                                     zip(self.symbols, alpha_evaluated) ]).n())

        ## get the mimimum value of the alpha to get the larget step to take.
        minimum_alpha = Golden(alpha_lambda).Minimize(a0=-1, b0=1, eps=1e-6)

        ## calculate the next point.
        xk = (X0 - minimum_alpha * grad).subs([ (var, val) for var, val in zip(self.symbols, X0) ]).n()

        ## calculate the error between the last and next values.
        err = ((xk - X0).norm().n() / np.maximum(1, X0.norm().n())).n()

        ## append the results of both err and step to errors and steps.
        self.errors.append(err)
        self.steps.append(np.array(xk.T.tolist()[0], dtype=np.float64))

        if verbose:
            print("Running with Tolerance of [{:.10f}] for Max Iterations of [{}]".format(eps, self.maxiters))

        for _ in range(self.maxiters):
            
            self.steps.append(np.array(xk.T.tolist()[0], dtype=np.float64))
            
            alpha_evaluated = (X0 - alpha * grad).subs([ (var, val) for var, val in zip(self.symbols, X0) ]).n()
            dummy = self.expr.subs([ (var, val) for var, val in zip(self.symbols, alpha_evaluated) ]).n()

            alpha_lambda = sp.lambdify([alpha], dummy, modules="numpy")

            minimum_alpha = Golden(alpha_lambda).Minimize(a0=-1, b0=1, eps=1e-5)

            xk = (X0 - minimum_alpha * grad).subs([ (var, val) for var, val in zip(self.symbols, X0) ]).n()
            
            err = (xk - X0).norm().n() / np.maximum(1, X0.norm().n())

            self.errors.append(err)
            
            if err < eps: break

            if verbose:
                print("Error at Iter [{:>3d}] = {:.12f}".format(_+1, err))
            
            X0 = xk

        ## convert the lists to numpy arrays
        self._minima = np.array(xk.n().tolist(), dtype=np.float64)
        self.steps  = np.array(self.steps, dtype=np.float64)
        self.errors = np.array(self.errors, dtype=np.float64)

        return self._minima


class NewtonND(GradientMethod):
    """
    Newton Gradient Method Minimizing Algorithm Implemenetation in Python

    Attrs
    -----
     - f (str) : string representation of the function to minimize
     - variables (list): list of the variables used in the function.
     - maxiters (int): maximum number of iterations to run if we fail to converge.
     - minima (list) : list of the minimum value for each variable.
     - steps (list) : list of each step make in the minimizing process
     - errors (list) : list of the errors at each step made.

    Methods
    -------
     - Minimize
     - PlotError
     - PlotContour
     - Plot3D

    Examples
    --------
    >>> from mloptm.grads import NewtonND

    >>> f = "x^2 + y^2 + z^2"
    >>> nm = NewtonND(f=f, variables=("x", "y"))
    >>> minima = nm.Minimize(x0=(1, 1), eps=1e-7, verbose=True)
    Running with Tolerance of [0.0000001000] for Max Iterations of [50]
    Error at Iter [  1] = [1.000000000000000000]
    Error at Iter [  2] = [0.000000000000000000]

    >>> minima
    ... array([[0.],
    ... [0.],
    ... [0.]])

    >>> fig = nm.PlotError(save=True, filename="errors.jpg")

    """
    def __init__(self, f, variables, maxiters=50):

        self.f = f
        self.variables = variables
        self.maxiters = maxiters

        self.expr, self.symbols = EvalExpr(self.f, self.variables)
        self.expr_lambda = sp.lambdify([self.symbols], self.expr)

    def Minimize(self, x0, eps=1e-7, verbose=False):
        """
        Actual Minimization Implementation of the Newton Method.
        
        Parameters
        ----------
         - x0 (list) : the initial point of the minimizing process
         - eps (float) : the tolerance to compare to the error from the minimizing process.
         - verbose (bool) : whether to print information about each step or not.

        Rerturns
        --------
         - minima (list) : the minimum value of the function after the minimizing process.
        """


        self.errors = []
        self.steps = []
        self._minima = None

        self.x0 = x0

        ## convert x0 to sympy matrix
        X0 = sp.Matrix(x0).n()
        self.steps.append(np.array(X0.T.tolist()[0], dtype=np.float64))

        ## compute the gradient and convert to matrix
        grad = sp.Matrix( [self.expr.diff(v) for v in self.symbols] ).n()
        grad_num = grad.subs([(var, val) for var, val in zip(self.symbols, x0)]).n()

        ## create the hessain matrix
        hessian = self._HessianMatrix(grad, self.symbols)
        hessian_num = hessian.subs( [(var, val) for var, val in zip(self.symbols, x0)] ).n()
        hessian_inv = hessian_num.inv().n()

        xk = X0 - hessian_inv * grad_num

        for _ in range(self.maxiters):

            grad = sp.Matrix( [self.expr.diff(v) for v in self.symbols] ).n()
            grad_num = grad.subs([(var, val) for var, val in zip(self.symbols, X0)]).n()

            hessian = self._HessianMatrix(grad, self.symbols).n()
            hessian_num = hessian.subs( [(var, val) for var, val in zip(self.symbols, X0)] ).n()
            hessian_inv = hessian_num.inv().n()

            xk = (X0 - hessian_inv * grad_num).n()

            self.steps.append(np.array(xk.T.tolist()[0], dtype=np.float64))

            err = (xk - X0).norm().n() / np.maximum(1, X0.norm().n())
            self.errors.append(err)
 
            if verbose:
                print("Error at Iter [{:>3d}] = [{:.18f}]".format(_+1, float(err)))

            if err < eps: break

            X0  = xk

        self._minima = np.array(xk.tolist(), dtype=np.float64)
        self.errors = np.array(self.errors, dtype=np.float64)
        self.steps = np.array(self.steps, dtype=np.float64)

        return self.minima

    def _HessianMatrix(self, grad, variables):
        """
        Method to Compute the Hessian Matrix.

        Parameters
        ----------
         - grad (sp.Matrix) : the gradient of the function to minimize.
         - variables (list) : list of the variables in of the function.

        Returns
        -------
         - hessian (sp.Matrix) : the computed hessian matrix.
        """

        hessian = []

        for v1 in self.symbols:
            hessian_row = []
            for v2 in self.symbols:
                hessian_row.append(self.expr.diff(v1, v2).n())
            hessian.append(hessian_row)

        hessian = sp.Matrix(hessian).n()

        return hessian

