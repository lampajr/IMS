import threading
import time

from os import name, system
from termcolor import cprint, colored

from utility import get_topic_from_subjects, get_time, Topic


def clear():

    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


class Monitor(threading.Thread):

    """ Monitor class """

    BASE_NAME = "AGENT-NAME"
    BASE_STATE = "STATE"
    BASE_DESCRIPTION = "DESCRIPTION"
    BASE_TOPIC = "TOPIC"
    BASE_TASK = "TASKS"
    BASE_PROGRESS = "PROGRESS"

    def __init__(self, tasks, agents, clear=True, refresh_rate=1):
        super(Monitor, self).__init__()
        self.tasks = tasks
        self.agents = agents
        self.refresh_rate = refresh_rate  # in seconds
        self.clear= clear

        self.name_width = 30
        self.state_width = 30
        self.description_width = 30
        self.topic_width = 30

        self.border = 170 * "*"
        self.header = "**{0: ^30s}**{1: ^30s}**{2: ^70s}**{3: ^30s}**".format(Monitor.BASE_NAME,
                                                                              Monitor.BASE_STATE,
                                                                              Monitor.BASE_DESCRIPTION,
                                                                              Monitor.BASE_TOPIC)
        self.task_header = "**{0: ^30s}**{1: ^30s}**{2: ^70s}**{3: ^30s}**".format(Monitor.BASE_TASK,
                                                                                   Monitor.BASE_STATE,
                                                                                   Monitor.BASE_PROGRESS,
                                                                                   Monitor.BASE_TOPIC)

    def __check_termination(self):
        for t in self.tasks:
            if not t.terminated:
                return False
        return True

    # define our clear function

    def __print_monitor(self):

        """ print the state of all the agents involved in the system
            and of all the tasks executed and that have to be executed """

        if self.clear:
            clear()
        # Agents' monitor
        print(self.border)
        print(self.header)
        print(self.border)
        topic = Topic.COOK
        for a in self.agents:
            if a.topic != topic:
                topic = a.topic
                print("**" + "-"*166 + "**")
            state = colored("executing", color="yellow") if a.executing else colored("occupied", color="blue") \
                if a.occupied else colored("failed", color="red") if a.failed else colored("free", color="green")
            description = a.current_task.logger.description if a.executing else "offering " + colored(a.bid, "red") + " in {} auction".format(a.current_task.logger.name) if a.occupied else "empty"
            if not a.executing and a.occupied:
                line = "**{0: ^30s}**{1: ^39s}**{2: ^79s}**{3: ^30}**".format(a.logger.name,
                                                                              state,
                                                                              description,
                                                                              a.topic.value)
            else:
                line = "**{0: ^30s}**{1: ^39s}**{2: ^70s}**{3: ^30}**".format(a.logger.name,
                                                                              state,
                                                                              description,
                                                                              a.topic.value)
            cprint(line)
        print(self.border)

        # Tasks' monitor
        print(self.border)
        print(self.task_header)
        print(self.border)
        count = 0
        for t in self.tasks:
            if count == 4:
                print("**" + "-"*166 + "**")
                count = 0
            state = colored("terminated!", "red") if t.terminated \
                else colored("allocated", "green") if t.allocated else colored("to be allocated..", "blue") \
                if t.generated else colored("not yet generated", "grey")
            progress = "{}% complete..".format(t.percentage) if t.progress != 0 else "not yet started!"
            line = "**{0: ^30s}**{1: ^39s}**{2: ^70s}**{3: ^30s}**".format(t.logger.name, state, progress, get_topic_from_subjects(t.subjects).value)
            cprint(line)
            count += 1
        print(self.border)

    def run(self):
        started_time = get_time()
        while not self.__check_termination():
            self.__print_monitor()
            #print("\n\n\n\n\n\n\n\n")
            print("")
            time.sleep(self.refresh_rate)
        for a in self.agents:
            a.occupied = False
            a.executing = False
        self.__print_monitor()
        elapsed_time = get_time() - started_time
        elapsed_minutes = int(((elapsed_time / 1000) / 60))
        elapsed_seconds = (((elapsed_time / 1000) / 60) - elapsed_minutes) * 60
        print("\n\nComputation ended in {} minutes and {} seconds".format(elapsed_minutes, int(elapsed_seconds)))
