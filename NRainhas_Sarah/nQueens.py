import random


class nQueens:

    def __init__(self, chromosome: list, nQueens):
        self.nQueens = nQueens
        self.chromosome = chromosome
        self.fitness = 0
        self.evaluated = False

    def crossover(self, individual):
        first_child = self.chromosome[:4]
        second_child = individual.chromosome[:4]

        self.crossover_second_part(individual.chromosome, first_child)
        self.crossover_second_part(self.chromosome, second_child)

        self.checkChromosome(first_child)
        self.checkChromosome(second_child)

        return [nQueens(first_child, self.nQueens), nQueens(second_child, self.nQueens)]

    def crossover_second_part(self, chromosome: list, child: list):
        for i in chromosome[4:]:
            if i not in child:
                child.append(i)
            else:
                child.append(-1)

    # seleciona aleatoriamente dois pontos no cromossomo e troca seus valores
    def mutate(self, rate=0.05):
        mutation = self.chromosome.copy()
        aux_mutation = False

        for mutation_index in range(self.nQueens):
            random_rate = random.random()
            if random_rate >= rate:

                new_chromosome = mutation[mutation_index]

                # gera valor aleatorio diferente do atual
                while new_chromosome == mutation[mutation_index]:
                    new_chromosome = random.randint(0, self.nQueens-1)

                # encontra indice com novo cromossomo e realiza a troca de posicoes
                index = mutation.index(new_chromosome)
                mutation[index] = mutation[mutation_index]
                mutation[mutation_index] = new_chromosome

                aux_mutation = True

        # garante que ocorra pelo menos uma mutacao na geracao
        if not aux_mutation:
            rand_pos = random.randint(0, self.nQueens-1)
            mutation = self.swap(mutation, rand_pos)
        return nQueens(mutation, self.nQueens)

    def swap(self, chromosome, position):
        rand_pos = position
        while rand_pos == position:
            rand_pos = random.randint(0, self.nQueens-1)

        chromosome[position], chromosome[rand_pos] = chromosome[rand_pos], chromosome[position]

        return chromosome

    # eval/colisao = numero de rainhas se atacando
    def evaluateColisions(self):
        eval = 0
        for i in range(self.nQueens):
            # verifica a cada par i+1
            for j in range(i + 1, self.nQueens):
                # distancia da posicao das duas rainhas
                value = abs(j - i)
                # verifica colisao nas linhas e diagonal
                if (self.chromosome[i] == self.chromosome[j] or
                    self.chromosome[i] == self.chromosome[j] - value or
                        self.chromosome[i] == self.chromosome[j] + value):

                    eval += 1
        return eval

    def get_evaluate(self):
        if not self.evaluated:
            self.fitness = self.evaluateColisions()
            self.evaluated = True
        return self.fitness

    # confere se o cromossomo possui todos os valores possíveis (0 a nQueens - 1) sem duplicacao
    def checkChromosome(self, chromosome: list):
        check = []

        for i in range(len(chromosome)):
            try:
                chromosome.index(i)
            except ValueError:
                check.append(i)

        while len(check) != 0:
            rand = random.randint(0, len(check)-1)
            index = chromosome.index(-1)
            checked_value = check.pop(rand)
            chromosome.pop(index)

            chromosome.insert(index, checked_value)
