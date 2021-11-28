import copy
import numpy as np
from agents import UniAI, init_weights, Arb, Trader


def return_random_agents(num_agents, type, env1, env2, env3, h1, h2): #type = 'trader' or 'arbitrageur'
    if type == 'trader':

        agents = []
        for _ in range(num_agents):

            agent = Trader(env1.x2y, env2.x2y, env3.x2y, np.random.rand()*10, np.random.rand()*4, np.random.rand()*1000, h1, h2)

            for param in agent.parameters():
                param.requires_grad = False

            init_weights(agent)
            agents.append(agent)
    elif type == 'arbitrageur':
        agents = []
        for _ in range(num_agents):

            agent = Arb(env1.x2y, env2.x2y, env3.x2y, np.random.rand()*10, np.random.rand()*4, np.random.rand()*1000, h1, h2)

            for param in agent.parameters():
                param.requires_grad = False

            init_weights(agent)
            agents.append(agent)

    return agents


def add_elite(agents, sorted_parent_indexes, elite_index=None, only_consider_top_n=10):
    candidate_elite_index = sorted_parent_indexes[:only_consider_top_n]

    if (elite_index is not None):
        candidate_elite_index = np.append(candidate_elite_index, [elite_index])

    top_score = None
    top_elite_index = None

    for i in candidate_elite_index:
        score = return_average_score(agents[i], runs=5)
        print("Score for elite i ", i, " is ", score)

        if (top_score is None):
            top_score = score
            top_elite_index = i
        elif (score > top_score):
            top_score = score
            top_elite_index = i

    print("Elite selected with index ", top_elite_index, " and score", top_score)

    child_agent = copy.deepcopy(agents[top_elite_index])
    return child_agent

def return_children(agents, sorted_parent_indexes, elite_index):
    children_agents = []

    # first take selected parents from sorted_parent_indexes and generate N-1 children
    for i in range(len(agents) - 1):
        selected_agent_index = sorted_parent_indexes[np.random.randint(len(sorted_parent_indexes))]
        children_agents.append(mutate(agents[selected_agent_index]))

    # now add one elite
    elite_child = add_elite(agents, sorted_parent_indexes, elite_index)
    children_agents.append(elite_child)
    elite_index = len(children_agents) - 1  # it is the last one

    return children_agents, elite_index

def mutate(child):
    mutation_power = 0.02
    mutated_child = copy.deepcopy(child)
    for param in mutated_child.parameters():
        if (len(param.shape) == 2):
            for i0 in range(param.shape[0]):
                for i1 in range(param.shape[1]):
                    param[i0][i1] += mutation_power * np.random.randn()
        elif (len(param.shape) == 1):
            for i0 in range(param.shape[0]):
                param[i0] += mutation_power * np.random.randn()


