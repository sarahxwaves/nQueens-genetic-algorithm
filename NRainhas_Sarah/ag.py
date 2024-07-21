from typing import List
from nQueens import nQueens
import sys
import random


class AlgoritmoGenetico:
    def __init__(self):
        self.__population: List[nQueens] = []
        self.best_generation = None
        self.best_individual = None

    def execute(self, num_geracoes: int, num_individuos: int, elitism: int, num_queens: int):
        # Iniciando população
        for i in range(num_individuos):
            gen = random.sample(list(range(num_queens)), k=num_queens)
            self.__population.append(nQueens(gen, num_queens))

        for gen in range(num_geracoes):
            aux_population: List[nQueens] = []
            aux_population.extend(self.__population)
            aux_population.extend(self.get_children())
            aux_population.extend(self.get_mutations())

            self.__population = aux_population
            # todo: fazer elitismo por fitness
            elite = sorted(self.__population, key=lambda individual: individual.chromosome)[
                :elitism]

            self.selection(num_individuos - elitism)
            self.__population.extend(elite)
            self.print_result(gen)

    def get_children(self):
        parents = self.__population.copy()
        children = []

        for i in range(int(len(self.__population)/2)):
            p1 = parents.pop(random.randint(0, len(parents)-1))
            p2 = parents.pop(random.randint(0, len(parents)-1))
            child = p1.crossover(p2)
            children.extend(child)

        return children

    def get_mutations(self):
        mutations = []
        for individual in self.__population:
            aux_mutation = individual.mutate()
            mutations.append(aux_mutation)

        return mutations

    def selection(self, numIndividuals: int):
        selected_genes = []
        for i in range(numIndividuals):
            selected = random.choice(self.__population)
            selected_genes.append(selected)
        self.__population = selected_genes

    def print_result(self, gen: int):
        best = self.__population[0]
        for individual in self.__population:
            if individual.get_evaluate() <= best.get_evaluate():
                best = individual

    # atualiza a melhor geração e o melhor indivíduo se necessário
    # todo: condicao de parada
        if self.best_individual is None or best.get_evaluate() < self.best_individual.get_evaluate():
            self.best_generation = gen
            self.best_individual = best

        print(
            f'Geração: {gen} Individuo: {best.chromosome} Colisão: {best.fitness}')

    def print_best(self):
        print(
            f'Melhor Geração: {self.best_generation} Individuo: {self.best_individual.chromosome} Colisão: {self.best_individual.fitness}')
