To reproduce the result:
1. Create a Google Cloud VM instance (under compute engine) with the following specification: 4 vCPUs, 15GB memory, zone = us-west1-b, Linux 16.04 LTS, allow HTTP/HTTPS traffic.
2. Clone our code on Github: git clone https://github.com/935963004/Reproducing-Results-from-A-Networking-Paper
3. cd into Reproducing-Results-from-A-Networking-Paper, then run "chmod +x *.sh" to make shell scripts executable.
4. Run "sudo ./install.sh" to install Mininet, Python 2.7, numpy, matplotlib, argparse.
5. Run "sudo ./run.sh" to run the simulation. It should take about 15 - 20 minutes. Once done, the two figures for RTT and BW will be in the figures folder.
