
import generate_serial_orders
from scipy.special import zeta


def in_dist(k):
    return k ** (-2) / zeta(2)


def out_dist(k):
    return k ** (-3)


if __name__ == "__main__":

    model = generate_serial_orders.models(

        group_name='mass_action',
        n_models=1,
        n_species=100,
        out_dist=out_dist,
        in_dist=in_dist,
        rxn_orders=[1, 3, 1, 3],
        kinetics=['mass_action', ['loguniform', 'loguniform', 'loguniform'],
                                 ['kf', 'kr', 'kc'],
                                 [[0.01, 100], [0.01, 100], [0.01, 100]]],
        overwrite=True,
        rev_prob=.5,
        ic_params=['uniform', 0, 10],
        dist_plots=True,
        net_plots='reaction',
        net_layout='neato',
        connected=True,
        reg=[3, .5]
        # edge_type='metabolic'
        # enforce_mass_balance=True,

    )
