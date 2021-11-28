import copy
import numpy as np
import random

def return_random_agents(num_agents, typ, env1, env2, env3, h1, h2): #type = 'trader' or 'arbitrageur'
  if typ == 'trader':
      agents = []
      for i in range(num_agents):
          agent = Trader(env1.x2y(), env2.x2y(), env3.x2y(), np.random.rand()*10, np.random.rand()*4, np.random.rand()*5000, h1, h2)
          agents.append(agent)
  elif typ == 'arbitrageur':
      agents = []
      for i in range(num_agents):
          agent = Arb(env1.x2y(), env2.x2y(), env3.x2y(), np.random.rand()*10, np.random.rand()*4, np.random.rand()*5000, h1, h2)
          agents.append(agent)
  return agents

def select_elites(agents, elites_frac = 0.2):
  agents = np.array(agents)
  returns = []
  for i in agents:
    returns.append(i.get_return())
  return agents[np.argsort(returns)][- len(agents) * 0.2 :]

def clone_elite(elite_agents, times = 5):
  cloned_agents = []
  for i in range(5):
    for agent in elite_agents:
      cloned_agents.append(agent)

def mutation(generation, frac = 0.8):
  for _ in range(frac * len(generation)):
    number = random.choice(np.arange(len(generation)))
    mutate(generation[number].model)
    generation[number].c1 = np.random.rand()*10
    generation[number].c2 = np.random.rand()*4
    generation[number].c3 = np.random.rand()*5000

def mutate(child):
    mutation_power = 0.01
    mutated_child = copy.deepcopy(child)
    for param in mutated_child.parameters():
        if (len(param.shape) == 2):
            for i0 in range(param.shape[0]):
                for i1 in range(param.shape[1]):
                    param[i0][i1] += mutation_power * np.random.randn()
        elif (len(param.shape) == 1):
            for i0 in range(param.shape[0]):
                param[i0] += mutation_power * np.random.randn()
