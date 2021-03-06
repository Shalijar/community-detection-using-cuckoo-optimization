# -*- coding: utf-8 -*-
"""cuckoo_clean.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hD1uQB4IjNcGlUhVJXF2ykqYQXtXSPvI
"""

import math
import random
import copy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import networkx as nx
import seaborn as sns

"""Define the problem parameters such as n = number of nodes 
			, adj = adjacency matrix of the graph
      , Graph_edge = array of graphs - this will simplify the graph visualization process - 
And lastly defualt_n_community = number of communities 
 
 
"""

class Problem:
	def __init__(self, n, adj, graph_edge, default_n_community):
		self.n = n
		self.adj = adj
		self.m = int(sum([len(x) for x in self.adj])/2)
		self.default_n_community = default_n_community
		self.graph_edge = graph_edge

"""We want to create a random first population and improve on this. To this we first shuffle the array list then we will iterate on it. In each iteration we will choose members of a community randomly and assign their community to them. Done by this section of the code : 
 
```````````
  selected = random.choices(vertices, k=int(self.n / self.default_n_community))
          vertices = [e for e in vertices if e not in selected]
          for i in selected:
            individual_map[i] = counter
          counter += 1 
```````````


Keep in mind in the last iteration there is only one possible community to assign the remaining nodes

In the end we will sort the randomly generated populations based on the fitness function. We can see the formula and code below : 



![image.png](data:image/png;base64,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)
 


```
self.population = sorted(self.population, key=lambda agent: self.fitness(
			agent), reverse=False)
```



"""

class Problem(Problem):
	def initial_population(self):
		self.population = []
		# We want to create a number of populations

		for _ in range(self.population_size):

			# For each one we will randomly put the nodes on a community
			
			vertices = list(range(self.n))
			random.shuffle(vertices)
			individual_map = [None] * self.n
			
			counter = 0
			
			while len(vertices) != 0:
				if len(vertices) < int(self.n / self.default_n_community):
					selected = vertices[:]
					for i in selected:
						individual_map[i] = counter
					counter += 1
					break
				else:
					selected = random.choices(vertices, k=int(self.n / self.default_n_community))
					vertices = [e for e in vertices if e not in selected]
					for i in selected:
						individual_map[i] = counter
					counter += 1

			self.population.append(individual_map)
			
		self.population = sorted(self.population, key=lambda agent: self.fitness(
			agent), reverse=False)

"""In the cuckoo algorithm each cuckoo will breed a random number of eggs and place them in its corresponding permitted radius (defined as elr). In our code we will select a random number of eggs. 


```
number_of_eggs = random.randint(1, min(4, self.n) )

```



then we will select a number of nodes (number of eggs) and randomly change their community to one of their neighbors



```
gene = [random.randint(1, self.n - 1) for _ in range(number_of_eggs)]
			while len(set(gene)) < number_of_eggs : 
				gene = [random.randint(1, self.n - 1) for _ in range(number_of_eggs)]
			for j in range(len(gene)):
				joining_node = random.choice([exc for exc in adj[gene[j]] if exc != gene[j] ])
				new_egg_pop = self.population[i][:]
				new_egg_pop[gene[j]] = self.population[i][joining_node]
				breaded_eggs.append(new_egg_pop)
```


As it is done in cuckoo optimization algorithm we will remove 10% of the least desirable eggs generated 

```
num_to_remove = round(len(breaded_eggs)/10)
		breaded_eggs = sorted(breaded_eggs, key=lambda agent: self.fitness(agent),
		                      reverse=False)[num_to_remove:] 
```

Finally we will maintain our population by removing the ones performing badly. This is basically the notion of : survival of the fittest 

```
self.population = sorted(self.population, key=lambda agent: self.fitness(
			agent), reverse=False)[:self.population_size] 
```


"""

class Problem(Problem):
	def egg_breading(self):
		breaded_eggs = []
		for i in range(self.population_size):
			number_of_eggs = random.randint(2, min(10, self.n) )
			gene = [random.randint(1, self.n - 1) for _ in range(number_of_eggs)]
			while len(set(gene)) < number_of_eggs : 
				gene = [random.randint(1, self.n - 1) for _ in range(number_of_eggs)]
			for j in range(len(gene)):
				joining_node = random.choice([exc for exc in adj[gene[j]] if exc != gene[j] ])
				new_egg_pop = self.population[i][:]
				new_egg_pop[gene[j]] = self.population[i][joining_node]

				breaded_eggs.append(new_egg_pop)
		############## remove 10%
		num_to_remove = round(len(breaded_eggs)/10)
		breaded_eggs = sorted(breaded_eggs, key=lambda agent: self.fitness(agent),
		                      reverse=False)[num_to_remove:] 
		for x in breaded_eggs:
			self.population.append(x)
		############## maintain population 
		self.population = sorted(self.population, key=lambda agent: self.fitness(
			agent), reverse=False)[len(self.population) - self.population_size:]

