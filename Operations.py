import random
import math
from Individual import Individual
import numpy as np
import operator
import matplotlib.pyplot as plt
import itertools
import random


def read_input():
    f = open("steiner_in.txt", "r")
    input_f = f.read().split('\n')
    num_of_steiner_v = int(input_f[0].split(' ')[0])
    num_of_terminal_v = int(input_f[0].split(' ')[1])
    num_of_edges = int(input_f[0].split(' ')[2])
    steiner_v = []
    for i in range(1, num_of_steiner_v + 1):
        steiner_v.append([[int(input_f[i].split(' ')[0]), int(input_f[i].split(' ')[1])], i - 1])
    terminal_v = []
    for i in range(num_of_steiner_v + 1, num_of_steiner_v + num_of_terminal_v + 1):
        terminal_v.append([[int(input_f[i].split(' ')[0]), int(input_f[i].split(' ')[1])], i - 1])
    edges = []
    for i in range(num_of_steiner_v + num_of_terminal_v + 1, len(input_f) - 1):
        edges.append([int(input_f[i].split(' ')[0]), int(input_f[i].split(' ')[1])])
    num_of_edges = len(edges)
    return steiner_v, terminal_v, edges


# vertices relations to each other with edges
def create_condition(edges, neighbour_v):
    # neighbour_v = {}
    for i in range(len(edges)):
        if edges[i][0] not in neighbour_v and edges[i][1] not in neighbour_v:
            neighbour_v[edges[i][0]] = [edges[i][1]]
            neighbour_v[edges[i][1]] = [edges[i][0]]

        if edges[i][0] in neighbour_v and edges[i][1] not in neighbour_v:
            neighbour_v[edges[i][1]] = [edges[i][0]]
            if edges[i][1] not in neighbour_v[edges[i][0]]:
                neighbour_v[edges[i][0]].append(edges[i][1])

        if edges[i][0] not in neighbour_v and edges[i][1] in neighbour_v:
            neighbour_v[edges[i][0]] = [edges[i][1]]
            if edges[i][0] not in neighbour_v[edges[i][1]]:
                neighbour_v[edges[i][1]].append(edges[i][0])

        if edges[i][0] in neighbour_v and edges[i][1] in neighbour_v:
            if edges[i][0] not in neighbour_v[edges[i][1]]:
                neighbour_v[edges[i][1]].append(edges[i][0])
            if edges[i][1] not in neighbour_v[edges[i][0]]:
                neighbour_v[edges[i][0]].append(edges[i][1])
    neighbour_v = {k: v for k, v in sorted(neighbour_v.items(), key=lambda item: item[0])}
    return neighbour_v


def bfs_connected_component(graph, start):
    explored = []
    explored_dict = {}
    # keep track of nodes to be checked
    queue = [start]
    # keep looping until there are nodes still to be checked
    while queue:
        # pop shallowest node (first node) from queue
        node = queue.pop(0)
        if node not in explored and not set(terminal_v_dict).issubset(explored_dict):
            # add node to list of checked nodes
            explored.append(node)
            neighbours = graph[node]
            explored_dict[node] = 1
            # add neighbours of node to queue
            for neighbour in neighbours:
                if neighbour not in explored and not set(terminal_v_dict).issubset(explored_dict):
                    queue.append(neighbour)
                    #### ??????????????????
                    # bfs_connected_component(graph, neighbour)
    return explored


def fitness(individual):
    # keep track of all visited nodes
    an_individual = individual.an_individual
    flag = -1
    counter = 0
    fitness = 0
    inputs = {}
    # individual.neighbour_v = update_neighbour_v(an_individual, origin_neighbours())
    while counter < len(an_individual):
        if an_individual[counter][1] in terminal_v_dict:
            explored_nodes = bfs_connected_component(individual.neighbour_v, an_individual[counter][1])
            for item in terminal_v_dict:
                if item not in explored_nodes:
                    flag = 1
            if flag != 1:
                accepted_path = explored_nodes
                for j in range(len(accepted_path)):
                    inputs[accepted_path[j]] = an_individual[j][0]
                # for i in range(len(an_individual)):
                #     inputs[an_individual[i][1]] = an_individual[i][0]
                for k in range(1, len(accepted_path)):
                    fitness += np.sqrt(
                        np.square(inputs[accepted_path[k]][0] - inputs[accepted_path[k - 1]][0]) + np.square(
                            inputs[accepted_path[k]][1] - inputs[accepted_path[k - 1]][1]))
                flag = 0
                # print('fitness : ')
                # print(fitness)
                return fitness
        counter += 1
    if flag == -1:
        return 100000000000
    return fitness



