import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
from pprint import PrettyPrinter

Q={}
alpha=0.50
gamma=0.25
class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.prev=None,None

    def policy(self,QQ):
        if len([i for i in QQ.values() if i==0])==4:
            action=random.choice(QQ.keys())
        else:
            action=random.choice([i for i in QQ.keys() if QQ[i]>=max(QQ.values())])
        return action
        
    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.prev=None,None

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state=(inputs['light'],inputs['oncoming'],inputs['left'],self.next_waypoint)
        Q[self.state]=Q.get(self.state,{None:0.0,'left':0.0,'right':0.0,'forward':0.0})
        
        # TODO: Select action according to your policy
        action=self.policy(Q[self.state])
        
        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        Q[self.state][action]=(alpha*Q[self.state][action])+(alpha*reward) #First part of the Q-learning equation (updating Q with rewards)
        if self.prev[0] in Q:
            Q[self.prev[0]][self.prev[1]]+=(alpha*gamma*Q[self.state][action]) #Second part of the Q-learning equation (back-assignment of future rewards)
        self.prev=self.state,action
                                                             
        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.01, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()

pp=PrettyPrinter()
print pp.pprint(Q)
