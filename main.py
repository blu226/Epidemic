#MAIN
from network import *
import os
import pickle
from generateMessage_new import *


#Function create_constants: creates a constants file for the given simulation
def create_constants(startTime):
    Link_Exists_path = "Link_Exists_path = \'Bands_UMass/2007-10-23_2007-10-24/'" + "\n"
    DataMule_path = " DataMule_path = \'DataMules1/2007-10-23_2007-10-24/Day1/\' " + "\n"
    time = "startTime = " + str(startTime) + "\n"

    f = open("constants.py", "w")

    f.write(time)
    f.write(Link_Exists_path)
    f.write(DataMule_path)

    f.write("M = [1,10,25,50,100,500,750,1000]\n")
    f.write("maxTau = 10\n")
    f.write("num_messages = 25\n")
    f.write("num_sources = 6\n")
    f.write("num_des = 3\n")
    f.write("T = 120\n")

    f.close()

#Loop thru each day
# days = os.listdir("Bands/")
# days.sort()

# counter = 0
# for day in days:
#     if counter > 0:
#         break

time = 0
    # print(day)
output_file = open(Link_Exists_path + delivery_file_name, "w")
output_file.write("ID\ts\td\tts\tte\tLLC\tsize\tparent\tparentTime\treplica\n")
output_file.write("----------------------------------------------------\n")
output_file.close()

output_file2 = open(Link_Exists_path + notDelivered_file_name, "w")
output_file2.write("ID\ts\td\tts\tte\tLLC\tsize\tparent\tparentTime\treplica\n")
output_file2.write("----------------------------------------------------\n")
output_file2.close()
#Load Link Exists
LINK_EXISTS = pickle.load(open(Link_Exists_path + "LINK_EXISTS.pkl", "rb"))
specBW = pickle.load(open(Link_Exists_path + "specBW.pkl", "rb"))
#Create constants
# create_constants(time)
#Generate Messages
create_messages()
#Create network
net = network()
#Fill network with datamules, sources, and destinations
net.fill_network()
#Create messages
# path = "Bands/" + day + "/"
# create_messages(path)
#Run simulation
for i in range(T):
    print("TIME: " + str(i))
    net.network_GO(i , LINK_EXISTS, specBW)

net.all_messages()
