'''
isd_algorithm.py

NK Landscape Model
Modularity x ISD

Jungpil and Taekyung

2014
'''
def linear_uncertainty(uncertainty_base, c_i, tick, total_tick):
    """
The following arguments should be included: uncertainty_base, c_i, tick and total_tick
    """
    import random
    uncertainty_i = (1-float(tick)/float(total_tick))*uncertainty_base
    fit_value_uncertain = (1 - uncertainty_i) * c_i + uncertainty_i * random.random()
    return fit_value_uncertain
# END OF PROGRAM #