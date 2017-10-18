#!/usr/bin/python                                                                            
                                                                                             
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.link import TCLink

class ComplexTopo(Topo):
    "Multi-switch, poly-host"
    def build(self, n=3):
        # generate switches
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')
        
        # generate hosts
        host1 = self.addHost('h%s' % 1)
        host2 = self.addHost('h%s' % 2)
        host3 = self.addHost('h%s' % 3)

        # link hosts to their respective switches, as well as the two switches
        self.addLink(host1, switch1, bw=10, delay='200ms', loss=0, max_queue_size=1000, use_htb=True)
        self.addLink(host2, switch2, bw=10, delay='200ms', loss=0, max_queue_size=1000, use_htb=True)
        self.addLink(host3, switch2, bw=10, delay='200ms', loss=0, max_queue_size=1000, use_htb=True)
        self.addLink(switch1, switch2, bw=10, delay='200ms', loss=0, max_queue_size=1000, use_htb=True)

topos = {'ComplexTopo': (lambda: ComplexTopo())}

def test():
    "Generate network and test it"
    topo = ComplexTopo(n=3)
    net = Mininet(topo, link=TCLink)
    net.start()
    
    dumpNodeConnections(net.hosts)
    
    net.pingAll()
    net.stop()

if __name__ == '__main__':
    # tell mininet to pirnt useful info
    setLogLevel('info')
    test()
