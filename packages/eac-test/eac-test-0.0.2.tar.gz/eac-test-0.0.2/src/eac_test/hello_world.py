
import numpy as np


def hello():
    """Print hello world"""
    print("Hello world")


def waste_cpu(n_trials = 1000000):
    """Estimate pi using a really inefficient method
    
    Parameters
    ----------
    n_trials : int
        Number of trials 
    
    Returns
    -------
    pi : float
        Estimate of pi
    """
    n_pass = 0    
    vec = np.random.uniform(size=2*n_trials).reshape(2, n_trials)
    rad2 = np.sum(vec*vec, axis=0)
    n_pass = (rad2 < 1.).sum()
    pi = 4*n_pass/n_trials
    return pi
