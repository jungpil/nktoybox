'''
Created on 2014. 3. 1.

@author: drtagkim
'''
import RandomGenerator
import numpy as NP
import random
from collections import deque #list object (faster)
class AgentClan:
    """
    >>> tribe = AgentClan(landscape,1,100) # 100 men
    >>> tribe.name_called('bushman') # They are called, 'bushman.'
    >>> tribe.set_constraints(0.7) # TODO - FOR TEST (OPTION)
    >>> tribe.set_iteration_plan([(1,2,3),(4,5),(6,7,8)]) # N=8 TODO - don't use it. it's just for testing.
    >>> tribe.place_in_land(landscape_america) # If you need to move another place...
    >>> tribe.establish() # They establish a state. #TODO - for testing
    >>> tribe.hatch_members(MyAgent) # MyAgent is a type class that inherits agent.Agent .
    So, simply,
    >>> tribe = AgentClan(landscape,1,100)
    >>> tribe.name_called('bushmen')
    >>> tribe.hatch_members()
    >>>
    """
    def __init__(self,landscape, processing_power, agent_class, population=1):
        """
        # An agent has a processing power (or limited processing capability).
        """
        assert processing_power > 0, "Processing power should be positive."
        self.myProcessingPower = processing_power
        self.myLocId = -1
        self.total_num = population #TODO, change the name
        self.landscape = landscape #nowhere to go
        self.tribe = deque() #list object (python collections)
        self.number_of_not_finished = -1 #finished work
        self.member_identification_record = []
        self.agent_class = agent_class
    def hatch_members(self):
        '''
        >>> my_tribe.hatch_members(MyAgent) # MyAgent is a class
        '''
        space_length = 1<<self.landscape.get_influence_matrix_N()
        upper_limit = space_length-1
        self.tribe = deque()
        add_member = self.tribe.append
        for _ in xrange(self.total_num):
            member_loc_id = random.randint(0,upper_limit)
            agent = self.agent_class(member_loc_id,self)
            add_member(agent)
        self.number_of_not_finished = self.total_num
    def refresh_clan(self):
        self.number_of_finished = self.total_num
        self.hatch_members()
    def place_in_land(self,landscape):
        self.landscape = landscape
    def name_called(self,type_name):
        self.type_name = type_name
    def set_constraints(self,constraint):
        assert constraint > 0, "Constraint should be positive."
        assert constraint <= 1, "Constraint should be less than 1."
        self.constraint = constraint
    def set_iteration_plan(self,iteration_plan):
        """
        input value -> [(1,2,3),(4,5,6),(7,8,9)]
        """
        #check data
        assert sum(map(len,iteration_plan)) == self.my_N, "You have a problem on the iteration plan!"
        total_item = []
        for ep in iteration_plan:
            total_item.extend(ep)
        #starting from 1
        total_item.sort() #sort (ascending)
        #report any missing values in the plan
        c_set_1 = NP.array(total_item,dtype=NP.int)
        c_set_2 = NP.arange(1,(self.my_N+1),dtype=NP.int)
        c_diff = c_set_1 - c_set_2
        if sum(c_diff) != 0:
            report = NP.where(c_diff != 0)[0]+1
            assert False, "The following items are missing in your plan: %s" % (", ".join(["%d"%i for i in report]))

        self.iteration_plan = iteration_plan
    def establish(self):
        self.my_num = 0
        self.my_implemented_elements = set()
        self.my_unimplemented_elements = set(range(self.my_N))
    def is_done(self):
        return self.my_current_iteration_num == len(self.iteration_plan)
    def get_current_elements_plan(self):
        return self.iteration_plan[self.my_current_iteration_num][:]
    def has_next_agent(self):
        return self.my_num < self.total_num

class Role:
    """
    # Role is a plug-in object for an agent.
    """
    def __init__(self,**plug_ins):
        self.define_plugin_behavior(plug_ins)
    def define_plugin_behavior(self,plug_ins):
        pass
        #List up plugin function here
        #if plug_ins.has_key('func_can_partner_with'): self.can_partner_with = plug_ins['func_can_partner_with'] #plug-in function
        #if plug_ins.has_key('func_getLocIdWithOtherLocId'): self.getLocIdWithOtherLocId = plug_ins['func_getLocIdWithOtherLocId']
'''
How to define plug-in behavior?
It is easy.
Create a class that inherits Role
class InnovatorRole(Role):
  def __init__(self,**plug_ins):
    Role.__init__(self,**plug_ins)
  def define_plugin_behavior(self,plug_ins):
    if plug_ins.has_key('func_can_partner_with'): self.can_partner_with = plug_ins['func_can_partner_with'] #plug-in function

>>> mb = InnovatorRole(func_can_partner_with = can_partner_with)
'''
class Agent:
    '''
    Abstract class for agent
    '''
    def __init__(self,my_id,my_clan):
        self.my_id  = my_id
        self.my_performance = 0.0 #this is default value of getting fitness value
        self.my_clan = my_clan #landscape
        self.my_status = -1
        #TODO - check assertions
    def compute_average_performance_fitness_around_me(self,whosethere):
        '''
        Include me, if plan is not specified, all occasions should be considered.
        That may be all others!
        So, it is much wiser to use generate_random_plan(N,how_many)
        '''
        fitness_values = map(self.my_clan.landscape.get_score_of_location_by_id,whosethere)
        self.my_status *= -1 #flip my status (DO NOT USE False or True! It drops performance.)
        return NP.mean(fitness_values)
    def compute_average_performance_fitness_around_me2(self,whosethere,candidate,plan):
        c_whose = set()
        for wid in whosethere:
            new_id = self.my_clan.landscape.change_element(wid,candidate,plan)
            c_whose.add(new_id)
        fitness_values = map(self.my_clan.landscape.get_score_of_location_by_id,c_whose)
        return NP.mean(fitness_values)
#For example, you can use this function as a plug-in for Behavior.
'''
'''
def getLocIdWithOtherLocId(land_scape,me,other,is_copy):
    assert type(me) == Agent and type(other) == Agent, "Input should be agents!"
    assert type(is_copy) == bool, "The parameter, is_copy, should be Boolean."
    result = me.myLocId #start point = result, at this time
    otherLocId = other.myLocId
    for idx in me.myP: #TODO - naming
        shiftAmount = land_scape.get_influence_matrix_N() - 1 - idx;
        x_1 = (1 << shiftAmount) * ((otherLocId >> shiftAmount) % 2 - (result >> shiftAmount) % 2)
        if is_copy:
            x_2 = 1
        else:
            x_2 = 0 if RandomGenerator.random_generator.randint(0,2) == 0 else 1
        result += (x_1 * x_2)
    return result
def generate_random_plan(N, how_many):
    import random #only for this method
    possible_men = xrange(N)
    random.shuffle(possible_men)
    return possible_men[:how_many]