# RESCUE Backend

## Generating JSON topology

To run:

1. Clone the repository.
2. Modify 20B.yml to chosen specifications (currently designed to read the pipeline and model parallel values directly from this config specifically)
3. Modify main.py to chosen specifications (change total number of gpus with your desired value [ex. - pp=4, mp=2, dp=12 = 96 gpus])
4. Run `mpirun -np <num_nodes> python main.py ` - replace <num_nodes> with however many nodes you have allocated.
   
And that's it!

---

### **NOTE**
- This version only works with the 20B.yml config - or at least, that's what I've tested. Support for other configs in the future.
- There is an shell script that is meant to use Flask to take the contents of the JSON and use it as an API, which can be referenced in the frontend. It was working at some point, but more recently has not been. Needs to be fixed. This, and the webserver code is found in the flask folder.

---

