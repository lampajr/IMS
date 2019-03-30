import threading
import time
from pprint import pprint


class Monitor(threading.Thread):

    def __init__(self, tasks, agents, refresh_rate=1):
        super(Monitor, self).__init__()
        self.tasks = tasks
        self.agents = agents
        self.refresh_rate = refresh_rate  # in seconds

    def __check_termination(self):
        for t in self.tasks:
            if not t.terminated:
                return False
        return True

    def run(self):
        while not self.__check_termination():
            # at each iteration print a sort of monitor
            pprint("***********************")
            for a in self.agents:
                pprint(a.logger.name)
            pprint("***********************")
            time.sleep(self.refresh_rate)