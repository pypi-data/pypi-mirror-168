
import numpy as np
from scipy.optimize import linprog

# print(linprog(c=[0., 0., 0.],
#     A_eq=[[.5, .3, .2], [.4, 6, .3], [.2, .3, .5], [1., 1., 1.]],
#     b_eq=[0., 0., 0., 1.],
#     bounds=(0, None)))

A = np.array([[-1, 2, 0], [-2, 0, 1], [0, 1, 1]])
b = np.zeros(A.shape[0])
c = np.ones(A.shape[1])
ulb = (1, None)
print(A.shape)

res = linprog(c, A_eq=A, b_eq=b, bounds=ulb)
print(res)
print(res.success)

# mass_equivalence_species = defaultdict(list)
# mass_equivalence_value = defaultdict(list)

# def equivalence_update(update):
#     if update not in mass_equivalence[update[0]]:
#         # print('update', update)
#         mass_equivalence[update[0]].append(deepcopy(update))
#         mass_equivalence[update[1][1]].append([update[1][1],
#                                                [1/update[1][0], update[0]]])
#
#         print()
#         for item in mass_equivalence:
#             print(item, mass_equivalence[item])
#         print()
#
#         update_list1 = []
#         for item in mass_equivalence[update[0]]:
#             if item[1][1] != update[1][1]:
#                 update_list1.append(item)
#
#         for item in update_list1:
#
#             if [item[1][1], [update[1][0]/item[1][0], update[1][1]]] not in mass_equivalence[item[1][1]]:
#                 mass_equivalence[item[1][1]].append([item[1][1], [update[1][0]/item[1][0], update[1][1]]])
#
#             if [update[1][1], [item[1][0]/update[1][0], item[1][1]]] not in mass_equivalence[update[1][1]]:
#                 mass_equivalence[update[1][1]].append([update[1][1], [item[1][0]/update[1][0], item[1][1]]])
#
#         update_list2 = []
#         for item in mass_equivalence[update[1][1]]:
#             if item[1][1] != update[0]:
#                 update_list2.append(item)
#
#         for item in update_list2:
#
#             if [update[0], [update[1][0] * item[1][0], item[1][1]]] not in mass_equivalence[update[0]]:
#                 mass_equivalence[update[0]].append([update[0], [update[1][0] * item[1][0], item[1][1]]])
#
#             if [item[1][1], [1 / (update[1][0] * item[1][0]), update[0]]] not in mass_equivalence[item[1][1]]:
#                 mass_equivalence[item[1][1]].append([item[1][1], [1 / (update[1][0] * item[1][0]), update[0]]])
#
#         print('ul1', update_list1)
#         print('ul2', update_list2)
#         print()
#         for item in mass_equivalence:
#             print(item, mass_equivalence[item])
#                 # print(item, every)
#                 # if every[1][1] == update[0]:
#
#         print('--------------------------------------------')

# changed = True
# while changed:
#
# for item in mass_equivalence[update[1][1]]:
#     update_iter = deepcopy(item)
#     update_iter[0] = update[0]
#     update_iter[1][0] = update_iter[1][0] * update[1][0]
#     equivalence_update(update_iter)

# def consistency_check(reactants, products):
#     # print(reactants, products)
#     equivalences = []
#     if len(reactants) == 1 and len(products) == 1:
#         equivalences.append([reactants[0], products[0], 1])
#     test_pass = True
#     for test in equivalences:
#         for j, item in enumerate(mass_equivalence_species[test[0]]):
#             if item[1] == test[1][1] and item[0] != test[1][0]:
#                 test_pass = False
#                 break
#             if not test_pass:
#                 break
#     if test_pass:
#         for test in tests:
#             # print('test', test)
#             equivalence_update(test)
#
#     return test_pass




