import numpy as np
import functions as fn
from scipy import optimize
import pylab

def pure_random_search(function=fn.eggholder, start_coordinates=[0,0], iterations=100000, bounds=[(-512, 512), (-512, 512)], show_plots=True):
    # defining the number of steps
    n = iterations
    #creating two array for containing x and y coordinate
    #of size equals to the number of size and filled up with 0's
    x = np.zeros(n)
    y = np.zeros(n)
    # set initial coordinates
    x[0], y[0] = start_coordinates[0], start_coordinates[1]
    # set minimum
    minimum = function(start_coordinates)
    best_point = start_coordinates
    # filling the coordinates with random variables
    count = 0
    iter_to_best = [0]
    f_points = [minimum]
    for i in range(1,n): # use those steps 
        x[i]= np.random.uniform(low=bounds[0][0], high=bounds[0][1])
        y[i]= np.random.uniform(low=bounds[1][0], high=bounds[1][1])
        #check if current point is better than current minimum 
        curr_point = [x[i],y[i]]
        f_curr_point = function(curr_point)
        if  f_curr_point <= minimum:
            f_points.append(f_curr_point)
            iter_to_best.append(count)
            minimum = f_curr_point
            best_point = curr_point        
        count += 1    
    #insert last iteration f_point
    iter_to_best.append(n)
    f_points.append(f_points[-1])    
    #create an optResult object
    result = optimize.OptimizeResult(x=best_point, fun=minimum, iter_to_best=iter_to_best, f_points=f_points)    
    #print('true iterations: ', count)
    if show_plots:
        # plotting stuff:
        pylab.title("Pure Random Search ($n = " + str(n) + "$ steps)")
        pylab.plot(x, y,'o',ms=0.1)
        #pylab.savefig("Pure_Random_Search"+str(n)+".png",bbox_inches="tight",dpi=600)
        pylab.show()    
    return result  

#pure_random_search()