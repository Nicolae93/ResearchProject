import numpy as np
import math
import pylab
import functions as fn
from scipy import optimize

# Input parameters
# n     -> Number of steps 
# m     -> Number of Dimensions 
# beta  -> Power law index  % Note: 1 < beta < 2

def levy_flight_steps(beta, n=100000, m=2):
    
    num = math.gamma(1+beta)*np.sin(np.pi*beta/2); # used for Numerator 
    
    den = math.gamma((1+beta)/2)*beta*2**((beta-1)/2); # used for Denominator

    sigma_u = (num/den)**(1/beta); # Standard deviation
    
    u = np.random.normal(0, sigma_u, n*m)

    v = np.random.normal(0, 1, n*m)
    
    z = u / np.power(np.fabs(v), 1 / beta)

    return z

def levy_flight(function=fn.eggholder, start_coordinates=[0,0], iterations=10, bounds=[(-512, 512), (-512, 512)], show_plots=True):
    n = iterations;
    
    #creating two array for containing x and y coordinate
    #of size equals to the number of size and filled up with 0's
    x = np.zeros(n)
    y = np.zeros(n)
    #set start coordinates
    x[0], y[0] = start_coordinates[0], start_coordinates[1]
    #call levy steps
    d = levy_flight_steps(beta=1.5, n=iterations)   
    # set minimum
    minimum = function(start_coordinates)
    best_point = start_coordinates
    
    count = 0
    iter_to_best = [0]
    f_points = [minimum]
    
    count = 0
    val_i = 0
    
    scale_step = 0.1
    #print('n',n)
    for i in range(1,n): # use those steps 
        x_bound_check = bounds[0][0]<x[i-1]+d[val_i]<bounds[0][1]
        y_bound_check = bounds[1][0]<y[i-1]+d[val_i+1]<bounds[1][1]
        if x_bound_check and y_bound_check: # check bounds
            count += 1    
            x[i]= x[i-1]+d[val_i]
            y[i]= y[i-1]+d[val_i+1]
        else:
            '''
            x[i]= x[i-1]
            y[i]= y[i-1]
            '''
            if not x_bound_check:
                #print('x',x[i-1]+d[val_i]*scale_step)
                x[i]= x[i-1]-d[val_i]*scale_step
                x_bound_check = bounds[0][0]<x[i]<bounds[0][1]
            if not y_bound_check:
                #print('y',y[i-1]+d[val_i+1]*scale_step)
                y[i]= y[i-1]-d[val_i+1]*scale_step
                y_bound_check = bounds[0][0]<y[i]<bounds[0][1]
            #if still not between bounds, stay in same place    
            
            if not x_bound_check or not y_bound_check:   
                x[i]= x[i-1]
                y[i]= y[i-1]
            else: count += 1   
            
        #check if current point is better than current minimum 
        curr_point = [x[i],y[i]]
        f_curr_point = function(curr_point)
        if  f_curr_point <= minimum:
            f_points.append(f_curr_point)
            iter_to_best.append(count)
            minimum = f_curr_point
            best_point = curr_point    
        val_i = val_i + 2
        #count += 1
    #print('count',count)    
    #print('minimum',minimum)
    #insert last iteration f_point
    iter_to_best.append(n)
    f_points.append(f_points[-1])
    #create an optResult object
    result = optimize.OptimizeResult(x=best_point, fun=minimum, iter_to_best=iter_to_best, f_points=f_points)    
    #print('true iterations: ', count)
    if show_plots:
        # plotting stuff:
        pylab.title("Levi-Flight ($n = " + str(n) + "$ steps)")
        pylab.plot(x, y,'-',lw=0.5)
        #pylab.savefig("Levi-Flight"+str(n)+".png",bbox_inches="tight",dpi=600)
        pylab.show()    
    return result    

#levy_flight()