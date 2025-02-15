from constants import *


def message_info(mes_list):
    with open(Link_Exists_path + generated_file_name, 'r') as f:
        lines = f.readlines()

    file = open("NOT_delivered.txt", 'w')

    for id in mes_list:
        for line in lines:
            line_arr = line.strip().split()
            if int(id) == int(line_arr[0]):
                file.write(line)
    file.close()


def compute_metrics(lines, total_messages, delivery_time):
    delivered = 0
    latency = 0
    energy = 0
    mes_IDs = []
    all_IDs = [x for x in range(num_messages)]

    for line in lines:
        line_arr = line.strip().split("\t")
        if int(line_arr[4]) <= delivery_time and int(line_arr[0]) not in mes_IDs:
            delivered += 1
            latency += int(line_arr[5])
            # energy += float(line_arr[7])
            mes_IDs.append(int(line_arr[0]))
            all_IDs.remove(int(line_arr[0]))

    if delivered > 0:
        latency = float(latency)/delivered
        energy = float(energy)/delivered

    if total_messages > 0:
        delivered = float(delivered) / total_messages

    print("t: ", t, " msg: ", total_messages, " del: ", delivered, "lat: ", latency)

    return delivered, latency, energy, all_IDs, mes_IDs


#Main starts here
msg_file = open("../Bands" + str(max_nodes) + "/" + Link_Exists_path.split("/")[2] + "/" + "generated_messages.txt", "r")
total_messages = len(msg_file.readlines()[1:])

metric_file = open(Link_Exists_path + metrics_file_name, "w")
f = open(Link_Exists_path + delivery_file_name, "r")

lines = f.readlines()[2:]


delivery_times = [i for i in range(0, T + 10, 10)]


metric_file.write("#t\tPDR\tLatency\tEnergy\n")
for t in delivery_times:
    avg_pdr, avg_latency, avg_energy, all_IDs, mes_IDs = compute_metrics(lines, total_messages, t)
    metric_file.write(str(t) + "\t" + str(avg_pdr) + "\t" + str(avg_latency) + "\t" + str(avg_energy) + "\n")

metric_file.close()
print("Delivered messages", sorted(mes_IDs))
# message_info(all_IDs)

