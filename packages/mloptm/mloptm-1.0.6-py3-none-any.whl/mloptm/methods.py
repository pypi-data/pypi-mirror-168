from math import ceil, log
from tabulate import tabulate

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from mloptm.consts import RO
from mloptm.exceptions import NotOptimizedError, NotConverganceError


class Method:
    """
    Generic Class for Encapsulating the Optimization Methods

    Attrs
    -----
     - minima     (float) : the local minimum value will be calculated.
     - optm_steps (list)  : the optimizations steps.

    Raises
    ------
     - NotOptimizedError

    """
    _optimized = None

    @property
    def minima(self):
        return self._minima

    @minima.setter
    def minima(self, val):
        raise ValueError("minima cannot be set. only calculated")

    @property
    def optm_steps(self):
        return self._optm_steps

    @optm_steps.setter
    def optm_steps(self, val):
        raise ValueError("optimization steps cannot be set. only calculated")

    def Minimize(self):
        pass

    def PlotOptimizationSteps(self, xmin, xmax):
        """
        Show a Video-Like of the Optimization Steps

        Parameters
        ----------
         - xmin (float) : the minimum value of the domin of the plot
         - xmax (float) : the maximum value of the domin of the plot

        Returns
        -------
        None

        """

        if self._optimized is None:
            raise NotOptimizedError("function did not optimized yet.")

        _xs = np.linspace(xmin, xmax, 100)
        _ys = np.vectorize(self.f)(_xs)

        for step in self.optm_steps:
            plt.plot(_xs, _ys, color="blue", alpha=0.5)
            plt.scatter(step, self.f(step), marker="o", color="red")
            plt.pause(0.2)
            plt.cla()

        plt.show()

    def PrintOptimizationSteps(self):
        """
        Print the Optimization Steps in nice tabulated way.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        pass

    def ExportOptimizationSteps(self, xmin, xmax, filename):

        """
        Export the Graph of the Optimization Steps to gif image

        Parameters
        ----------
         - xmin     (float) : the minimum value of the domin of the plot
         - xmax     (float) : the maximum value of the domin of the plot
         - filename (float) : filename of the exported figure.

        Returns
        -------
        None

        """

        if self._optimized is None:
            raise NotOptimizedError("function did not optimized yet.")

        fig, ax = plt.subplots(nrows=1, figsize=(10, 7))

        _xs = np.linspace(xmin, xmax, 100)
        _ys = np.vectorize(self.f)(_xs)

        def animate(i):
            ax.clear()
            ax.plot(_xs, _ys, color="b", alpha=0.5, lw=1.5)
            ax.scatter(self.optm_steps[i], self.f(self.optm_steps[i]), 
                    marker="o", color="red")
            ax.set_xlabel("Step")
            ax.set_ylabel("Function")
            ax.set_title("Optimization Steps")

        anim = FuncAnimation(fig, animate, len(self.optm_steps), interval=200)
        anim.save('{}.gif'.format(filename), writer = 'pillow', fps = 10)


class Golden(Method):
    """
        Golden Search Optimization Method Implimintation in Python.

        Attrs
        -----
         - f (func) : the function to be optimized.
        
        Raises
        ------
         - NotOptimizedError

        Examples
        --------
        >>> from mloptm.methods import Golden
        >>> def f(x):
        ...     return x**4 - 14*x**3 + 60*x**2 - 70*x

        >>> op = Golden(f)
        >>> minima = op.Minimize(a0=0, b0=2, eps=0.03)
        >>> op.PrintOptimizationSteps()

        Using Golden Optimization Medhod
        Found Local Minima at x -> [0.777088]
        Optimization Steps with [9] Steps
        ---------------------------------
              a0        b0        a1        b1    Minima
        --------  --------  --------  --------  --------
        0         1.23607   0.763932  1.23607   0.618034
        0.472136  1.23607   0.472136  0.763932  0.854102
        0.472136  0.944272  0.763932  0.944272  0.708204
        0.652476  0.944272  0.652476  0.763932  0.798374
        0.652476  0.832816  0.763932  0.832816  0.742646
        0.72136   0.832816  0.72136   0.763932  0.777088
        0.763932  0.832816  0.763932  0.790243  0.798374
        0.763932  0.806504  0.790243  0.806504  0.785218
        0.763932  0.790243  0.780193  0.790243  0.777088

        >>> op.PlotOptimizationSteps(xmin=0, xmax=2)
        >>> op.ExportOptimizationSteps(xmin=0, xmax=2, filname="OptimizedFunction")
    """
    def __init__(self, f, *a, **kw):
        self.f = f
        self.a = a
        self.kw = kw
    
    def Minimize(self, a0, b0, eps):
        """
        Function to Run the Algorithm and Minimize the Function

        Parameters
        ----------
         - a0  (float) : the starting point of the function domin
         - b0  (float) : the ending point of the function domain
         - eps (float) : the error to compare to.

        Returns
        -------
         - minima (float) : the local minimum value. 
        """
        
        self._optm_steps = []
        self.data = []

        self.N = ceil(log(eps / 2.0) / log(1 - RO))

        for _ in range(self.N):

            a1 = a0 + RO * (b0 - a0)
            b1 = b0 - RO * (b0 - a0)

            if self.f(b1) > self.f(a1):
                b0 = b1
            else:
                a0 = a1

            minima_avg = (a0+b0)/2
            self.data.append( (a0, b0, a1, b1, minima_avg) )
            self._optm_steps.append(minima_avg)

        self._optimized = True
        self._minima = minima_avg

        return minima_avg

    def PrintOptimizationSteps(self):
        if self._optimized is None:
            raise NotOptimizedError("function did not optimized yet.")

        headers = ["a0", "b0", "a1", "b1", "Minima"]
        print("\nUsing Golden Optimization Medhod")
        print("Found Local Minima at x -> [{:.6f}]".format(self.minima))
        print("Optimization Steps with [{}] Steps".format(self.N))
        print("---------------------------------")
        print(tabulate(self.data, headers=headers))


class BiSection(Method):
    """
        BiSection Optimization Method Implimintation in Python.

        Attrs
        -----
         - f  (func) : the function to be optimized.
         - df (func) : the first derivative of function to be optimized.
        
        Raises
        ------
         - NotOptimizedError

        Examples
        --------
        >>> from mloptm.methods import BiSection
        >>> def f(x):
        ...     return x**4 - 14*x**3 + 60*x**2 - 70*x

        >>> def df(x):                                                                      
        ...     return 4*x**3 - 14*3*x**2 + 120*x - 70

        >>> op = BiSection(f, df)
        >>> minima = op.Minimize(a0=0, b0=2, epochs=10)
        >>> op.PrintOptimizationSteps()

        Using BiSection Optimization Medhod
        Found Local Minima at x -> [0.779297]
        ---------------------------------
              a0       b0    (a0+b0)/2    f'((a0+b0)/2)
        --------  -------  -----------  ---------------
        0         1           1              12
        0.5       1           0.5           -20
        0.75      1           0.75           -1.9375
        0.75      0.875       0.875           5.52344
        0.75      0.8125      0.8125          1.91895
        0.75      0.78125     0.78125         0.022583
        0.765625  0.78125     0.765625       -0.949448
        0.773438  0.78125     0.773438       -0.461435
        0.777344  0.78125     0.777344       -0.218928
        0.779297  0.78125     0.779297       -0.0980478

        >>> op.PlotOptimizationSteps(xmin=0, xmax=2)
        >>> op.ExportOptimizationSteps(xmin=0, xmax=2, filname="OptimizedFunction")
    """
    def __init__(self, f, df, *a, **kw):
        self.f = f
        self.df = df
        self.a = a
        self.kw = kw

    def Minimize(self, a0, b0, epochs=10):
        """
        Function to Run the Algorithm and Minimize the Function

        Parameters
        ----------
         - a0     (float) : the starting point of the function domin
         - b0     (float) : the ending point of the function domain
         - epochs (int)   : the number of iterations to run.

        Returns
        -------
         - minima (float) : the local minimum value. 
        """
 
        self._optm_steps = []
        self.data = []
       
        for _ in range(epochs):
            center = (a0 + b0) / 2

            if self.df(center) > 0:
                b0 = center
            else:
                a0 = center

            self._optm_steps.append(center)
            self.data.append( [a0, b0, center, self.df(center)] )

        self._optimized = True
        self._minima = center

        return center

    def PrintOptimizationSteps(self):
        if self._optimized is None:
            raise NotOptimizedError("function did not optimized yet.")

        headers = ["a0", "b0", "(a0+b0)/2", "f'((a0+b0)/2)"]
        print("\nUsing BiSection Optimization Medhod")
        print("Found Local Minima at x -> [{:.6f}]".format(self.minima))
        print("---------------------------------")
        print(tabulate(self.data, headers=headers))



class Newton(Method):
    """
        Newton Optimization Method Implimintation in Python.

        Attrs
        -----
         - f   (func) : the function to be optimized.
         - df  (func) : the first derivative of function to be optimized.
         - ddf (func) : the second derivative of function to be optimized.
        
        Raises
        ------
         - NotOptimizedError
         - NotConverganceError

        Examples
        --------
        >>> from mloptm.methods import Newton
        >>> def f(x):
        ...     return x**4 - 14*x**3 + 60*x**2 - 70*x

        >>> def df(x):
        ...     return 4*x**3 - 14*3*x**2 + 120*x - 70

        >>> def ddf(x):
        ...     return 12*x**2 - 14*6*x + 120

        >>> op = Newton(f, df, ddf)
        >>> minima = op.Minimize(x0=0, eps=10**-5)
        >>> op.PrintOptimizationSteps()

        Using Newton Optimization Method
        Found Local Minima at x -> [0.780884]
        ---------------------------------
              xk      xk+1       f'(xk+1)    f''(xk+1)
        --------  --------  -------------  -----------
        0         0.583333  -13.4977           75.0833
        0.583333  0.763103   -1.10786          62.8873
        0.763103  0.780719   -0.0101707        61.7339
        0.780719  0.780884   -8.85683e-07      61.7231
        0.780884  0.780884    0                61.7231

        >>> op.PlotOptimizationSteps(xmin=0, xmax=2)
        >>> op.ExportOptimizationSteps(xmin=0, xmax=2, filname="OptimizedFunction")
    """
    def __init__(self, f, df, ddf, *a, **kw):
        self.f = f
        self.df = df
        self.ddf = ddf
        self.a = a
        self.kw = kw
        self.__max_iters = int(10e5)

    def Minimize(self, x0, eps=10**-5):
        """
        Function to Run the Algorithm and Minimize the Function

        Parameters
        ----------
         - x0  (float) : the starting point of the function domin
         - eps (int)   : the error to compare to.

        Returns
        -------
         - minima (float) : the local minimum value. 
        """
 
        self._optm_steps = []
        self.data = []

        i = 0

        while True:
            xk = x0 - ( self.df(x0)/self.ddf(x0) )
            self._optm_steps.append(xk)
            self.data.append([x0, xk, self.df(xk), self.ddf(xk)])
            if abs(xk - x0) < eps: break
            x0 = xk
            
            # check for convergnace
            i += 1
            if i > self.__max_iters:
                raise NotConverganceError("Newton method did not converge. try different method")

        self._optimized = True
        self._minima = xk

        return xk
 
    def PrintOptimizationSteps(self):
        if self._optimized is None:
            raise NotOptimizedError("function did not optimized yet.")

        headers = ["xk", "xk+1", "f'(xk+1)", "f''(xk+1)"]
        print("\nUsing Newton Optimization Method")
        print("Found Local Minima at x -> [{:.6f}]".format(self.minima))
        print("---------------------------------")
        print(tabulate(self.data, headers=headers))


class Secant(Method):
    """
        Secant Optimization Method Implimintation in Python.

        Attrs
        -----
         - f  (func) : the function to be optimized.
         - df (func) : the first derivative of function to be optimized.
        
        Raises
        ------
         - NotOptimizedError

        Examples
        --------
        >>> from mloptm.methods import Secant
        >>> def f(x):
        ...     return x**4 - 14*x**3 + 60*x**2 - 70*x

        >>> def df(x):                                                                      
        ...     return 4*x**3 - 14*3*x**2 + 120*x - 70

        >>> op = Secant(f, df)
        >>> minima = op.Minimize(x0=4, x1=3, eps=0.0001)
        >>> op.PrintOptimizationSteps()

        Using Newton Optimization Method
        Found Local Minima at x -> [0.780884]
        ---------------------------------
              xk      xk+1    f(xk+1)       f'(xk+1)
        --------  --------  ---------  -------------
        0         0.604282   -23.3462  -11.9401
        0.1       0.733837   -24.3002   -2.97653
        0.604282  0.776858   -24.3691   -0.249017
        0.733837  0.780786   -24.3696   -0.00605475
        0.776858  0.780884   -24.3696   -1.28637e-05
        0.780786  0.780884   -24.3696   -6.67001e-10

        >>> op.PlotOptimizationSteps(xmin=0, xmax=2)
        >>> op.ExportOptimizationSteps(xmin=0, xmax=2, filname="OptimizedFunction")
    """
    def __init__(self, f, df, *a, **kw):
        self.f = f
        self.df = df
        self.a = a
        self.kw = kw

    def Minimize(self, x0, x1, eps=10**-5):
        """
        Function to Run the Algorithm and Minimize the Function

        Parameters
        ----------
         - x0  (float) : the starting point of the function domin
         - x0  (float) : the next starting point of the function domin
         - eps (int)   : the error to compare to.

        Returns
        -------
         - minima (float) : the local minimum value. 
        """
 
        self._optm_steps = []
        self.data = []

        while True:
            xk = (self.df(x1)*x0 - self.df(x0)*x1) / (self.df(x1) - self.df(x0))
            self._optm_steps.append(xk)
            self.data.append([x0, xk, self.f(xk), self.df(xk)])
            if abs(xk - x1) < eps: break
            x0 = x1
            x1 = xk

        self._optimized = True
        self._minima = xk

        return xk
        
    def PrintOptimizationSteps(self):
        if self._optimized is None:
            raise NotOptimizedError("function did not optimized yet.")

        headers = ["xk", "xk+1", "f(xk+1)", "f'(xk+1)"]
        print("\nUsing Secant Optimization Method")
        print("Found Local Minima at x -> [{:.6f}]".format(self.minima))
        print("---------------------------------")
        print(tabulate(self.data, headers=headers))


