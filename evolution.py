import copy
import numpy as np

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


