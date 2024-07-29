from typing import List
from nQueens import nQueens
import sys
import random


class AlgoritmoGenetico:
    def __init__(self):
        self.__population: List[nQueens] = []
        self.best_generation = None
        self.best_individual = None
        # contador de gerações sem melhoria
        self.generations_without_improvement = 0
        self.best_result_find = False

    def execute(self, num_geracoes: int, num_individuos: int, elitism: int, num_queens: int):

        # max_generations_without_improvement = 20 #Limite de gerações sem melhoria permitido
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
            # elite = sorted(self.__population, key=lambda individual: individual.chromosome)[
            #     :elitism]
            elite = sorted(self.__population, key=lambda individual: individual.get_evaluate())[
                :elitism]

            self.selection(num_individuos - elitism)
            self.__population.extend(elite)
            self.print_result(gen)
            # Verifica se uma solução perfeita foi encontrada
            if self.best_individual.fitness == 0:
                self.best_result_find = True
                print(
                    f'Solução perfeita: {self.best_generation} Individuo: {self.best_individual.chromosome} Colisão: {self.best_individual.fitness}')
                break

           # Verifica condição de parada
            # best_current_individual = min(
            #     self.__population, key=lambda individual: individual.get_evaluate())
            # if self.best_individual is not None and best_current_individual.get_evaluate() >= self.best_individual.get_evaluate():
            #     self.generations_without_improvement += 1
            # else:
            #     self.best_individual = best_current_individual
            #     self.generations_without_improvement = 0

    def get_children(self):
        parents = self.__population.copy()
        children = []

        for i in range(int(len(self.__population)/2)):
            p1 = parents.pop(random.randint(0, len(parents)-1))
            p2 = parents.pop(random.randint(0, len(parents)-1))
            child = p1.crossover(p2)
            children.extend(child)
            # força mutação se o filho for igual a qualquer um dos pais
        while any(s.chromosome == p1.chromosome or s.chromosome == p2.chromosome for s in child):
            child = [s.mutate() for s in child]

        children.extend(child)

        return children

    def get_mutations(self):
        mutations = []
        for individual in self.__population:
            aux_mutation = individual.mutate()
            mutations.append(aux_mutation)

        return mutations

    # calcula fitness total
    def evaluation(self):
        total = 0
        for individual in self.__population:
            total += 1/(individual.get_evaluate()+0.1)
        return total

    # selecao roleta
    def selection(self, numIndividuals: int):
        selected_genes = []
        total = self.evaluation()

        for i in range(numIndividuals):
            rand = random.uniform(0, total)
            value = self.wheel(rand)
            selected_genes.append(value)

        self.__population = selected_genes

    # roleta
    def wheel(self, sortedIndividual):
        selected = None
        sum = 0

        for individual in self.__population:
            # soma fitness individuos ate que seja maior ou igual ao individuo sorteado
            sum += 1/(individual.get_evaluate()+0.1)
            # chegamos no ponto da roleta onde está o individuo?
            if sum >= sortedIndividual:
                selected = individual
                break

        return selected

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
        if not self.best_result_find:
            print(
                f'Melhor Geração: {self.best_generation} Individuo: {self.best_individual.chromosome} Colisão: {self.best_individual.fitness}')
