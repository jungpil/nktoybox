'''
Created on 2014. 3. 2.

@author: drtagkim
'''
import copy
class Case:
    def __init__(self,*args,**kwargs):
        self.runs = kwargs['run']
        self.influence_matrix = kwargs['influence_matrix']
        self.initial_uncertainty = kwargs['bias']
        self.amount_of_change_per_shock = kwargs['delta']
        self.tau_list =copy.deepcopy(kwargs['tau_list'])
        self.agent_list = kwargs['agent_list']
    def get_agent_list(self):
        return copy.deepcopy(self.agent_list)
    def get_tau_list(self):
        return copy.deepcopy(self.tau_list)
