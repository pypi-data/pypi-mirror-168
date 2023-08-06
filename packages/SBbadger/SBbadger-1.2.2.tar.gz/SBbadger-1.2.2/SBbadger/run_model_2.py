
import tellurium as te
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

model_file = 'sindy_bench_1.txt'
model_str = ''

with open('oscillators/' + model_file) as model:
    lines = model.readlines()
    for line in lines:
        model_str += line

# print(model_str)
r = te.loada(model_str)

sim = r.simulate(0, 10, 1000, selections=['time', 'S1', 'S2', 'S3', 'S4', 'S5', 'S8', 'S9'])
# sim = r.simulate(0, 10, 1000)
print(sim)
# r.plot()
# quit()
# print(sim)
t = sim['time']
# s0 = sim['S0']
s1 = sim['S1']
s2 = sim['S2']
s3 = sim['S3']
s4 = sim['S4']
s5 = sim['S5']
# s6 = sim['S6']
# s7 = sim['S7']
s8 = sim['S8']
s9 = sim['S9']

# NUM_COLORS = 20

# cm = plt.get_cmap('nipy_spectral')
# fig = plt.figure(figsize=(16, 12))
fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.set_prop_cycle(color=[cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])

# plt.plot(t, s0)
plt.plot(t, s1)
plt.plot(t, s2)
plt.plot(t, s3)
plt.plot(t, s4)
plt.plot(t, s5)
# plt.plot(t, s6)
# plt.plot(t, s7)
plt.plot(t, s8)
plt.plot(t, s9)


# plt.xlabel('Time', fontsize=16)
# plt.ylabel('Concentration', fontsize=16)
# plt.xticks(fontsize=16)
# plt.yticks(fontsize=16)

plt.xlabel('Time')
plt.ylabel('Concentration')

plt.tight_layout()

# plt.legend(['S1', 'S2', 'S3', 'S4', 'S5', 'S8', 'S9'],
#            ncol=2, fontsize=16)

plt.legend(['S1', 'S2', 'S3', 'S4', 'S5', 'S8', 'S9'],
           ncol=2)

plt.show()


