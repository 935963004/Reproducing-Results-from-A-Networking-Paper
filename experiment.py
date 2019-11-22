import os
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from time import sleep
from subprocess import Popen

class InitialCwndTopo(Topo):
	def __init__(self):
		Topo.__init__(self)
		h1 = self.addHost("h1" )
		h2 = self.addHost("h2")
		s1 = self.addSwitch("s1")
		self.addLink(h1, s1, bw=500, delay=str(rtt / 2) + "ms")
		self.addLink(h2, s1, bw=bw / 1000)

def set_cwnd(net):
	h1 = net.get("h1")
	ip_route = h1.cmd("ip route show")
	h1.cmd("ip route change %s initcwnd %d initrwnd %d mtu 1500" % (ip_route.strip(), init_cwnd, 100))

	h2 = net.get("h2")
	ip_route = h2.cmd("ip route show")
	h2.cmd("ip route change %s initcwnd %d initrwnd %d mtu 1500" % (ip_route.strip(), init_cwnd, 100))

def start_web_server(net):
	h1 = net.get("h1")
	h1.popen("python web_server.py", shell=True)
	sleep(1)

def get_web_transfer_time(net):
	h1 = net.get("h1")
	h2 = net.get("h2")
	with open("results/cwnd%d_rtt%d_bw%d.txt" % (init_cwnd, rtt, bw), 'w') as f:
		print("Running test for init_window = %d and rtt = %d and bw = %d" % (init_cwnd, rtt, bw))
		f.write(h2.cmd('curl -o /dev/null -s -w %%{time_total} %s' % (h1.IP())))
		f.write('\n')

if __name__ == "__main__":
	if not os.path.exists("results"):
		os.makedirs("results")
	
	for rtt in (20, 50, 100, 200, 500, 1000, 3000, 5000):
		for bw in (56, 256, 512, 1000, 2000, 3000, 5000, 7000):
			for init_cwnd in (3, 10):
				topo = InitialCwndTopo()
				os.system("sudo mn -c > /dev/null 2>&1")
				os.system("sysctl -w net.ipv4.tcp_congestion_control=cubic > /dev/null")
				net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
				net.start()
				set_cwnd(net)
				start_web_server(net)
				get_web_transfer_time(net)
				net.stop()
				Popen("pgrep -f webserver.py | xargs kill -9", shell = True).wait()

