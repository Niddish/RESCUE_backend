#!/bin/bash

#SBATCH -J tap_flask
#SBATCH -o flask.out
#SBATCH -p development
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 02:00:00

echo "TACC: job ${SLURM_JOB_ID} execution at: $(date)"

TAP_FUNCTIONS="/share/doc/slurm/tap_functions"
if [ -f ${TAP_FUNCTIONS} ]; then
    . ${TAP_FUNCTIONS}
else
    echo "TACC: ERROR - could not find TAP functions file: ${TAP_FUNCTIONS}"
    exit 1
fi

NODE_HOSTNAME=$(hostname -s)
echo "TACC: running on node ${NODE_HOSTNAME}"

echo "TACC: unloading xalt"
module unload xalt
module load python3/3.7.0

LOCAL_PORT=8080
echo "TACC: Starting Flask server on ${NODE_HOSTNAME}:${LOCAL_PORT}"
nohup python3 webserver.py &> ${HOME}/flask.log &

sleep 5  # Give Flask time to start

LOGIN_PORT=$(tap_get_port)
echo "TACC: got login node Flask port ${LOGIN_PORT}"

NUM_LOGINS=4
for i in $(seq ${NUM_LOGINS}); do
    ssh -q -f -g -N -R ${LOGIN_PORT}:${NODE_HOSTNAME}:${LOCAL_PORT} login${i}
done

if [ $(ps -fu ${USER} | grep ssh | grep login | grep -vc grep) != ${NUM_LOGINS} ]; then
    echo "TACC: ERROR - ssh tunnels failed to launch"
    exit 1
fi
echo "TACC: created reverse ports on Frontera logins"

FLASK_URL="https://frontera.tacc.utexas.edu:${LOGIN_PORT}"
echo "TACC: Your Flask server is now running at ${FLASK_URL}"

# Keep the job alive while Flask is running
while ps aux | grep webserver.py | grep -qv grep; do
    sleep 10
done
