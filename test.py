from coop_evolve.population import Population
import pprint
pop = Population(10, 10, 15)

pop[0][0][0].dna.sequence = "aaa"
pop[0][0][1].dna.sequence = "aaa"
pop[0][1][0].dna.sequence = "aaa"
pop[1][0][0].dna.sequence = "aaa"

census = []

for i in range(pop.width):
    for j in range(pop.length):
        for k in range(pop.subpop_size):
            sub_census = {}
            if pop[i][j][k].dna.sequence in sub_census:
                sub_census[pop[i][j][k].dna.sequence] += 1
            else:
                sub_census[pop[i][j][k].dna.sequence] = 1
        for sequence, count in sub_census.items():
            census.append({"x_coord": i, "y_coord": j, "sequence": sequence, "count": count})
            
pp = pprint.PrettyPrinter(indent = 4)

pp.pprint(census)

            