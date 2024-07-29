from ag import AlgoritmoGenetico

ag = AlgoritmoGenetico()
numGeracoes = 200
numIndividuos = 1000
numQueens = 12
numElitismo = 8

ag.execute(numGeracoes,
           numIndividuos,
           numElitismo,
           numQueens,
           )
ag.print_best()
