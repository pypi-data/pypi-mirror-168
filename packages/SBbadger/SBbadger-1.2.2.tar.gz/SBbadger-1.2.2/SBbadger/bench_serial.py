
import os
import generate_serial
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


# if __name__ == "__main__":

start = time.time()

model = generate_serial.models(

    # group_name='none_800_ma_mp_1',
    # group_name='inPLa2_800_ma_mp_1',
    group_name='test',
    # n_models=10,
    n_species=20,
    out_dist=out_dist,
    in_dist=in_dist,
    rxn_prob=[.5, 0, 0, .5],
    # kinetics=['mass_action', 'loguniform', ['kf', 'kr', 'kc'], [[0.01, 100], [0.01, 100], [0.01, 100]]],
    # kinetics=['gma', 'loguniform', ['kf', 'kr', 'kc', 'ko', 'kor'], [[0.01, 100], [0.01, 100], [0.01, 100],
    #                                                                  [0.01, 100], [0.01, 100]]],
    kinetics=['gma', 'lognormal', ['kf', 'kr', 'kc', 'ko', 'kor'], [[0.01, 1], [0.01, 1], [0.01, 1],
                                                                    [0.01, 1], [1, 1]]],
    gma_reg=[[.1, .9, 0, 0], .5],
    overwrite=True,
    rev_prob=.5,
    # ic_params=['uniform', 0, 10],
    # dist_plots=True,
    # net_plots=True

)

print(model)

finish = time.time()
elapsed = finish-start
# print(elapsed)
