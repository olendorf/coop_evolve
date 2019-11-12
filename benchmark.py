import timeit
import random
from scipy.stats import nbinom
import csv

size = 1000


ns = [1, 10, 100, 1000, 10000, 100000]
reps = 1000

def nbinom_single_val(n):
    ary = []
    for i in range(n):
        ary.append(nbinom.rvs(1, 0.1, size=1))
    return(ary)
    
def nbinom_gen_val():
    num = 0
    while random.random() < 0.1:
        num += 1
    return(num)

def nbinom_manual_array(n):
    ary = []
    for i in range(n):
        ary.append(nbinom_gen_val())
    return(ary)


with open('nbinom_bench.csv', mode='w') as out_file:
    file_writer = csv.writer(out_file, delimiter=',',  quotechar='"')
    
    file_writer.writerow(
                            [
                                "values generated", 
                                "nbinom_single",
                                "nbinom_array",
                                "nbinom_manual"
                            ]
                          )
                          
    for n in ns:
        
        print(f"n: {n}")
        
        print("working on nbinom_array")
        nb_a_call = "nbinom.rvs(1, 0.1, size = " + str(n) + ")"
        nbinom_array = timeit.timeit(
                            nb_a_call, 
                            setup = "from scipy.stats import nbinom",
                            number = reps)
                            
        print("working on nibnom_single")
        nb_s_call = "nbinom_single_val(" + str(n) + ")"
        nbinom_single = timeit.timeit(
                            nb_s_call,
                            setup = "from __main__ import nbinom_single_val",
                            number = reps)
        
        print("working on nbinom_manual")               
        nb_m_call = "nbinom_manual_array(" + str(n) + ")"
        nbinom_manual = timeit.timeit(
                            nb_m_call,
                            setup = "from __main__ import nbinom_manual_array",
                            number = reps)
                            
        file_writer.writerow(
                                [
                                    n,
                                    nbinom_single,
                                    nbinom_array,
                                    nbinom_manual
                                ]
                            )