import sys
import re
import os
from collections import defaultdict
from draw_network_graph import draw_topology

def parse_cdp_neighbors(file_content):
    regex = r"(?P<device_id>\S+)\s+(?P<local_interface>\S+ \S+)\s+\d+\s+\S+\s+\S+\s+(?P<port_id>\S+ \S+)"
    connections = defaultdict(dict)
    for match in re.finditer(regex, file_content):
        device_id = match.group("device_id")
        local_interface = match.group("local_interface")
        port_id = match.group("port_id")
        connections[local_interface] = (device_id, port_id)
    return connections

def read_files(file_list):
    combined_data = defaultdict(dict)
    for file_name in file_list:
        with open(file_name) as f:
            device_name = os.path.basename(file_name).split('.')[0]
            file_content = f.read()
            device_connections = parse_cdp_neighbors(file_content)
            for local_interface, (remote_device, remote_port) in device_connections.items():
                combined_data[(device_name, local_interface)] = (remote_device, remote_port)
    return combined_data

def remove_duplicate_links(topology):
    filtered_topology = {}
    for key, value in topology.items():
        if not filtered_topology.get(value) == key:
            filtered_topology[key] = value
    return filtered_topology

def main(file_list):
    raw_topology = read_files(file_list)
    filtered_topology = remove_duplicate_links(raw_topology)
    draw_topology(filtered_topology)

if __name__ == "__main__":
    file_list = sys.argv[1:]
    main(file_list)
