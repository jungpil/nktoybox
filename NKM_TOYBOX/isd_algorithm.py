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
    import numpy.random as NPRD
    import numpy as NP
    ep = NPRD.rand(c_i.size)
    fit_value_uncertain = float(NP.mean((1 - uncertainty_base) * c_i + uncertainty_base * ep))
    return fit_value_uncertain
def linear_shock(contribution_table,shock):
    import numpy.random as NPRD
    table_dim = contribution_table.shape
    ep = NPRD.rand(table_dim[0],table_dim[1],table_dim[2])
    new_table = (1 - shock) * contribution_table + shock * ep
    return new_table
# END OF PROGRAM #