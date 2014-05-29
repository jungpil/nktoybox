import numpy as np

class AdapterPlanISD:
    def __init__(self, simulator, adapter_behavior, agent_clan, agent, tick_end):
        self.simulator = simulator
        self.adapter_behavior = adapter_behavior
        self.agent_clan = agent_clan
        self.agent = agent
        self.tick_end = tick_end
    def run(self):
        agent = self.agent
        current_behavior = self.adapter_behavior(self.agent_clan,agent)
        break_marker = False
        ct = 0
        # initialization
        agent.true_performance = self.agent_clan.landscape.get_score_of_location_by_id(agent.my_id)
        agent.expected_performance = agent.true_performance
        self.simulator.write_record(agent.true_performance,ct)
        # searching
        while 1:
            for plan in agent.plans:
                agent.ct = ct
                (agent.my_id, agent.true_performance) = current_behavior.execute(agent, plan)
                ct += 1
                self.simulator.write_record(agent.true_performance,ct)
                if ct >= self.tick_end: # if ticks are over the target number,
                    break_marker = True
                    break
            if break_marker == True:
                break