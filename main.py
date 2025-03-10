import json
import time
from mpi_gpu import collect_and_merge_gpu_data
from config_topology import generate_topology_from_gpu_data
import os

def write_json_atomic(filename, data):
    """
    Writes JSON data atomically to prevent corruption and ensure consistency.
    If interrupted, the original file remains unchanged.
    """
    tmp_filename = filename + ".tmp"
    with open(tmp_filename, "w") as f:
        json.dump(data, f, indent=4)

    os.replace(tmp_filename, filename)  

def main():
    json_filename = "gpu_topology.json"
    
    # Define total GPUs dynamically 
    total_gpus = 96  #CHANGE VALUE HERE

    while True:
        try:
            #collect real-time GPU data from MPI
            gpu_data = collect_and_merge_gpu_data()

            #generate topology
            topology_data = generate_topology_from_gpu_data(gpu_data, total_gpus)

            #write to json
            write_json_atomic(json_filename, topology_data)

            print("Updated gpu_topology.json")

            #wait before next write to reduce overhead
            time.sleep(5)

        except KeyboardInterrupt:
            print("\nInterrupted. Keeping the last known good GPU topology.")
            break  #currently exits with keyboard interrupt, this ensures data is not lost on exit

if __name__ == "__main__":
    main()
