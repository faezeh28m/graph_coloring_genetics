from itertools import count
import random
from typing import Counter

COLOR = ['RED' , 'BLUE' , 'WHITE' , 'YELLOW' , 'GREEN']


class Node:
    def __init__(self, ID , node_list = [] , color = None):
        self.__id = ID
        self.__connections = node_list.copy()
        self.__color = color

    def get_id(self):
        return self.__id

    def neighbours(self):
        return self.__connections

    def get_degree(self):
        return len(self.__connections)

    def create_connection(self, node):

        # if node not in self.__connections:

        if (node not in self.__connections) and (node is not self):
            self.__connections.append(node)
            node.create_connection(self)


    def destroy_connection(self, id):
        
        for elm in self.__connections:
            if elm.get_id() == id:
                
                self.__connections.remove(elm)
                
                return True

        return False

    def colorize(self , color):
        self.__color = color

    def get_color(self):
        return self.__color

    def __repr__(self):
        return  str(self.__id)



class Graph:

    def __init__(self, name = 'default' , node_list = []):
        self.nodes = node_list
        self.name = name


    def is_coloring_valid(self):

        for node in self.nodes:

            my_color = node.get_color()

            for neighbour in node.neighbours():
                
                if my_color == neighbour.get_color():
                    return False

        return True

    
    # def score(self): # Fitness Function

    #     score = 0

    #     for node in self.nodes:

    #         my_color = node.get_color()

    #         for neighbour in node.neighbours():
                
    #             if my_color == neighbour.get_color():
    #                 score += 1
        
    #     return (score/2)

    @staticmethod
    def read_file(pth):
        with open(pth , 'r') as file:
            num_of_nodes = int( file.readline() )
            
            # node_list = [Node(name) for name in range(1 , num_of_nodes + 1)]    # list comperhension
            
            node_list = { str(name): Node(name) for name in range(1 , num_of_nodes + 1)}

            for index in range(1 , num_of_nodes + 1 ):
                file_line = file.readline()
                current_node_list = file_line.split(' ')[:-1]
                
                for node_key in current_node_list:
                    if (node_key == '-1'):
                        break

                    node_list[str(index)].create_connection(
                        node_list[node_key]
                    )
        
        return Graph(node_list = node_list.values())



def initialze(graph , size_of_population , colors): #Initial population formation

    node_list = graph.nodes
    population = []
    num_of_colors = len(colors)

    for i in range(size_of_population):

        individual = [] 

        for node in node_list: #creat individual

            random_num = random.randint(0 , num_of_colors-1)
            random_color = colors[random_num]
            node.get_color()
            node.colorize(random_color)
            individual.append(node.get_color())
        
        population.append(individual)

    return population


def fitness(graph , individual): 

    fitness = 0
    counter1 = 0
    counter2 = 0
    
    for node in graph.nodes:
        node.colorize(individual[counter1])
        # print(node.get_color())
        counter1 += 1

    for node in graph.nodes:
        my_color = individual[counter2]

        for neighbour in node.neighbours():               
            if my_color == neighbour.get_color():
                fitness += 1
                # print('f = ' , fitness)

        counter2 += 1
        
    return (fitness/2)


def selection(graph , populatioin , size_population): #Selection best individual for population
    
    new_population = []

    for i in range(size_population):
        best_fitness = fitness(graph , populatioin[0])
        best_individual = populatioin[0]

        for individual in populatioin:
            individual_fitness = fitness(graph , individual)

            if (individual_fitness < best_fitness):
                best_fitness = individual_fitness
                best_individual = individual

        new_population.append(best_individual)
        populatioin.remove(best_individual)
        # print (new_population)
        # print(populatioin)
        # print('*******************************************8')

    return new_population
        

def crossover(parent1 , parent2 , n): #single point crossover , n = num of nodes in graph
    rand_num = random.randint(1 , n - 1)
    child1 = []
    child2 = []

    for count in range(0 , rand_num):
        child1.append( parent1[count] )
        child2.append( parent2[count] )

    for count in range(rand_num , n):
        child1.append( parent2[count] )
        child2.append( parent1[count] )

    return child1 , child2


def mutation(individual , colors):
    
    PM = 0.5 #Possibility of chromosome mutation
    PG = 0.4 #Possibility of gene mutation
    rand_num1 = random.random() #between 0 and 1
    new_individual = individual.copy()

    if(rand_num1 < PM):

        counter_gene = 0
        for gene in new_individual:
            rand_num2 = random.random()

            if(rand_num2 < PG):
                
                num_of_colors = len(colors)

                flag = True
                while (flag):
                    rand_num_color = random.randint(0 , num_of_colors - 1)
                    color = colors[rand_num_color]

                    if (color != gene) :
                        new_individual[counter_gene] = color
                        flag = False

            counter_gene += 1

    return new_individual