"""
In this function we will perform the migration task. The best performing chromosome is chosen as the goal. Every other chromosome will move towards it with a predefined probability 


"""

class Problem(Problem): 
	def migration(self):
		goal = self.population[len(self.population)-1]
		#move towards the best chromosome with a preset probibality
		for i in range(0, len(self.population) - 2):
			migration_rate = 0.7
			for j in range(self.n):
				if random.uniform(0, 1) > migration_rate:
					continue;
				self.population[i][j] = goal[j]

"""In this function we will calculate the fitness of the cuckoo given based on the below formula 
![image.png](data:image/png;base64,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)
"""

class Problem(Problem):
	def fitness(self, individual):
		# Calculate the fitness of a chromosome based on the formula provided   

		Q = 0
		for i in range(self.n):
			for j in range(self.n):
				Q += (int(j in self.adj[i]) - ((len(self.adj[i]) * len(self.adj[j])) / (2 * self.m))) * int(individual[i] == individual[j])
		Q /= (2 * self.m)
		return Q

"""This function will calculate the fitness of every chromosome of our population """

class Problem(Problem):
	def evalute(self):
		pop_fit = [None] * len(self.population)
		for i in range(len(self.population)) : pop_fit[i] = self.fitness(self.population[i])
		return sum(pop_fit), max(pop_fit)

"""This function will visulize our answer"""

class Problem(Problem):
	def graph_visulization(self):
		fig2, ax2 = plt.subplots()
		ax2.set_title('Communities')
		G = nx.Graph()	
		G.add_edges_from(self.graph_edge)	
		color_map = [node for node in self.population[-1:]]
		nx.draw_networkx(G, node_color = color_map[0])
		plt.savefig("Communities_graph.png")
                
"""We will commence the cuckoo optimization algorithms. first we will breed the eggs than migrate each chromosome to the best one (base on fitness function)

"""

class Problem(Problem):
	def Cuckoo(self, population_size, n_generations, high_egg, low_egg):
		self.population_size = population_size
		self.n_generations = n_generations

		# Make the random first population 
		self.initial_population()
	
		plotFitness = []
		plotEpoch = []
		plotPopFit = []
		for epoch in range(self.n_generations): 
			# Start laying the eggs - after this function we only have a set of mature eggs 
			self.egg_breading()
			# Start migrating toward the best chromosome
			self.migration()
			eval_ = self.evalute()	
			plotFitness.append(eval_[1])
			plotEpoch.append(epoch)
			plotPopFit.append(eval_[0])  
			with open('output.txt', 'a') as f: 
                                print("Epoch", epoch, ":\tPopulation total fitness:", eval_[0], "\tBest fitness:", eval_[1], file=f)
 
	 
		fig, ax = plt.subplots()
		ax.scatter(plotEpoch, plotPopFit, color = 'r')
		ax.set_title('Population Total Fitness')
		ax.set_xlabel('Generation')
		ax.set_ylabel('Population Total Fitness')
		sns.scatterplot(x=plotEpoch, y=plotPopFit)
		plt.savefig("Population_Total_Fitness.png")
	
		fig1, ax1 = plt.subplots()
		ax1.scatter(plotEpoch, plotFitness, color = 'b')
		ax1.set_title('Population Best Fitness')
		ax1.set_xlabel('Generation')
		ax1.set_ylabel('Population Best Fitness')
		sns.scatterplot(x=plotEpoch, y=plotFitness)
		plt.savefig("Population_Best_Fitness.png")

		self.graph_visulization()

#from google.colab import files 
#uploaded = files.upload()
f = open('sample dataset.txt', 'r')
lines = f.readlines()
n = int(lines[0])
lines = lines[1:]

adj = [[] for _ in range(n)]
graph_edge = []

for edge in lines:
	edge = edge.split()
	graph_edge.append(edge)
 
	adj[int(edge[0]) - 1].append(int(edge[1]) - 1)
	adj[int(edge[1]) - 1].append(int(edge[0]) -1)

# Define problem parameters : Number of nodes, adjacency matrix, array of edges and finlay number of communities
problem = Problem(n, adj, graph_edge, 7)

problem.Cuckoo(population_size = 100, n_generations = 30, high_egg = 5, low_egg = 1)

