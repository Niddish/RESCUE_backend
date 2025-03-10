import yaml
import json

def load_config(filepath="20B.yml"):
    """
    Load the YAML configuration file.
    """
    with open(filepath, 'r') as f:
        config = yaml.safe_load(f)
    return config

def extract_parallel_settings(config, total_gpus):
    """
    Extract parallelism settings from the configuration and compute data parallel size.
    """
    pipe_parallel_size = config.get("pipe_parallel_size", 1)
    model_parallel_size = config.get("model_parallel_size", 1)
    data_parallel_size = total_gpus // (pipe_parallel_size * model_parallel_size)

    return {
        "pipe_parallel_size": pipe_parallel_size,
        "model_parallel_size": model_parallel_size,
        "data_parallel_size": data_parallel_size,
    }

def construct_3d_topology(parallel_settings, gpu_info, total_gpus, gpus_per_node=4):
    """
    Constructs a 3D topology representation based on parallel settings and real GPU data.
    """
    topology = {}
    node_gpu_map = {}

    # Group detected GPUs by node
    detected_nodes = set()
    for gpu in gpu_info:
        node_name = gpu["node_name"]
        if node_name not in node_gpu_map:
            node_gpu_map[node_name] = []
        node_gpu_map[node_name].append(gpu)
        detected_nodes.add(node_name)

    # Assign detected GPUs first
    for node_name, gpus in node_gpu_map.items():
        topology[node_name] = [{"id": f"GPU {gpu['id']+1}", "info": gpu} for gpu in gpus]

    # Determine number of placeholder nodes
    detected_node_count = len(detected_nodes)
    total_nodes = total_gpus // gpus_per_node

    # Assign placeholder nodes
    for i in range(detected_node_count + 1, total_nodes + 1):
        node_placeholder = f"Node {i} (not detected)"
        topology[node_placeholder] = [{"id": f"GPU {j+1} (no data)"} for j in range(gpus_per_node)]

    return topology

def generate_topology_from_gpu_data(gpu_info, total_gpus):
    """
    Generate the 3D topology from real-time GPU data.
    """
    config = load_config("20B.yml")
    parallel_settings = extract_parallel_settings(config, total_gpus)
    topology = construct_3d_topology(parallel_settings, gpu_info, total_gpus)
    return {
        "parallel_settings": parallel_settings,
        "topology": topology,
        "configuration": config
    }