def genetics(graph , num_of_nodes , colors):

    size_of_population = int(input('Please enter the number of population you want : '))
    population = initialze( graph , size_of_population , colors)

    best_fitness = fitness(graph , population[0])
    best_individual = population[0]
    gen = int(input('Please enter the number of replications you want for genetics : ')) #counter of while, for repeat genetic
    counter = 0
    while best_fitness != 0 and counter != gen:

        population = selection(graph , population , size_of_population)
        random.shuffle(population)
        new_population = []

        for i in range(0 , size_of_population-1 , 2):
            child1, child2 = crossover(population[i], population[i+1] , num_of_nodes)
            new_population.append(child1)
            new_population.append(child2)
        
        for individual in new_population:
            individual = mutation(individual , colors)

        population = new_population

        for individual in population:

            individual_fitness = fitness(graph , individual)

            if(individual_fitness < best_fitness):
                best_fitness = individual_fitness
                best_individual = individual

        counter += 1

    return best_individual , best_fitness , counter


def main():
    print('********************************@@@@@@@@@@@@@@@@@')
    graph = Graph.read_file('sample-graph.gp')

    # a = Node('1' ,)
    # b = Node('2' ,)
    # c = Node('3' ,)

    # a.create_connection(b)
    # b.create_connection(c)
    # c.create_connection(a)

    # graph = Graph(node_list= [a,b,c])

    num_of_nodes = len(graph.nodes)
    num_of_colors = int(input('How many graphic colors do you want to be colored with?\n num of colors = '))

    colors = COLOR[0 : num_of_colors]

    print ('********************* Genetic *********************')

    best_individual , best_fitness , counter = genetics(graph , num_of_nodes , colors)

    print(
        'The best answer was found in the ' , counter , 'rd iteration of genetics' , 
        '\nbest answer = ' , 
        best_individual ,
        '\nwith fitnes = ' ,
        best_fitness,

        '\n********************* End *********************'
        )


main()


""" To test the selection function : """
# a = Node('1' ,)
# b = Node('2' ,)
# c = Node('3' ,)

# a.create_connection(b)
# b.create_connection(c)
# c.create_connection(a)

# my_graph = Graph(node_list= [a,b,c])
# colors = COLOR[0 : 3]
# initial_population = initialze(my_graph , 4 , colors)  
  
# print ('initial_population =' , initial_population)
# selectionP = selection(my_graph , initial_population , 3)

""" To test the mutation function : """
# a = Node('1' ,)
# b = Node('2' ,)
# c = Node('3' ,)

# a.create_connection(b)
# b.create_connection(c)
# c.create_connection(a)

# my_graph = Graph(node_list= [a,b,c])
# colors = COLOR[0 : 3]
# initial_population = initialze(my_graph , 3 , colors)

# for i in range(3):
#     print(initial_population[i])
#     mutation_individual = mutation(initial_population[i] , colors)
#     print(mutation_individual)
#     print("****************************")

""" To test the crossover function : """
# a = Node('1' ,)
# b = Node('2' ,)
# c = Node('3' ,)

# a.create_connection(b)
# b.create_connection(c)
# c.create_connection(a)

# my_graph = Graph(node_list= [a,b,c])
# colors = COLOR[0 : 3]
# initial_population = initialze(my_graph , 3 , colors)

# cross = crossover(initial_population[0] , initial_population[1] , 3)
# print('\n ', cross[0] ,'\n', cross[1])

""" To test the fitness function : """
# a = Node('1' ,)
# b = Node('2' ,)
# c = Node('3' ,)

# a.create_connection(b)
# b.create_connection(c)
# c.create_connection(a)

# my_graph = Graph(node_list= [a,b,c])
# colors = COLOR[0 : 3]
# initial_population = initialze(my_graph , 3 , colors)

# fitness1 = fitness(my_graph , initial_population[0])
# print (fitness1)
# fitness2 = fitness(my_graph , initial_population[1])
# print (fitness2)



###### For Writing Custom File ######
## Line 0: Number Of Node
## Line 1 - NON: Connections to other node
### Reminder. Note that at the end of each line from line 1 to line NON you must
### leave a blank space