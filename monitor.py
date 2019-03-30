import threading
import time

from os import name, system
from termcolor import cprint, colored

from utility import get_topic


class Monitor(threading.Thread):

    """ Monitor class """

    BASE_NAME = "AGENT-NAME"
    BASE_STATE = "STATE"
    BASE_DESCRIPTION = "DESCRIPTION"
    BASE_TOPIC = "TOPIC"
    BASE_TASK = "TASKS"

    def __init__(self, tasks, agents, refresh_rate=1):
        super(Monitor, self).__init__()
        self.tasks = tasks
        self.agents = agents
        self.refresh_rate = refresh_rate  # in seconds
        self.name_width = 30
        self.state_width = 30
        self.description_width = 30
        self.topic_width = 30

        self.border = 130 * "*"
        self.header = "**{0: ^30s}**{1: ^30s}**{2: ^30s}**{3: ^30s}**".format(Monitor.BASE_NAME,
                                                                              Monitor.BASE_STATE,
                                                                              Monitor.BASE_DESCRIPTION,
                                                                              Monitor.BASE_TOPIC)
        self.task_header = "**{0: ^30s}**{1: ^62}**{2: ^30s}**".format(Monitor.BASE_TASK,
                                                                       Monitor.BASE_DESCRIPTION,
                                                                       Monitor.BASE_TOPIC)

    def __check_termination(self):
        for t in self.tasks:
            if not t.terminated:
                return False
        return True

    # define our clear function
    def __clear(self):

        # for windows
        if name == 'nt':
            _ = system('cls')

            # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')

    def __print_monitor(self):
        # TODO: clear the terminal before printing the monitor
        self.__clear()
        # Agents' monitor
        print(self.border)
        print(self.header)
        print(self.border)
        for a in self.agents:
            state = colored("executing", color="yellow") if a.executing else colored("occupied", color="blue") \
                if a.occupied else colored("failed", color="red") if a.failed else colored("free", color="green")
            description = "empty" if not a.executing else a.current_task.logger.name
            line = "**{0: ^30s}**{1: ^39s}**{2: ^30s}**{3: ^30}**".format(a.logger.name,
                                                                          state,
                                                                          description,
                                                                          a.topic.value)
            cprint(line)
        print(self.border)

        # Tasks' monitor
        print(self.border)
        print(self.task_header)
        print(self.border)
        for t in self.tasks:
            state = colored("terminated!", "red") if t.terminated \
                else colored("in execution.. {}% complete".format(t.percentage), "green") \
                    if t.progress != 0 else colored("to be allocated", "grey")
            line = "**{0: ^30s}**{1: ^71s}**{2: ^30s}**".format(t.logger.name, state, get_topic(t.subjects).value)
            cprint(line)
        print(self.border)

    def run(self):
        while not self.__check_termination():
            self.__print_monitor()
            print("\n\n\n\n\n\n")
            time.sleep(self.refresh_rate)
        self.__print_monitor()