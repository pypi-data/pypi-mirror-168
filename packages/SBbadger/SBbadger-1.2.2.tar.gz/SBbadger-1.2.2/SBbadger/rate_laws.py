
import generate_serial


if __name__ == "__main__":

    # output_dir='models/modular_CM/networks',
    generate_serial.rate_laws(

        group_name='modular_CM',
        kinetics=['modular_CM', ['uniform', 'loguniform', 'loguniform', 'loguniform', 'loguniform',
                                 'loguniform', 'loguniform', 'loguniform', 'loguniform'],
                                ['ro', 'kf', 'kr', 'km', 'm',
                                 'kms', 'ms', 'kma', 'ma'],
                                [[0, 1], [0.01, 100], [0.01, 100], [0.01, 100], [0.01, 100],
                                 [0.01, 100], [0.01, 100], [0.01, 100], [0.01, 100]]],

    )

