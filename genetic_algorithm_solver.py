import random

class GeneticAlgorithmSolver:
    def __init__(self, n, population_size=100, generations=1000, mutation_rate=0.01):
        self.n = n
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            chromosome = list(range(self.n))
            random.shuffle(chromosome)
            population.append(chromosome)
        return population

    def calculate_fitness(self, chromosome):
        collisions = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if chromosome[i] == chromosome[j] or abs(chromosome[i] - chromosome[j]) == abs(i - j):
                    collisions += 1
        return 1 / (1 + collisions)  

    def select_parents(self, population, fitnesses):

        total_fitness = sum(fitnesses)
        if total_fitness == 0:
            return random.choices(population, k=2)
        probabilities = [f / total_fitness for f in fitnesses]
        return random.choices(population, weights=probabilities, k=2)

    def crossover(self, parent1, parent2):

        crossover_point = random.randint(1, self.n - 1)
        child1 = parent1[:crossover_point] + [gene for gene in parent2 if gene not in parent1[:crossover_point]]
        child2 = parent2[:crossover_point] + [gene for gene in parent1 if gene not in parent2[:crossover_point]]
        return child1, child2

    def mutate(self, chromosome):
        if random.random() < self.mutation_rate:
            index1, index2 = random.sample(range(self.n), 2)
            chromosome[index1], chromosome[index2] = chromosome[index2], chromosome[index1]
        return chromosome

    def solve(self):
        population = self.initialize_population()
        for generation in range(self.generations):
            fitnesses = [self.calculate_fitness(chromo) for chromo in population]
            best_fitness = max(fitnesses)
            best_chromosome = population[fitnesses.index(best_fitness)]

            if best_fitness == 1:  
                return best_chromosome

            new_population = []
            for _ in range(self.population_size):
                parent1, parent2 = self.select_parents(population, fitnesses)
                child1, child2 = self.crossover(parent1, parent2)
                new_population.append(self.mutate(list(child1))) 
                if len(new_population) < self.population_size:
                    new_population.append(self.mutate(list(child2)))

            population = new_population


        fitnesses = [self.calculate_fitness(chromo) for chromo in population]
        best_fitness = max(fitnesses)
        best_chromosome = population[fitnesses.index(best_fitness)]
        return best_chromosome if best_fitness == 1 else None