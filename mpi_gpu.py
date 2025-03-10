import os
import pynvml
import socket
import json
import time
from mpi4py import MPI

def get_available_gpus():
    """
    Detect available GPUs using NVML and return GPU information.
    """
    pynvml.nvmlInit()

    # Get node hostname (short name)
    full_node_name = socket.gethostname()
    short_node_name = full_node_name.split('.')[0]

    # Check CUDA_VISIBLE_DEVICES first
    cuda_visible_devices = os.getenv("CUDA_VISIBLE_DEVICES")
    if cuda_visible_devices:
        gpu_indices = [int(x) for x in cuda_visible_devices.split(",") if x.strip().isdigit()]
    else:
        gpu_indices = list(range(pynvml.nvmlDeviceGetCount()))

    gpu_info = []
    for i in gpu_indices:
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)

        raw_name = pynvml.nvmlDeviceGetName(handle)
        name = raw_name.decode("utf-8") if isinstance(raw_name, bytes) else raw_name

        memory = pynvml.nvmlDeviceGetMemoryInfo(handle)
        utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
        temperature = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)

        gpu_info.append({
            "id": i,
            "name": name,
            "memory_used_MB": memory.used // (1024 * 1024),
            "memory_total_MB": memory.total // (1024 * 1024),
            "utilization_pct": utilization.gpu,
            "temperature_C": temperature,
            "node_name": short_node_name
        })

    pynvml.nvmlShutdown()
    return {f"Node: {short_node_name}": gpu_info}

def collect_and_merge_gpu_data():
    """
    Uses MPI to collect GPU data from all nodes and merge it in real-time.
    Returns a list of dictionaries containing GPU and node details.
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()  # Unique ID for each node

    while True:
        # Each node gets its own GPU data
        local_gpu_data = get_available_gpus()

        # Master node (rank 0) collects all data
        all_gpu_data = comm.gather(local_gpu_data, root=0)

        if rank == 0:
            # Master node merges all collected data into a list
            merged_data = []
            for node_data in all_gpu_data:
                for node_name, gpus in node_data.items():
                    for gpu in gpus:
                        merged_data.append(gpu)

            return merged_data  # Now returns a list instead of writing JSON

        # Wait 5 seconds before next update
        time.sleep(5)
