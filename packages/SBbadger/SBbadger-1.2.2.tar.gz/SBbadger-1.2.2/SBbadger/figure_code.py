
import generate
import generate_serial
from scipy.special import zeta
from scipy.stats import zipf

def in_dist(k):
    return k ** (-2) / zeta(2)

def out_dist(k):
    return zipf.pmf(k, 3)

if __name__ == "__main__":

    # model = generate.models(
    model = generate_serial.models(
    # model = generate_serial.model(
    # model = generate.model(
        group_name='example',
        n_models=1,
        n_species=50,
        out_dist=out_dist,
        in_dist=in_dist,
        out_range=[1, 10],
        in_range=[1, 10],
        rxn_prob=[.35, .3, .3, .05],
        kinetics=['mass_action', ['loguniform', 'loguniform', 'loguniform'],
                                 ['kf', 'kr', 'kc'],
                                 [[0.01, 100], [0.01, 100], [0.01, 100]]],
        ic_params=['uniform', 0, 10],
        dist_plots=True,
        net_plots='True',
        net_layout='dot'
    )
