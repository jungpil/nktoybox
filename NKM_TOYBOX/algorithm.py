'''
algorithm.py

NK Landscape Model

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
def incentive_structure(incentive_base, c_i, which_a, which_b, part_idx):
    """
which_a <- [...]
which_b <- [...]
    """
    N = float(len(which_a) + len(which_b))
    assert N > 0, "No incentive at all"
    import numpy as NP
    sum_of_a = c_i[which_a].sum()
    sum_of_b = c_i[which_b].sum()
    if part_idx < 1:
        F_d = (sum_of_a + incentive_base * sum_of_b) / N
    else:
        F_d = (incentive_base * sum_of_a) / N
    return F_d
# END OF PROGRAM #