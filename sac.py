# IMPORTS
import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize
from mpl_toolkits.mplot3d import Axes3D
from config import Config as cf
import random_walk as r_w
import levy_flight as l_f
import pure_random_search as p_r_s
import matplotlib.patches as mpatches

def sac():
    #CONFIGURATIONS
    start_coordinates = cf.get_random_coordinates()
    iterations = cf.get_iteration()
    min_domain = cf.get_min_domain()
    max_domain = cf.get_max_domain()
    function = cf.get_function()
    show_plots = cf.get_show_plots()
    
    #BOUNDS FOR SHGO_SOBOL
    bounds = [(min_domain, max_domain), (min_domain, max_domain)]
    
    #FIG 1. SHOW FUNCTION IN 3D
    if(show_plots):
        x = np.arange(min_domain, max_domain+1)
        y = np.arange(min_domain, max_domain+1)
        xgrid, ygrid = np.meshgrid(x, y)
        xy = np.stack([xgrid, ygrid])
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.view_init(45, -45)
        ax.plot_surface(xgrid, ygrid, function(xy), cmap='terrain')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('goldstein-price(x, y)')
        #plt.savefig('3Dfunction.png',dpi=600)
        plt.show()
    
    #OPTIMIZATION ALGORITHMS
    results = dict()
    # run shgo_sobol for better minimas visualization
    results['shgo_sobol'] = optimize.shgo(function, bounds, n=500, iters=5, sampling_method='sobol')
    results['random_walk'] = r_w.random_walk(function=function, iterations=iterations, start_coordinates=start_coordinates,show_plots=show_plots,bounds=bounds)
    results['levy_flight'] = l_f.levy_flight(function=function, iterations=iterations, start_coordinates=start_coordinates,show_plots=show_plots, bounds=bounds)
    results['pure_random_search'] = p_r_s.pure_random_search(function=function, iterations=iterations, start_coordinates=start_coordinates,show_plots=show_plots,bounds=bounds)
    '''
    #results['shgo'] = optimize.shgo(eggholder, bounds)
    results['DA'] = optimize.dual_annealing(eggholder, bounds)
    results['DE'] = optimize.differential_evolution(eggholder, bounds)
    results['BH'] = optimize.basinhopping(eggholder, bounds)
    print(results['DE'])
    '''
    #SHOW LOCAL MINIMAS AND RESULTS OF OPT ALGS
    if(show_plots):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.imshow(function(xy), interpolation='bilinear', origin='center',
                       cmap='gray')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        
        def plot_point(res, marker='o', color=None):
            return ax.plot(max_domain+res.x[0], max_domain+res.x[1], marker=marker, color=color, ms=10)
        
        '''
        plot_point(results['BH'], color='y')  # basinhopping           - yellow
        plot_point(results['DE'], color='c')  # differential_evolution - cyan
        plot_point(results['DA'], color='w')  # dual_annealing.        - white
        # SHGO produces multiple minima, plot them all (with a smaller marker size)
        plot_point(results['shgo'], color='r', marker='+')
        '''
        yellow_dot = plot_point(results['random_walk'], color='y')
        cyan_dot = plot_point(results['levy_flight'], color='c')
        blue_dot = plot_point(results['pure_random_search'], color='b')
        green_plus = ax.plot(max_domain+start_coordinates[0], max_domain+start_coordinates[1], marker='+', color='g', ms=10)
        red_x = plot_point(results['shgo_sobol'], color='r', marker='x')
        
        #PRINT RESULTS
        print('random_walk\n ','fun: '+str(results['random_walk'].fun)+'\n ','x: '+str(results['random_walk'].x))
        print('levy_flight\n ','fun: '+str(results['levy_flight'].fun)+'\n ','x: '+str(results['levy_flight'].x))
        print('pure_random_search\n ','fun: '+str(results['pure_random_search'].fun)+'\n ','x: '+str(results['pure_random_search'].x))
        print('shgo_sobol\n ','success: '+str(results['shgo_sobol'].success)+'\n ',
              'fun: '+str(results['shgo_sobol'].fun)+'\n ','x: '+str(results['shgo_sobol'].x))
    
        #FIG 2. PRINT ALL MINIMAS
        for i in range(results['shgo_sobol'].xl.shape[0]):
            ax.plot(max_domain + results['shgo_sobol'].xl[i, 0],
                    max_domain + results['shgo_sobol'].xl[i, 1],
                    'ro', ms=2)
    
        #PRINT OBTAINED MINIMAS
        red_x = mpatches.Patch(color='r', label='global')
        cyan_dot = mpatches.Patch(color='c', label='l_f')
        yellow_dot = mpatches.Patch(color='y', label='r_w')
        blue_dot = mpatches.Patch(color='b', label='p_r_s')
        green_plus = mpatches.Patch(color='g', label='start')
        plt.legend(handles=[cyan_dot,yellow_dot,blue_dot,green_plus,red_x])
    
        ax.set_xlim([0, max_domain*2])
        ax.set_ylim([0, max_domain*2])
        fig.suptitle('Minimas', fontsize=10)
        #plt.savefig('Minimas.png',dpi=600)
        plt.show()
        
        #FIG 3. PLOT MINIMA IMPROVEMENT
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(results['pure_random_search'].iter_to_best, results['pure_random_search'].f_points,'.-',label='p_r_s')
        ax.plot(results['levy_flight'].iter_to_best, results['levy_flight'].f_points,'.-',label='l_f')
        
        plt.plot(results['pure_random_search'].iter_to_best[-2], results['pure_random_search'].f_points[-1], '|', color='b', ms=15);
        plt.plot(results['levy_flight'].iter_to_best[-2], results['levy_flight'].f_points[-1], '|', color='red', ms=15);
        
        ax.set(xlabel='iterations', ylabel='f_val',
               title='towards the global minima')
        plt.legend(loc = 'best')
        ax.grid()
        #plt.savefig('LevyVsPureRS',dpi=600)
        plt.show()
        
    best_x = min(results['pure_random_search'].fun,results['levy_flight'].fun)#,results['random_walk'].fun)
    if results['pure_random_search'].fun == best_x:
        best_alg = 'pure_random_search'
    elif results['levy_flight'].fun == best_x:
        best_alg = 'levy_flight'
    else: best_alg = 'random_walk'
    #print('best alg: '+best_alg, best_x)
    
    return results


