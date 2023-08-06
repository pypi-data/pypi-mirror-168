
import tellurium as te
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

model_file = 'mass_action_0.txt'
model_str = ''

with open('models/mass_action/antimony/' + model_file) as model:
    lines = model.readlines()
    for line in lines:
        model_str += line

r = te.loada(model_str)

# r = te.loada('''
# A -> B; A
# B -> A; 2*B
# A = 1
# '''
# )

# print(r.getScaledFluxControlCoefficientMatrix())
sim = r.simulate(0, 100, 101)
print(sim)
# print(r.getScaledFluxControlCoefficientMatrix())

r.plot()
