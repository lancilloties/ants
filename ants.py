# -*- coding: utf-8 -*-

import numpy as np
import random as rand

class Colony:
	class Ant:
		def __init__(self, colony):
			self.colony = colony
			self.pos = rand.randrange(self.colony.n)
			
			self.mem = np.zeros(self.colony.n)
			self.mem[self.pos] = 1
			
			self.path = [self.pos]
			self.cost = 0

		def reset(self, colony):
			self.__init__(colony)

		def __str__(self):
			#TO DO # DONE
			result = "["
			for i in range(len(self.path)):
				result += str(self.path[i])
				if i != len(self.path)-1:
					result += ", "
			return result+"], cost : " + str(self.cost)

		def __lt__(self, other):
			#TO DO # DONE
			if self.cost < other.cost:
				return True
			else:
				return False

		# Returns city to be travelled to from current position
		def policy(self):
			if rand.random() < self.colony.q_0:
				# Deterministic decision
				# TODO # DONE
				winner = None
				winnerValue = None;
				for city in range(len(self.mem)): # Iterate over all cities.
					if self.mem[city] == 0: # Skip cities previously visited.
						if winnerValue is None or (winnerValue < (self.colony.tau[self.pos][city] * (self.colony.eta(self.pos, city) ** self.colony.beta))):
							winner = city
							winnerValue = self.colony.tau[self.pos][city] * (self.colony.eta(self.pos, city) ** self.colony.beta)
				return winner
			else:
				# Stochastic decision
				# TODO # DONE
				# Created tuple array with option & percentage.
				distribution = []
				division_bottom = 0
				
				# Initialize division bottom
				for city in range(len(self.mem)):
					if self.mem[city] == 0:
						division_bottom += (self.colony.tau[self.pos][city] * (self.colony.eta(self.pos, city) ** self.colony.beta))
				
				# Populate distribution
				for city in range(len(self.mem)):
					if self.mem[city] == 0:
						distribution.append(((self.colony.tau[self.pos][city] * (self.colony.eta(self.pos, city) ** self.colony.beta)) / division_bottom,city))
				
				# Select a choice
				choice = rand.random()
				previous_lower_bound = 0
				for i in range(len(distribution)):
					if (choice > previous_lower_bound or previous_lower_bound == 0) and choice <= previous_lower_bound+distribution[i][0]:
						return distribution[i][1]
					previous_lower_bound += distribution[i][0]
				return None

		# Updates the local pheromones and position of ant
		# while keeping track of total cost and path
		def move(self):
			destination = self.policy()
			
			# local updating
			# TODO # DONE
			self.colony.tau[self.pos][destination] = ((1-self.colony.alpha) * self.colony.tau[self.pos][destination]) + (self.colony.alpha * self.colony.tau_0)
			self.colony.tau[destination][self.pos] = ((1-self.colony.alpha) * self.colony.tau[destination][self.pos]) + (self.colony.alpha * self.colony.tau_0)
			self.cost += self.colony.adjMat[self.pos][destination] # They seem to be distances, not edges since none are unique and are repeating.
			if len(self.path)+1 == len(self.mem):
				self.cost += self.colony.adjMat[destination][self.path[0]]
				self.colony.tau[self.path[0]][destination] = ((1-self.colony.alpha) * self.colony.tau[self.path[0]][destination]) + (self.colony.alpha * self.colony.tau_0)
				self.colony.tau[destination][self.path[0]] = ((1-self.colony.alpha) * self.colony.tau[destination][self.path[0]]) + (self.colony.alpha * self.colony.tau_0)
			
			# Change position
			# TODO # DONE
			self.mem[destination] = 1
			self.path.append(destination)
			self.pos = destination
			

		# Updates the pheromone levels of ALL edges that form 
		# the minimum cost loop at each iteration
		def globalUpdate(self):
			# TODO # DONE
			for i in range(len(self.path)):
				if len(self.path)-1-i-1 >= 0: # Prevent outofboundaccess
					from_var = self.path[len(self.path)-1-i]
					to_var = self.path[len(self.path)-1-i-1]
					self.colony.tau[from_var][to_var] = ((1-self.colony.alpha) * self.colony.tau[from_var][to_var]) + (self.colony.alpha / self.cost)
					self.colony.tau[to_var][from_var] = ((1-self.colony.alpha) * self.colony.tau[to_var][from_var]) + (self.colony.alpha / self.cost)
					
			from_var = self.path[len(self.path)-1]
			to_var = self.path[0]
			self.colony.tau[from_var][to_var] = ((1-self.colony.alpha) * self.colony.tau[from_var][to_var]) + (self.colony.alpha / self.cost)
			self.colony.tau[to_var][from_var] = ((1-self.colony.alpha) * self.colony.tau[to_var][from_var]) + (self.colony.alpha / self.cost)
			print(self)

	def __init__(self, adjMat, m=10, beta=2, alpha=0.1, q_0=0.9):
		# Parameters: 
		# m => Number of ants
		# beta => Importance of heuristic function vs pheromone trail
		# alpha => Updating propensity
		# q_0 => Probability of making a non-stochastic decision
		# tau_0 => Initial pheromone level
		
		self.adjMat = adjMat
		self.n = len(adjMat)
		self.tau_0 = 1 / (self.n * self.nearestNearbourHeuristic())
		self.tau = [[self.tau_0 for _ in range(self.n)] for _ in range(self.n)]
		self.ants = [self.Ant(self) for _ in range(m)]
		
		self.beta = beta
		self.alpha = 0.1
		self.q_0 =q_0

	def __str__(self):
		# TODO # DONE
		# We print the best ant path.
		try:
			return str(min(self.ants))
		except:
			return "[]"

	# Returns the cost of the solution produced by 
	# the nearest neighbour heuristix
	def nearestNearbourHeuristic(self):
		costs = np.zeros(self.n)
		
		# TODO # DONE
		for j in range(self.n): # Run this n times.
			init_node = rand.randrange(self.n)
			tmp_node_list = [init_node]
			tmp_mem = np.zeros(self.n)
			tmp_mem[init_node] = 1
			for i in range(self.n): # Run this for the amount of the nodes.
				tmp_low = None
				tmp_selection = None
				for u in range(self.n): # Find new nodes.
					if (tmp_selection is None and tmp_mem[u] != 1) or (tmp_mem[u] != 1 and tmp_node_list[i] != u and self.adjMat[tmp_node_list[i]][u] < tmp_low): # Check if node is closer than the others.
						tmp_low = self.adjMat[tmp_node_list[i]][u]
						tmp_selection = u
				if tmp_selection is not None: # If new node found.
					tmp_node_list.append(tmp_selection)
					tmp_mem[tmp_selection] = 1
					costs[j] += tmp_low
			costs[j] += self.adjMat[tmp_node_list[self.n-1]][tmp_node_list[0]] # The last mile cost.
		
		# Present in the result.txt and was the only place I could find to add it without modifying the squeleton.
		print("Nearest Nearbour Heuristic Cost :  "+str(min(costs)))
		
		return min(costs)

	# Heuristic function
	# Returns inverse of smallest distance between r and u
	def eta(self, r, u):
		# TODO # DONE
		return (1 / (self.adjMat[r][u]))

	def optimize(self, num_iter):
		for _ in range(num_iter):
			for _ in range(self.n-1):
				for ant in self.ants:
					ant.move()
			
			
			min(self.ants).globalUpdate()
			
			for ant in self.ants:
				ant.reset(self)

if __name__ == "__main__":
	rand.seed(420)
	
	#file = open('d198')
	file = open('dantzig.csv')
	# Is a CSV with a list of costs for each node. A big matrix that's symmetric.
	
	adjMat = np.loadtxt(file, delimiter=",")
	ant_colony = Colony(adjMat)
	
	ant_colony.optimize(1000)
	# On prend 40515 iterations pour trouver 700.
