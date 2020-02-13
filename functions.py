import numpy as np

# FUNCTIONS
def goldstein(xx):
    x1 = xx[0]
    x2 = xx[1]
    fact1a = (x1 + x2 + 1)**2
    fact1b = 19 - 14*x1 + 3*x1**2 - 14*x2 + 6*x1*x2 + 3*x2**2
    fact1 = 1 + fact1a*fact1b
    fact2a = (2*x1 - 3*x2)**2
    fact2b = 18 - 32*x1 + 12*x1**2 + 48*x2 - 36*x1*x2 + 27*x2**2
    fact2 = 30 + fact2a*fact2b
    return fact1*fact2
    
def sphere(xx):
    d = len(xx)
    summa = 0
    for i in range(0,d):
        xi = xx[i]
        summa = summa + np.power(xi, 2)
    return summa

def eggholder(x):
    return (-(x[1] + 47) * np.sin(np.sqrt(abs(x[0]/2 + (x[1]  + 47))))
            -x[0] * np.sin(np.sqrt(abs(x[0] - (x[1]  + 47)))))

def rastrigin(array):
    sum = 0
    fitness = 0
    for x in array:
        sum = sum + x**2 - 10 * np.cos(2 * np.pi * x)
    fitness = 10.0 * len(array) + sum
    return fitness

def schwefel(array):
    summa = 0
    fitness = 0
    for x in array:
        summa = summa + x * np.sin(np.sqrt(np.abs(x)))
    fitness = 418.9829 * len(array) - summa
    return fitness

def michalewicz(array):#for the number of Dimension is 2
    sum = 0
    fitness = 0
    m = 10
    for (i,x) in enumerate(array, start=1):
        sum = sum + np.sin(x) * np.sin((i * (x**2) )/np.pi)**(2*m)
    fitness = -sum
    return fitness

def rosen(array):
    return (1 - array[0])**2 + 100 * (array[1] - array[0]**2)**2

#DOMAINS
setattr(goldstein, 'domain', [-2,2])
setattr(sphere, 'domain', [-5.12,5.12])
setattr(eggholder, 'domain', [-512,512])
setattr(rastrigin, 'domain', [-5.12,5.12])
setattr(schwefel, 'domain', [-500,500])
setattr(michalewicz, 'domain', [0,3.14])
setattr(rosen, 'domain', [-5,10])

#MINIMAS
setattr(goldstein, 'min', 3.00)
setattr(sphere, 'min', 0.00)
setattr(eggholder, 'min', -959.6406)
setattr(rastrigin, 'min', 0.00)
setattr(schwefel, 'min', 0.00)
setattr(michalewicz, 'min', -1.8013)
setattr(rosen, 'min', 0.00)
