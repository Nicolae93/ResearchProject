import numpy as np
import functions as fn

class Config:
    __Function = fn.goldstein
    __Iteration = 1000
    __GlobalMin = __Function.min
    __MinDomain = __Function.domain[0] # variable lower limit
    __MaxDomain = __Function.domain[1] # variable upper limit
    __Beta = 1.5 # parameter for Levy flight
    __Dimension = 2 # The number of dimension
    __InitialCoordinates = [0,0]
    __RandomCoordinates = np.random.randint(low=__MinDomain, high=__MaxDomain, size=__Dimension)
    __ShowPlots = False
    
    @classmethod
    def get_global_min(cls):
        return cls.__GlobalMin

    @classmethod
    def get_show_plots(cls):
        return cls.__ShowPlots
        
    @classmethod
    def get_function(cls):
        return cls.__Function
    
    @classmethod
    def set_function(cls,_function):
        cls.__Function = _function
    
    @classmethod
    def get_random_coordinates(cls):
        return cls.__RandomCoordinates
    
    @classmethod
    def set_random_coordinates(cls):
        cls.__RandomCoordinates = np.random.randint(low=cls.__MinDomain, high=cls.__MaxDomain, size=cls.__Dimension)
        
    @classmethod
    def get_initial_coordinates(cls):
        return cls.__InitialCoordinates
    
    @classmethod
    def set_initial_coordinates(cls, _initial_coordinates):
        cls.__InitialCoordinates = _initial_coordinates
        
    @classmethod
    def get_iteration(cls):
        return cls.__Iteration

    @classmethod
    def get_dimension(cls):
        return cls.__Dimension

    @classmethod
    def get_max_domain(cls):
        return cls.__MaxDomain

    @classmethod
    def set_max_domain(cls, _max_domain):
        cls.__MaxDomain = _max_domain

    @classmethod
    def get_min_domain(cls):
        return cls.__MinDomain

    @classmethod
    def set_min_domain(cls, _min_domain):
        cls.__MinDomain = _min_domain

    @classmethod
    def get_beta(cls):
        return cls.__Beta

    @classmethod
    def set_beta(cls, _beta):
        cls.__Beta = _beta