def remove_iterated_gens(new_child):
    gens = []
    for gen in new_child:
        if gen not in gens:
            gens.append(gen)
        else:
            del new_child[new_child.index(gen)]
    return new_child


def remove_iterated_items(list):
    items = []
    for item in list:
        if item not in items:
            items.append(item)
        else:
            del list[list.index(item)]
    return list


def update_neighbour_v(each_individual, neighbour_v):
    neighbours = origin_neighbours()
    for steiner_node in steiner_v:
        if steiner_node not in each_individual and steiner_node[1] in neighbours:
            all_neighbours = neighbours[steiner_node[1]]
            del neighbours[steiner_node[1]]
            for term in all_neighbours:
                neighbours[term].remove(steiner_node[1])
    return neighbours


def steiner_node_for_individual(new_child):
    child_steiner_nodes = []
    for steiner_node in steiner_v:
        if steiner_node in new_child:
            child_steiner_nodes.append(steiner_node)
    return child_steiner_nodes


def mutation(new_child, worst_children, best_children, selected_parent_individual, neighbour_v, flag_status,
             last_steiner_node, thereshold, mutationRate):
    counter = 0
    child_steiner_nodes = steiner_node_for_individual(new_child)
    new_child = remove_iterated_gens(new_child)
    while counter < len(new_child):
        if new_child[counter][1] in terminal_v_dict:
            neighbour_of_child = update_neighbour_v(new_child, neighbour_v)
            explored_nodes = bfs_connected_component(neighbour_of_child, new_child[counter][1])
            flag_1 = 0
            for item in terminal_v_dict:
                if item not in explored_nodes:
                    flag_1 = 1
            if flag_1 != 1:
                print('yess best')
                flag_status = 1
                best_children = new_child
                print('best answer')
                print(best_children)
                thereshold -= 1
                last_steiner_node = child_steiner_nodes[0]
                del new_child[new_child.index(child_steiner_nodes[0])]
                mutate_chance = random.uniform(0, 1)
                if thereshold < 1 and mutate_chance > mutationRate:
                    return best_children
                return mutation(new_child, worst_children, best_children, selected_parent_individual, neighbour_v,
                                flag_status,
                                last_steiner_node, thereshold, mutationRate)
        counter += 1
    if flag_status == 1:
        best_children.append(last_steiner_node)
    if flag_status == 0 and selected_parent_individual == best_children:
        selected_parent_steiners = origin_steiners(selected_parent_individual)
        selected_parent_steiners_list = []
        for term in selected_parent_steiners:
            selected_parent_steiners_list.append([selected_parent_steiners[term], term])
        worst_children_steiners = origin_steiners(worst_children)
        ignored_steiners = []
        for steiner_node in steiner_v_dict:
            if steiner_node not in selected_parent_steiners and steiner_node not in worst_children_steiners:
                ignored_steiners.append([steiner_v_dict[steiner_node], steiner_node])
        all_terminals = []
        for item in terminal_v_dict:
            all_terminals.append([terminal_v_dict[item], item])
        new_child_random = all_terminals + ignored_steiners + selected_parent_steiners_list
        new_child_random = remove_iterated_gens(new_child_random)
        random.shuffle(new_child_random)
        print('new_child_random : ')
        print(new_child_random)
        counter_3 = len(selected_parent_steiners_list) - 1
        while counter_3 > -1:
            counter_2 = 0
            new_child_random = remove_iterated_gens(new_child_random)
            new_child_random.remove(selected_parent_steiners_list[counter_3])
            while counter_2 < len(new_child_random):
                if new_child_random[counter_2][1] in terminal_v_dict:
                    new_child_random = remove_iterated_gens(new_child_random)
                    neighbour_of_child_1 = update_neighbour_v(new_child_random, origin_neighbours())
                    explored_nodes = bfs_connected_component(neighbour_of_child_1, new_child_random[counter_2][1])
                    flag_1 = 0
                    for item in terminal_v_dict:
                        if item not in explored_nodes:
                            # necessary_steiner_node.append(item)
                            # necessary_steiner_node = remove_iterated_items(necessary_steiner_node)
                            flag_1 = 1
                    if flag_1 != 1:
                        print('yess better')
                        best_children = new_child_random
                        print('better answer')
                        print(best_children)
                        return best_children
                counter_2 += 1
            counter_3 -= 1
    if flag_status == 0 and selected_parent_individual == best_children:
        print('Bad news !!!')
    return best_children


