import threading
import time


class Monitor(threading.Thread):

    def __init__(self, tasks, refresh_rate=1):
        super(Monitor, self).__init__()
        self.tasks = tasks
        self.refresh_rate = refresh_rate  # in seconds

    def __check_termination(self):
        for t in self.tasks:
            if not t.terminated:
                return False
        return True

    def run(self):
        while self.__check_termination():
            # at each iteration print a sort of monitor
            time.sleep(self.refresh_rate)