# def generate_samples(n_species, in_dist, out_dist, joint_dist, min_node_deg, in_range, out_range,
#                      joint_range):
#
#     in_samples = []
#     out_samples = []
#     joint_samples = []
#
#     def single_unbounded_pmf(sdist):
#         """Assumes starting degree of 1 and extends until cutoff found"""
#
#         deg = 1
#         while True:
#             dist0 = []
#             for j in range(deg):
#                 dist0.append(sdist(j + 1))
#             distsum = sum(dist0)
#             dist_n = [x * n_species / distsum for x in dist0]
#             if any(elem < min_node_deg for elem in dist_n[:-1]) and dist_n[-1] >= min_node_deg:
#                 raise Exception("\nThe provided distribution is invalid; consider revising.")
#             elif dist_n[-1] < min_node_deg:
#                 pmf0 = dist0[:-1]
#                 sum_dist_f = sum(pmf0)
#                 pmf0 = [x / sum_dist_f for x in pmf0]
#                 break
#             else:
#                 deg += 1
#
#         pmf_range = [i + 1 for i, each in enumerate(pmf0)]
#
#         return pmf0, pmf_range
#
#     def single_bounded_pmf(sdist, drange):
#         """Start with given degree range and trim until cutoffs found"""
#
#         dist_ind = [j for j in range(drange[0], drange[1] + 1)]
#         pmf0 = [sdist(j) for j in range(drange[0], drange[1] + 1)]
#         dist_sum = sum(pmf0)
#         pmf0 = [x / dist_sum for x in pmf0]
#         dist0 = [x * n_species for x in pmf0]
#
#         while any(freq < 1 for freq in dist0):
#
#             min_ind = pmf0.index(min(pmf0))
#             del dist_ind[min_ind]
#             del pmf0[min_ind]
#             dist_sum = sum(pmf0)
#             pmf0 = [x / dist_sum for x in pmf0]
#             dist0 = [x * n_species for x in pmf0]
#
#         return pmf0, dist_ind
#
#     def sample_single_pmf(pmf0, drange):
#
#         samplest = [0 for _ in pmf0]
#         outind = [j for j in range(len(pmf0))]
#
#         j = 0
#         while j < n_species:
#             ind = random.choices(outind, pmf0)[0]
#             samplest[ind] += 1
#             j += 1
#
#         samples = []
#         for j in range(len(pmf0)):
#             if samplest[j] > 0:
#                 samples.append((drange[j], samplest[j]))
#
#         return samples
#
#     def sample_both_pmfs(pmf01, drange1, pmf02, drange2):
#
#         ind1 = [j for j in range(len(pmf01))]
#         ind2 = [j for j in range(len(pmf02))]
#
#         num_tries = 0
#         while True:
#
#             samples1t = [0 for _ in pmf01]
#
#             j = 0
#             while j < n_species:
#                 ind = random.choices(ind1, pmf01)[0]
#                 samples1t[ind] += 1
#                 j += 1
#
#             samples1 = []
#             for j in range(len(pmf01)):
#                 if samples1t[j] > 0:
#                     samples1.append((drange1[j], samples1t[j]))
#
#             edges1 = 0
#             for item in samples1:
#                 edges1 += item[0] * item[1]
#
#             num_tries += 1
#             edges2 = 0
#             nodes = 0
#             samples2t = [0 for _ in pmf02]
#
#             while edges2 < edges1 and nodes < n_species:
#                 ind = random.choices(ind2, pmf02)[0]
#                 samples2t[ind] += 1
#                 edges2 += drange2[ind]
#                 nodes += 1
#
#             if edges2 == edges1:
#                 samples2 = []
#                 for j in range(len(pmf02)):
#                     if samples2t[j] > 0:
#                         samples2.append((drange2[j], samples2t[j]))
#                 break
#
#             if num_tries == 10000:
#                 raise Exception("\nReconciliation of the input and output distributions was attempted 10000 times.\n"
#                       "Consider revising these distributions.")
#
#         return samples1, samples2
#
#     def find_edge_count(dist0):
#
#         edge_count = 0
#         for item in dist0:
#             edge_count += item[0] * item[1]
#
#         return edge_count
#
#     def find_edges_expected_value(x_dist, x_range, num_species=n_species):
#
#         edge_ev = 0
#         for j, item in enumerate(x_dist):
#             if isinstance(x_range, list):
#                 edge_ev += item * x_range[j] * num_species
#             elif isinstance(x_range, int):
#                 edge_ev += item * (j + x_range) * num_species
#             else:
#                 edge_ev += item * (j+1) * num_species
#
#         return edge_ev
#
#     def trim_pmf_general(edge_count_target, dist0, dist_range=None):
#
#         if not dist_range:
#             dist_range = [i + 1 for i in range(len(dist0))]
#
#         edge_ev = find_edges_expected_value(dist0, dist_range)
#         reduced_species = deepcopy(n_species)
#
#         dist_0 = None
#         dist_range_0 = None
#         edge_ev_0 = None
#
#         while edge_ev > edge_count_target:
#
#             dist_0 = deepcopy(dist0)
#             dist_range_0 = deepcopy(dist_range)
#             edge_ev_0 = deepcopy(edge_ev)
#             reduced_species -= 1
#             freqs = [reduced_species * dist0[i] for i in range(len(dist0))]
#
#             while any(freq < min_node_deg for freq in freqs):
#                 rm_ind = freqs.index(min(freqs))
#                 del dist0[rm_ind]
#                 del dist_range[rm_ind]
#                 dist_sum = sum(dist0)
#                 dist0 = [dist0[i]/dist_sum for i in range(len(dist0))]
#                 freqs = [reduced_species * dist0[i] for i in range(len(dist0))]
#
#             edge_ev = find_edges_expected_value(dist0, dist_range, reduced_species)
#
#         if abs(edge_ev - edge_count_target) < abs(edge_ev_0 - edge_count_target):
#
#             return dist0, dist_range
#
#         if abs(edge_ev - edge_count_target) >= abs(edge_ev_0 - edge_count_target):
#
#             return dist_0, dist_range_0
#
#     def joint_unbounded_pmf(joint_dist1):
#
#         dist0 = [(1, 1)]
#         dscores = [joint_dist1(1, 1)]
#         dsum = dscores[-1]
#         edge = []
#         edge_scores = []
#
#         while True:
#
#             for item in dist0:
#                 item1 = (item[0] + 1, item[1])
#                 item2 = (item[0], item[1] + 1)
#                 item3 = (item[0] + 1, item[1] + 1)
#                 if item1 not in dist0 and item1 not in edge:
#                     edge.append(item1)
#                     edge_scores.append(joint_dist1(item1[0], item1[1]))
#                 if item2 not in dist0 and item2 not in edge:
#                     edge.append(item2)
#                     edge_scores.append(joint_dist1(item2[0], item2[1]))
#                 if item3 not in dist0 and item3 not in edge:
#                     edge.append(item3)
#                     edge_scores.append(joint_dist1(item3[0], item3[1]))
#
#             tiles = []
#             low_score = 0
#             for j, item in enumerate(edge_scores):
#                 if item == low_score:
#                     tiles.append(j)
#                 elif item > low_score:
#                     tiles = [j]
#                     low_score = item
#
#             new_dist = deepcopy(dist0)
#             new_dscores = deepcopy(dscores)
#
#             for j in tiles:
#                 new_dist.append(edge[j])
#                 new_dscores.append(joint_dist1(edge[j][0], edge[j][1]))
#                 dsum += joint_dist1(edge[j][0], edge[j][1])
#
#             scaled_dscores = []
#             for item in new_dscores:
#                 scaled_dscores.append(n_species * item / dsum)
#
#             if any(x < min_node_deg for x in scaled_dscores[:len(dist0)]):
#                 raise Exception("\nThe provided distribution appears to be malformed; consider revising.")
#             if any(x < min_node_deg for x in scaled_dscores[len(dist0):]):
#                 break
#
#             dist0 = new_dist
#             dscores = new_dscores
#
#             new_edge = []
#             new_edge_scores = []
#
#             for j, item in enumerate(edge):
#                 if j not in tiles:
#                     new_edge.append(item)
#                     new_edge_scores.append(edge_scores[j])
#
#             edge = new_edge
#             edge_scores = new_edge_scores
#
#         joint_pmf = []
#         dsum = sum(dscores)
#         for j, item in enumerate(dist0):
#             joint_pmf.append([item[0], item[1], dscores[j] / dsum])
#
#         return joint_pmf
#
#     def sample_joint(joint_pmf):
#
#         cells, joint_pmf = [[x[0], x[1]] for x in joint_pmf], [x[2] for x in joint_pmf]
#
#         ind = [j for j, item in enumerate(joint_pmf)]
#
#         count = 0
#         while True:
#             count += 1
#             samplest = [0 for _ in joint_pmf]
#             j = 0
#             while j < n_species:
#                 sample = random.choices(ind, joint_pmf)[0]
#                 samplest[sample] += 1
#                 j += 1
#
#             out_edges = 0
#             in_edges = 0
#             samples = []
#             for j, item in enumerate(samplest):
#
#                 out_edges += item*cells[j][0]
#                 in_edges += item*cells[j][1]
#                 samples.append((cells[j][0], cells[j][1], item))
#
#             if out_edges == in_edges:
#
#                 return samples
#
#             if count == 10000:
#                 raise Exception("\nYour joint distribution was sampled 10000 times.\n"
#                                 "Reconciliation of the outgoing and incoming edges was not achieved.\n"
#                                 "Consider revising this distribution.")
#
#     def joint_bounded_pmf(joint_dist1, joint_range1):
#
#         joint_pmf = []
#
#         for j in range(joint_range1[0], joint_range1[1]+1):
#             for k in range(joint_range1[0], joint_range1[1]+1):
#                 joint_pmf.append([joint_dist1(j, k), 0., (j, k)])
#
#         pmf_sum = sum(joint_pmf[j][0] for j in range(len(joint_pmf)))
#         joint_pmf = [[joint_pmf[j][0]/pmf_sum, joint_pmf[j][0]*n_species/pmf_sum, joint_pmf[j][2]]
#                      for j in range(len(joint_pmf))]
#         joint_pmf.sort(key=lambda x: x[1])
#
#         while joint_pmf[0][1] < min_node_deg:
#             value = joint_pmf[0][1]
#             joint_pmf = [x for x in joint_pmf if x[1] != value]
#             pmf_sum = sum(joint_pmf[j][0] for j in range(len(joint_pmf)))
#             joint_pmf = [[joint_pmf[j][0]/pmf_sum, joint_pmf[j][0]*n_species/pmf_sum, joint_pmf[j][2]]
#                          for j in range(len(joint_pmf))]
#
#         joint_pmf_temp = []
#         for item in joint_pmf:
#             joint_pmf_temp.append([item[2][0], item[2][1], item[0]])
#         joint_pmf = joint_pmf_temp
#
#         return joint_pmf
#
#     input_case = None
#
#     if out_dist == 'random' and in_dist == 'random':
#         input_case = 0
#
#     if callable(out_dist) and in_dist == 'random' and out_range is None:
#         input_case = 1
#
#     if callable(out_dist) and in_dist == 'random' and isinstance(out_range, list):
#         input_case = 2
#
#     if isinstance(out_dist, list) and in_dist == 'random' and all(isinstance(x[1], float) for x in out_dist):
#         input_case = 3
#
#     if isinstance(out_dist, list) and in_dist == 'random' and all(isinstance(x[1], int) for x in out_dist):
#         input_case = 4
#
#     if out_dist == 'random' and callable(in_dist) and in_range is None:
#         input_case = 5
#
#     if out_dist == 'random' and callable(in_dist) and isinstance(in_range, list):
#         input_case = 6
#
#     if out_dist == 'random' and isinstance(in_dist, list) and all(isinstance(x[1], float) for x in in_dist):
#         input_case = 7
#
#     if out_dist == 'random' and isinstance(in_dist, list) and all(isinstance(x[1], int) for x in in_dist):
#         input_case = 8
#
#     if callable(out_dist) and callable(in_dist):
#
#         if in_dist == out_dist and in_range is None and out_range is None:
#             input_case = 9
#         if in_dist == out_dist and in_range and in_range == out_range:
#             input_case = 10
#         if in_dist == out_dist and in_range != out_range:
#             input_case = 11
#         if in_dist != out_dist and in_range is None and out_range is None:
#             input_case = 12
#         if in_dist != out_dist and in_range and in_range == out_range:
#             input_case = 13
#         if in_dist != out_dist and in_range != out_range:
#             input_case = 14
#
#     if isinstance(out_dist, list) and isinstance(in_dist, list):
#         if all(isinstance(x[1], int) for x in out_dist) and all(isinstance(x[1], int) for x in in_dist):
#             input_case = 15
#         if all(isinstance(x[1], float) for x in out_dist) and all(isinstance(x[1], float) for x in in_dist):
#             input_case = 16
#
#     if callable(joint_dist):
#         if not joint_range:
#             input_case = 17
#         if joint_range:
#             input_case = 18
#
#     if isinstance(joint_dist, list):
#         if all(isinstance(x[2], float) for x in joint_dist):
#             input_case = 19
#         if all(isinstance(x[2], int) for x in joint_dist):
#             input_case = 20
#
#     # ---------------------------------------------------------------------------
#
#     if input_case == 1:
#
#         pmf_out, range_out = single_unbounded_pmf(out_dist)
#         out_samples = sample_single_pmf(pmf_out, range_out)
#
#     if input_case == 2:
#
#         pmf_out, range_out = single_bounded_pmf(out_dist, out_range)
#         out_samples = sample_single_pmf(pmf_out, range_out)
#
#     if input_case == 3:
#
#         pmf_out = [x[1] for x in out_dist]
#         range_out = [x[0] for x in out_dist]
#
#         out_samples = sample_single_pmf(pmf_out, range_out)
#
#     if input_case == 4:
#         out_samples = out_dist
#
#     if input_case == 5:
#
#         pmf_in, range_in = single_unbounded_pmf(in_dist)
#         in_samples = sample_single_pmf(pmf_in, range_in)
#
#     if input_case == 6:
#
#         pmf_in, range_in = single_bounded_pmf(in_dist, in_range)
#         in_samples = sample_single_pmf(pmf_in, range_in)
#
#     if input_case == 7:
#
#         pmf_in = [x[1] for x in in_dist]
#         range_in = [x[0] for x in in_dist]
#
#         in_samples = sample_single_pmf(pmf_in, range_in)
#
#     if input_case == 8:
#         in_samples = in_dist
#
#     if input_case == 9:
#
#         pmf_out, range_out = single_unbounded_pmf(out_dist)
#         pmf_in, range_in = single_unbounded_pmf(in_dist)
#         in_or_out = random.randint(0, 1)  # choose which distribution is guaranteed n_species
#         if in_or_out:
#             in_samples, out_samples = sample_both_pmfs(pmf_in, range_in, pmf_out, range_out)
#         else:
#             out_samples, in_samples = sample_both_pmfs(pmf_out, range_out, pmf_in, range_in)
#
#     if input_case == 10:
#
#         pmf_out, range_out = single_bounded_pmf(out_dist, out_range)
#         pmf_in, range_in = single_bounded_pmf(in_dist, in_range)
#         in_or_out = random.randint(0, 1)  # choose which distribution is guaranteed n_species
#         if in_or_out:
#             in_samples, out_samples = sample_both_pmfs(pmf_in, range_in, pmf_out, range_out)
#         else:
#             out_samples, in_samples = sample_both_pmfs(pmf_out, range_out, pmf_in, range_in)
#
#     if input_case == 11:
#
#         pmf_out, range_out = single_bounded_pmf(out_dist, out_range)
#         pmf_in, range_in = single_bounded_pmf(in_dist, in_range)
#
#         edge_ev_out = find_edges_expected_value(pmf_out, out_range)
#         edge_ev_in = find_edges_expected_value(pmf_in, in_range)
#
#         if edge_ev_in < edge_ev_out:
#             pmf_out, range_out = trim_pmf_general(edge_ev_in, pmf_out)
#             in_samples, out_samples = sample_both_pmfs(pmf_in, range_in, pmf_out, range_out)
#
#         if edge_ev_in > edge_ev_out:
#             pmf_in, range_in = trim_pmf_general(edge_ev_out, pmf_in)
#
#             out_samples, in_samples = sample_both_pmfs(pmf_out, range_out, pmf_in, range_in)
#
#         if edge_ev_in == edge_ev_out:
#             out_samples, in_samples = sample_both_pmfs(pmf_out, range_out, pmf_in, range_in)
#
#     if input_case == 12:
#
#         pmf_out, range_out = single_unbounded_pmf(out_dist)
#         pmf_in, range_in = single_unbounded_pmf(in_dist)
#
#         edge_ev_out = find_edges_expected_value(pmf_out, out_range)
#         edge_ev_in = find_edges_expected_value(pmf_in, in_range)
#
#         if edge_ev_in < edge_ev_out:
#             pmf_out, range_out = trim_pmf_general(edge_ev_in, pmf_out)
#             in_samples, out_samples = sample_both_pmfs(pmf_in, range_in, pmf_out, range_out)
#
#         if edge_ev_in > edge_ev_out:
#             pmf_in, range_in = trim_pmf_general(edge_ev_out, pmf_in)
#
#             out_samples, in_samples = sample_both_pmfs(pmf_out, range_out, pmf_in, range_in)
#
#         if edge_ev_in == edge_ev_out:
#             out_samples, in_samples = sample_both_pmfs(pmf_out, range_out, pmf_in, range_in)
#
#     if input_case == 13:
#         pmf_out, range_out = single_bounded_pmf(out_dist, out_range)
#         pmf_in, range_in = single_bounded_pmf(in_dist, in_range)
#
#         edge_ev_out = find_edges_expected_value(pmf_out, range_out)
#         edge_ev_in = find_edges_expected_value(pmf_in, range_in)
#
#         if edge_ev_in < edge_ev_out:
#
#             pmf_out, range_out = trim_pmf_general(edge_ev_in, pmf_out, range_out)
#             in_samples, out_samples = sample_both_pmfs(pmf_in, range_in, pmf_out, range_out)
#         if edge_ev_in > edge_ev_out:
#             pmf_in, in_range = trim_pmf_general(edge_ev_out, pmf_in, range_in)
#             out_samples, in_samples = sample_both_pmfs(pmf_out, range_out, pmf_in, range_in)
#         if edge_ev_in == edge_ev_out:
#             out_samples, in_samples = sample_both_pmfs(pmf_out, range_out, pmf_in, range_in)
#
#     if input_case == 14:
#
#         pmf_out, range_out = single_bounded_pmf(out_dist, out_range)
#         pmf_in, range_in = single_bounded_pmf(in_dist, in_range)
#
#         edge_ev_out = find_edges_expected_value(pmf_out, out_range)
#         edge_ev_in = find_edges_expected_value(pmf_in, in_range)
#
#         if edge_ev_in < edge_ev_out:
#             pmf_out, range_out = trim_pmf_general(edge_ev_in, pmf_out)
#             in_samples, out_samples = sample_both_pmfs(pmf_in, range_in, pmf_out, range_out)
#
#         if edge_ev_in > edge_ev_out:
#             pmf_in, range_in = trim_pmf_general(edge_ev_out, pmf_in)
#
#             out_samples, in_samples = sample_both_pmfs(pmf_out, range_out, pmf_in, range_in)
#
#         if edge_ev_in == edge_ev_out:
#             out_samples, in_samples = sample_both_pmfs(pmf_out, range_out, pmf_in, range_in)
#
#     if input_case == 15:
#
#         if find_edge_count(out_dist) != find_edge_count(in_dist):
#             raise Exception("The edges counts for the input and output distributions must match.")
#
#         out_samples = out_dist
#         in_samples = in_dist
#
#     if input_case == 16:
#
#         pmf_out = [x[1] for x in out_dist]
#         pmf_in = [x[1] for x in in_dist]
#
#         range_out = [x[0] for x in out_dist]
#         range_in = [x[0] for x in in_dist]
#
#         edge_ev_out = find_edges_expected_value(pmf_out, range_out)
#         edge_ev_in = find_edges_expected_value(pmf_in, range_in)
#
#         if edge_ev_in < edge_ev_out:
#             pmf_out, range_out = trim_pmf_general(edge_ev_in, pmf_out, range_out)
#             in_samples, out_samples = sample_both_pmfs(pmf_in, range_in, pmf_out, range_out)
#         if edge_ev_in > edge_ev_out:
#             pmf_in, range_in = trim_pmf_general(edge_ev_out, pmf_in, range_in)
#             out_samples, in_samples = sample_both_pmfs(pmf_out, range_out, pmf_in, range_in)
#
#     if input_case == 17:
#
#         pmf = joint_unbounded_pmf(joint_dist)
#         joint_samples = sample_joint(pmf)
#
#     if input_case == 18:
#
#         pmf = joint_bounded_pmf(joint_dist, joint_range)
#         joint_samples = sample_joint(pmf)
#
#     if input_case == 19:
#
#         joint_samples = sample_joint(joint_dist)
#
#     if input_case == 20:
#
#         joint_samples = joint_dist
#
#     return in_samples, out_samples, joint_samples