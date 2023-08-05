# Optimization Methods
Methods Discussed
 - Golden Section Search Method
 - BiSection Method
 - Newton Method
 - Secant Method

## Golden Section Search Methods
```python
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
```

## BiSection Method
```python
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
```

## Newton Method
```python
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
```

## Secant Method
```python
>>> from mloptm.methods import Secant
>>> def f(x):
...     return x**4 - 14*x**3 + 60*x**2 - 70*x

>>> def df(x):                                                                      
...     return 4*x**3 - 14*3*x**2 + 120*x - 70

>>> op = Secant(f, df)
>>> minima = op.Minimize(a0=0, b0=2, epochs=10)
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
>>> p.ExportOptimizationSteps(xmin=0, xmax=2, filname="OptimizedFunction")

```
