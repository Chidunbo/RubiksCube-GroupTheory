from pyvis.network import Network

net = Network()
net.add_node(1, label = "e")
net.add_node(2, label = "F")
net.add_edge(1,2,weight=0.87)
net.toggle_physics(True)
net.show("rubics_test1.html",notebook=False)
