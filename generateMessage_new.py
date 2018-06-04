from constants import *
import random

def create_messages():

    message_file = open(Link_Exists_path + generated_file_name, "w")
    with open(Link_Exists_path + "LLC_PATH.txt", "r") as fp:
        path_lines = fp.readlines()[1:]
    fp.close()

    id = 0

    while id < num_messages:
        rand_line = random.randint(0, len(path_lines) - 1)
        line_arr = path_lines[rand_line].strip().split()

        src = int(line_arr[0])
        des = int(line_arr[1])
        genT = int(line_arr[2])
        size = int(line_arr[3])

        path = line_arr[4:]

        generateMessage = True

        if len(set(path)) > 2:
            for nodeId in path:
                if int(nodeId) > num_sources + num_des:
                    generateMessage = True

        t = random.randint(int(45), int(60))

        #rand = random.uniform(0, 1)

        if generateMessage == True  and src < num_sources and  des >= num_sources and des <= num_sources + num_des and genT <= 60:

            p = random.uniform(0, 1)

            if p < .1:
                message_file.write(
                    str(id) + "\t" + str(src) + "\t" + str(des) + "\t" +  str(t + startTime) + "\t" + str(size) + "\n")
            else:
                message_file.write(
                    str(id) + "\t" + str(src) + "\t" + str(des) + "\t"  + "\t" + str(genT + startTime) + "\t" + str(size) + "\n")

            id += 1

    message_file.close()





