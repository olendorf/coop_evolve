from coop_evolve.population import Population

width = 4
length = 5
subpop_size = 6

pop = Population(width, length, subpop_size)

pop[0][0][0].dna.sequence = "aaaa"
pop[0][0][1].dna.sequence = "aaaa"
pop[0][0][4].dna.sequence = "aaaa"
pop[0][0][5].dna.sequence = "aaaa"
pop[0][1][0].dna.sequence = "aaaa"
pop[0][1][3].dna.sequence = "aaaa"
pop[0][2][0].dna.sequence = "aaaa"
pop[1][0][0].dna.sequence = "aaaa"
pop[1][0][1].dna.sequence = "aaaa"
pop[0][3][0].dna.sequence = "aaaa"

subpop_data = []
pop_data = {}
    

for i in range(width):
    row = []
    for j in range(length):
        seqs = {}
        for k in range(subpop_size):
            if pop[i][j][k].dna.sequence in seqs:
                seqs[pop[i][j][k].dna.sequence] += 1
            else:
                seqs[pop[i][j][k].dna.sequence] = 1
                
            if pop[i][j][k].dna.sequence in pop_data:
                pop_data[pop[i][j][k].dna.sequence] += 1
            else:
                pop_data[pop[i][j][k].dna.sequence] = 1
        row.append(seqs)
    subpop_data.append(row)
    
print(subpop_data)
print(pop_data)
            