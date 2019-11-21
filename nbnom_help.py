from scipy.stats import nbinom

pmfs = []
k = 0
f = open("nbinom_pmf.csv", "w")
f.write("k, pmf, cmf\n")
while sum(pmfs) < 0.9999:
    pmf = nbinom.pmf(k, 1, 1 - 10/11)
    pmfs.append(pmf)
    f.write(f"{k}, {pmf}, {sum(pmfs)}\n")
    k += 1
    