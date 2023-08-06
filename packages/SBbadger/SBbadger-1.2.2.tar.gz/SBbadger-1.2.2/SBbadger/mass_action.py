
# import generate
import generate_serial
from scipy.special import zeta
from scipy.stats import gamma


# def in_dist(k):
#     return k ** (-2) / zeta(2)


def out_dist(k):
    return k ** (-2)

def in_dist(k):
    return k ** (-3)


# def in_dist(k):
#     return gamma.pdf(k, 1.5) + .01
#
#
# def out_dist(k):
#     return gamma.pdf(k, 1.5) + .01


if __name__ == "__main__":

    model = generate_serial.models(

        group_name='mass_action',
        n_models=1,
        n_species=10,
        out_dist=out_dist,
        in_dist=in_dist,
        # out_range=[1, 10],
        # in_range=[1, 9],
        rxn_prob=[1, 0, 0, 0],
        # kinetics=['mass_action', ['loguniform', 'loguniform', 'loguniform'],
        #                          ['kf', 'kr', 'kc'],
        #                          [[0.01, 100], [0.01, 100], [0.01, 100]]],
        # in_flux=2,
        # out_flux=2,
        overwrite=True,
        # rev_prob=.5,
        # ic_params=['uniform', 0, 10],
        # dist_plots=True,
        net_plots='reaction',
        # net_layout='neato',
        connected=True,
        independent_sampling=False,
        # source=[5, 'loguniform', 0.01, 100],
        # sink=[5, 'loguniform', 0.01, 100],
        # add_enzyme=['loguniform', 0.01, 100]
        # n_cpus=1
        # edge_type='metabolic'
        # enforce_mass_balance=True,

    )
