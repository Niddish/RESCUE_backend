# RESCUE Backend

## Generating JSON topology

To run:

1. Clone the repository.
2. Modify 20B.yml to chosen specifications (currently designed to read the pipeline and model parallel values directly from this config specifically)
3. Modify main.py to chosen specifications (change total number of gpus with your desired value [ex. - pp=4, mp=2, dp=12 = 96 gpus])
4. Run `mpirun -np <num_nodes> python main.py ` - replace <num_nodes> with however many nodes you have allocated.
5. You should now see (via another terminal) a new file - gpu_topology.json - this is updated every 5 seconds with GPU information.
   
And that's it!

## Running webserver

To run:

1. Run "sbatch flask_job.sh" - this is the shell script.
2. Wait ~15-30 seconds (allocates node to run webserver so time varies).
3. After waiting, do an "ls" - there should be two new files - flask.out and flask.log - flask.out contains the API link to be inputted in frontend code, and flask.log is the debug log)

And that's it!

---

### **NOTE**
- This version only works with the 20B.yml config - or at least, that's what I've tested. Support for other configs in the future.

---

