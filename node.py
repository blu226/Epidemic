#NODE CLASS
from constants import *
from computeHarvesine import *
from message import *
import random
import math



def can_transfer(size, s, seconds):
    bw = random.randint(minBW[s], maxBW[s])
    time_to_transfer = math.ceil(size/bw)

    if time_to_transfer < seconds:
        return True
    else:
        return False


#Function init: initialize variables
class node(object):
    def __init__(self, id):
        self.ID = int(id)
        self.buf = []

#Function send_message: sends message to a node if it doesn't have the message already
    def send_message(self, des_node, mes, ts, replicaID, LINK_EXISTS):

        if mes.last_sent < ts:
            max_end = ts + maxTau

            if max_end > T:
                max_end = T

            for te in range(ts + 1, max_end):
                spec_to_use = []

                for s in range(4):
                    if LINK_EXISTS[self.ID, des_node.ID, s, int(ts - startTime), int(te - startTime)] == 1:
                        spec_to_use.append(s)

                for spec in range(len(spec_to_use)):
                    if can_transfer(mes.size, spec_to_use[spec], (te - ts) * 60):
                        new_message = message(mes.ID, mes.src, mes.des, mes.genT, mes.size )
                        new_message.set(te, replicaID, te, self.ID)
                        des_node.buf.append(new_message)

                        return True
            return False

