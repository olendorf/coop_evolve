from scipy.stats import nbinom

import math

expected_length = 10
pmfs = []
k = 0
nuc_length = 5
deltas = []
while sum(pmfs) <= 0.9999:
    pmf = nbinom.pmf(k, 1, (1 - expected_length/(1 + expected_length)))
    pmfs.append(pmf)
    
    diffs = math.floor(k/2) * (1 - 1/(nuc_length)) * 2
    delta = pmf * diffs
    deltas.append(delta)
    print(f"success: {k}; pmf: {pmf}; cdf: {sum(pmfs)}; pmf_delta: { delta }; cum_delta: {sum(deltas)}")
    k += 1