
import pydot

graph = pydot.Dot(graph_type="digraph")
# graph = pydot.Dot(graph_type="digraph", concentrate=True)
graph.set_node_defaults(color='black', style='filled', fillcolor='#4472C4')
ind = 0
r_nodes = []
with open('models/example/networks/example_0.csv', 'r') as network:
    lines = network.readlines()
    for i, line in enumerate(lines):
        if i > 0:
            print(line[:-1])
            if line:
                ls = line.split(',')
                ls1 = ls[1][1:-1].split(':')
                ls2 = ls[2][1:-1].split(':')
                print(ls1)
                if ls[0] == '0':
                    graph.add_edge(pydot.Edge(ls1[0], ls2[0]))
                if ls[0] == '1':
                    graph.add_node(pydot.Node('R'+str(ind), style="filled", fillcolor="black",
                                              shape='point', width='0.1', height='0.1'))
                    graph.add_edge(pydot.Edge(ls1[0], 'R'+str(ind), arrowhead='none'))
                    graph.add_edge(pydot.Edge(ls1[1], 'R'+str(ind), arrowhead='none'))
                    graph.add_edge(pydot.Edge('R'+str(ind), ls2[0]))
                if ls[0] == '2':
                    graph.add_node(pydot.Node('R' + str(ind), style="filled", fillcolor="black",
                                              shape='point', width='0.1', height='0.1'))
                    graph.add_edge(pydot.Edge(ls1[0], 'R'+str(ind), arrowhead='none'))
                    graph.add_edge(pydot.Edge('R'+str(ind), ls2[0]))
                    graph.add_edge(pydot.Edge('R'+str(ind), ls2[1]))

                if ls[0] == '3':
                    graph.add_node(pydot.Node('R'+str(ind), style="filled", fillcolor="black",
                                              shape='point', width='0.1', height='0.1'))
                    graph.add_edge(pydot.Edge(ls1[0], 'R'+str(ind), arrowhead='none'))
                    graph.add_edge(pydot.Edge(ls1[1], 'R'+str(ind), arrowhead='none'))
                    graph.add_edge(pydot.Edge('R'+str(ind), ls2[0]))
                    graph.add_edge(pydot.Edge('R'+str(ind), ls2[1]))
                r_nodes.append('R'+str(ind))
                ind += 1


graph.write_png('test_00.png', prog='neato')
quit()
# for each in edges:
#     graph.add_edge(pydot.Edge(each[0], each[1]))
#
# graph.write_png(os.path.join(output_dir, group_name, 'net_figs', group_name + '_' + str(i) + '.png'))
# graph.write(os.path.join(output_dir, group_name, 'dot_files', group_name + '_' + str(i) + '.dot'),
#             format='dot')