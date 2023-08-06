
import os
import generate
# import generateDistributions
from math import exp
from scipy.special import zeta
import numpy as np
from scipy.stats import zipf
import time


def in_dist(k):
    return k**(-2) / zeta(2)


def out_dist(k):
    return k**(-2) / zeta(2)

# def out_dist(k):
#     return zipf.pmf(k, 3)


def function_test(n_models):
    generate.models(

        # group_name='none_800_ma_mp_1',
        # group_name='inPLa2_800_ma_mp_1',
        group_name='test',
        n_models=n_models,
        n_species=20,
        out_dist=out_dist,
        in_dist=in_dist,
        # kinetics=['mass_action', 'loguniform', ['kf', 'kr', 'kc'], [[0.01, 100], [0.01, 100], [0.01, 100]]],
        overwrite=True,
        # ic_params=['uniform', 0, 10],
        dist_plots=True,
        net_plots=True
    )


# if __name__ == "__main__":

start = time.time()

function_test(10)

finish = time.time()
elapsed = finish-start
# print(elapsed)

