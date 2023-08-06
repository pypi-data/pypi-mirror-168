
import generate
from scipy.special import zeta
import time


def in_dist(k):
    return k ** (-2) / zeta(2)


def out_dist(k):
    return k ** (-3)


if __name__ == "__main__":
    starttime = time.perf_counter()
    print('start', starttime)
    model = generate.models(

        group_name='performance100',
        n_models=1000,
        n_species=100,
        # out_dist=out_dist,
        # in_dist=in_dist,
        # rxn_prob=[.35, .3, .3, .05],
        kinetics=['mass_action', ['loguniform', 'loguniform', 'loguniform'],
                                 ['kf', 'kr', 'kc'],
                                 [[0.01, 100], [0.01, 100], [0.01, 100]]],
        overwrite=True,
        rev_prob=.5,
        ic_params=['uniform', 0, 10],
        # dist_plots=True,
        net_plots='reaction',
        net_layout='neato',
        # connected=True,
        n_cpus=8
        # edge_type='metabolic'
        # enforce_mass_balance=True,

    )
    endtime = time.perf_counter()
    print('end', endtime)
    # print(endtime - starttime)
