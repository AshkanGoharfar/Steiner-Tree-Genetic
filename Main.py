from Operations import *
import matplotlib.pyplot as plt

steiner_v, terminal_v, edges = read_input()
neighbour_v = {}
neighbour_v = create_condition(edges, neighbour_v)

print('steiner_v_dict : ')
print(steiner_v_dict)

print('terminal_v_dict : ')
print(terminal_v_dict)

print('Neighbour rules')
print(neighbour_v)

# an_individual = steiner_v + terminal_v
population = []

populationSize = 3
numberOfGenerations = 5
# mutation rate should be lower than 0.2
mutationRate = 0.2
tornumentSize = 10
thereshold = 1
generation = []
best_individual = []
neighbour_v_copy = neighbour_v


def plot_optimum_path(generation, terminal_v_dict):
    indiv = generation[0].an_individual
    counter_6 = 0
    flag_5 = 0
    while counter_6 < len(indiv) and flag_5 == 0:
        if indiv[counter_6][1] in terminal_v_dict:
            explored_nodes = bfs_connected_component(generation[0].neighbour_v, indiv[counter_6][1])
            flag = 0
            for item in terminal_v_dict:
                if item not in explored_nodes:
                    flag = 1
            if flag != 1:
                print('hora')
                accepted_path = explored_nodes
                flag_5 = 1
        counter_6 += 1

    # x axis values
    x = []
    # corresponding y axis values
    y = []
    for each_node in accepted_path:
        flag_find_node = 0
        count_7 = 0
        while flag_find_node == 0 and count_7 < len(indiv):
            if indiv[count_7][1] == each_node:
                x.append(indiv[count_7][0][0])
                y.append(indiv[count_7][0][1])
                flag_find_node = 1
            count_7 += 1

    # outputs :
    plt.plot(x, y)
    plt.plot(x, y, color='blue', linewidth=3,
             marker='o', markerfacecolor='red', markersize=12)
    plt.xlabel('x - axis')
    plt.ylabel('y - axis')
    plt.title('Optimum path')
    plt.show()

    return accepted_path


for i in range(populationSize):
    an_individual = Individual(steiner_v, terminal_v, neighbour_v_copy)
    random.shuffle(an_individual.an_individual)
    generation.append(an_individual)

# initialed path
plot_optimum_path(generation, terminal_v_dict)

report = []
# Generate new populations
for numberOfRemainingGeneration in range(numberOfGenerations):
    count = 0
    for individual in generation:
        visited = []  # List to keep track of visited nodes.
        queue = []  # Initialize a queue
        explored = []
        explored_dict = {}
        individual.fitness = fitness(individual)
        count += 1
    generation_sorted = sorted(generation, key=operator.attrgetter('fitness'))
    repeated_fitness = []
    repeated_gens = []
    for item in generation_sorted:
        if item.fitness not in repeated_fitness:
            repeated_fitness.append(item.fitness)
        else:
            repeated_gens.append(item)
    for term in repeated_gens:
        del generation_sorted[generation_sorted.index(term)]
    population_selected = generation_sorted[0:tornumentSize]
    # for item in generation_sorted:
    #     print(item.fitness)

    # for item in population_selected:
    #     print(item.an_individual)

    report.append({'generation': numberOfRemainingGeneration,
                   'mean_fitness': np.mean(np.array([item.fitness for item in generation]))})
    print(report)
    print('********************************************')
    new_generation = generate_crossover(population_selected, neighbour_v, thereshold, mutationRate)
    print('********************************************')
    # for item in population_selected:
    #     print(item.an_individual)
    # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    # for item in new_generation:
    #     print(item.an_individual)

    all_gens = new_generation + generation
    all_gens_sorted = sorted(all_gens, key=operator.attrgetter('fitness'))
    repeated_list_fitness = []
    counter_8 = 0
    counter_9 = 0
    while counter_8 < populationSize:
        if all_gens_sorted[counter_9].fitness not in repeated_list_fitness:
            repeated_list_fitness.append(all_gens_sorted[counter_9].fitness)
            generation.append(all_gens_sorted[counter_9])
            counter_8 += 1
        counter_9 += 1
    generation = sorted(generation, key=operator.attrgetter('fitness'))
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

x = []
y = []
for item in report:
    x.append(item['generation'])
    y.append(item['mean_fitness'])


accepted_path = plot_optimum_path(generation, terminal_v_dict)
plt.plot(x, y)
plt.xlabel('number of generations')
plt.ylabel('Mean Fitness')
plt.title('Optimum path')
plt.show()
with open('steiner_out.txt', 'w') as the_file:
    for node in accepted_path:
        the_file.write(str(node) + '\n')
    the_file.write(str(generation[0].fitness) + '\n')