def generate_crossover(individuals, neighbour_v, thereshold, mutationRate):
    new_pop = []
    for i in range(len(individuals)):
        if individuals[i].fitness < individuals[(i + 1) % len(individuals)].fitness:
            selected_parent = individuals[i]
            other_parent = individuals[(i + 1) % len(individuals)]
        else:
            selected_parent = individuals[(i + 1) % len(individuals)]
            other_parent = individuals[i]

        if len(individuals[i].an_individual) < len(individuals[(i + 1) % len(individuals)].an_individual):
            less_length = len(individuals[i].an_individual)
        elif len(individuals[i].an_individual) > len(individuals[(i + 1) % len(individuals)].an_individual):
            less_length = len(individuals[(i + 1) % len(individuals)].an_individual)
        else:
            less_length = len(individuals[(i + 1) % len(individuals)].an_individual)
        new_child = []
        for j in range(0, less_length):
            if j % 2 == 0:
                new_child.append(individuals[i].an_individual[j])
            else:
                new_child.append(individuals[(i + 1) % len(individuals)].an_individual[j])
        new_child = remove_iterated_gens(new_child)
        for terminal in terminal_v:
            if terminal not in new_child:
                new_child.append(terminal)

        ignored_steiner_nodes = []
        for steiner_node in selected_parent.steiner_v:
            if steiner_node not in new_child:
                ignored_steiner_nodes.append(steiner_node)
        counter_9 = 0
        selected_parent_individual = selected_parent.an_individual
        other_parent_individual = other_parent.an_individual
        while len(new_child) < len(selected_parent_individual):
            new_child.append(ignored_steiner_nodes[counter_9])
            counter_9 += 1
        best_children = selected_parent_individual
        worst_children = other_parent_individual
        flag_stats = 0
        last_steiner_node = []
        best_children = mutation(new_child, worst_children, best_children, selected_parent_individual, neighbour_v,
                                 flag_stats,
                                 last_steiner_node, thereshold, mutationRate)
        best_children_steiner_nodes = steiner_node_for_individual(best_children)
        best_children_neighbour = update_neighbour_v(best_children, neighbour_v)
        new_individual = Individual(best_children_steiner_nodes, terminal_v, best_children_neighbour)
        new_individual.an_individual = best_children
        new_individual.fitness = fitness(new_individual)
        new_pop.append(new_individual)
    return new_pop


def origin_neighbours():
    original_neighbour = {}
    steiner_v, terminal_v, edges = read_input()
    original_neighbour = create_condition(edges, original_neighbour)
    return original_neighbour


steiner_v, terminal_v, edges = read_input()
steiner_v_dict = {}
for i in range(len(steiner_v)):
    steiner_v_dict[steiner_v[i][1]] = steiner_v[i][0]

terminal_v_dict = {}
for i in range(len(terminal_v)):
    terminal_v_dict[terminal_v[i][1]] = terminal_v[i][0]


def origin_steiners(each_individual):
    individual_stiener_dict = {}
    for item in each_individual:
        if item[1] in steiner_v_dict:
            individual_stiener_dict[item[1]] = item[0]
    return individual_stiener_dict

