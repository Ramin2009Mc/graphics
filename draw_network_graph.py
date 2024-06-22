from graphviz import Graph

def draw_topology(topology_dict, output_filename="topology"):
    dot = Graph(comment='Network Topology')
    for (local_device, local_interface), (remote_device, remote_interface) in topology_dict.items():
        dot.node(local_device)
        dot.node(remote_device)
        dot.edge(f"{local_device}:{local_interface}", f"{remote_device}:{remote_interface}")
    dot.render(output_filename, format='png', cleanup=True)
