#NETWORK CLASS
from constants import *
from node import *
from message import *
from computeHarvesine import *
import os


#Function init: initialize node list and start time
class network(object):
    def __init__(self):
        self.nodes = []
        self.time = 0

#Function add_node: adds node to network
    def add_node(self, node):
        self.nodes.append(node)

#Function get_ID: gets ID for datamule, source, or destination from filename
    def get_ID(self, filename):
        if filename[1] == ".":
            return filename[0]
        else:
            return filename[:2]

# Function fill_network: create node objects for each datamule, source, and destination
    def fill_network(self):
        files = os.listdir(DataMule_path)
        files.sort()

        for i in range(len(files)):
            node_ID = self.get_ID(files[i])
            node_curr = node(node_ID)
            self.add_node(node_curr)

#Function send_message: sends message to all nodes in range
    def send_message(self,src_node, message, tau, LINK_EXISTS, specBW):

        to_send = True
        replica = 0

        for des_node in self.nodes:
            if des_node != src_node and message not in des_node.buf:
                for mes in des_node.buf:
                    if mes.ID == message.ID:
                        to_send = False

                if to_send == True:
                    if src_node.send_message(des_node, message, tau, replica, LINK_EXISTS, specBW):
                       # print("SENDING: " + str(message.ID) + " at time " + str(tau) + " from " + str(src_node.ID))
                        replica += 1



#Function update_nodes: updates each nodes position for a given time
    def update_nodes(self):
        for i in range(len(self.nodes)):
            self.nodes[i].update_position(self.time)

#Function is_in_communication_range: checks if 2 nodes are within range of a certain spectrum
    def is_in_communication_range(self, node1, node2):
        dist = funHaversine(node1.coord[1], node1.coord[0], node2.coord[1], node2.coord[0])
        if dist < 1800:
            return True
        else:
            return False

#Function add_messages: adds messages to their source node at each tau
    def add_messages(self, time):
        with open("generated_messages.txt", "r") as f:
            lines = f.readlines()

        for line in lines:
            line_arr = line.strip().split()
            if int(line_arr[3]) == time:
                new_mes = message(line_arr[0], line_arr[1], line_arr[2], line_arr[3], line_arr[4])
                src = int(line_arr[1])
                self.nodes[src].buf.append(new_mes)


#Function messages_delivered: deletes messages that have been delivered
    def messages_delivered(self):
        for node in self.nodes:
            for mes in node.buf:
                if int(mes.des) == int(node.ID):
                    f = open(Link_Exists_path + "delivered_messages.txt", "a")
                    line = str(mes.ID) + "\t" + str(mes.src) + "\t" + str(mes.des) + "\t" + str(mes.genT) + "\t" + str(self.time)+ "\t" + str(mes.last_sent - mes.genT) + "\t" + str(mes.size) + "\t\t" + str(mes.parent) + "\t\t" + str(mes.parentTime) + "\t\t\t" + str(mes.replica) + "\n"
                  #  print(line)
                    f.write(line)
                    f.close()
                    node.buf.remove(mes)

    def all_messages(self):
        f = open(Link_Exists_path + "all_messages.txt", "a")
        for node in self.nodes:
            print("Node " + str(node.ID) + ": ")
            for mes in node.buf:
                line = str(mes.ID) + "\t" + str(mes.src) + "\t" + str(mes.des) + "\t" + str(mes.genT) + "\t" + str(self.time) + "\t" + str(mes.last_sent - mes.genT) + "\t" + str(mes.size) + "\t" + str(mes.parent) + "\t" + str(mes.parentTime) + "\t" + str(mes.replica) + "\n"
                print(line)
                f.write(line)
        f.close()

#Function network_GO: completes all tasks of a network in 1 tau
    def network_GO(self, tau, LINK_EXISTS, specBW):
        self.time = tau
    #Send all messages
        #For each node
        for i in range(len(self.nodes)):
            #For each message in this nodes buffer
            node = self.nodes[i]
            for mes in node.buf:
                if mes.last_sent < tau:
                    self.send_message(node, mes, tau, LINK_EXISTS, specBW)
    #Handle messages that got delivered
        self.messages_delivered()
     #Check if new messages were generated
        self.add_messages(tau)