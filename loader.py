from task import Task, CookTask, HandlePaymentTask, ServeTask
from utility import *
from agent import Agent


class Loader:

    """ class that given a file loads all the data, creating the
        multiagent system, its task and the starting the system
        itself """

    def __init__(self, filename):
        self.n_agents = 0
        self.n_tasks = 0
        self.auctioneer_contract_time = 0
        self.auction_timeout = 4

        # lists
        self.agents = []
        self.starter_tasks = []  # will contain only the started task (cook topic)
        self.tasks = []  # will contain all the tasks involved

        self.time_between_task = 5  # seconds between two consecutive task generation
        self.refresh_rate = 1  # refresh rate of the monitor

        self.__load_data(filename=filename)

    def __load_data(self, filename):
        with open(filename, "r") as file:
            # the first integer tells how many agents are involved in the system
            self.n_agents = int(file.readline())

            for idx in range(self.n_agents):
                # the line representing the agent has to be in comma separated values
                # all the elements must be reported
                elements = file.readline().rstrip().split(",")
                self.agents.append(Agent(name=elements[0],
                                         topic=get_topic_from_string(elements[1]),
                                         contract_time=int(elements[2]),
                                         skill=create_skill(elements[3]),
                                         write_on_terminal=get_boolean(elements[4]),
                                         verbose=get_boolean(elements[5])))

            # now the integers tells how many starter task have to be generated
            self.n_tasks = int(file.readline())

            for idx in range(self.n_tasks):
                # each line represent a list of task where the task in position i+1 is
                # a subtask of the one in position i, each task is '-' separated
                tasks_list = file.readline().rstrip().split('-')
                current_tasks = []
                for task_info in tasks_list:
                    # each task stores info in comma separated values
                    elements = task_info.split(',')
                    name = elements[0]
                    length = int(elements[1])
                    topic = get_topic_from_string(elements[2])
                    min_progress = int(elements[3])
                    difficulty = int(elements[4])
                    color = elements[5]
                    write_on_terminal = get_boolean(elements[6])
                    verbose = get_boolean(elements[7])
                    description = elements[8]
                    if topic == Topic.COOK:
                        current_tasks.append(CookTask(name=name,
                                                      length=length,
                                                      min_progress=min_progress,
                                                      difficulty=difficulty,
                                                      color=color,
                                                      write_on_terminal=write_on_terminal,
                                                      verbose=verbose,
                                                      description=description))
                    elif topic == Topic.HANDLE_PAYMENTS:
                        current_tasks.append(HandlePaymentTask(name=name,
                                                               length=length,
                                                               min_progress=min_progress,
                                                               difficulty=difficulty,
                                                               color=color,
                                                               write_on_terminal=write_on_terminal,
                                                               verbose=verbose,
                                                               description=description))
                    elif topic == Topic.SERVE:
                        current_tasks.append(ServeTask(name=name,
                                                       length=length,
                                                       min_progress=min_progress,
                                                       difficulty=difficulty,
                                                       color=color,
                                                       write_on_terminal=write_on_terminal,
                                                       verbose=verbose,
                                                       description=description))

                # add subtasks
                for i, t in enumerate(current_tasks):
                    if i == 0:
                        self.starter_tasks.append(t)
                    if i != len(current_tasks) - 1:
                        t.subtask = current_tasks[i+1]
                    self.tasks.append(t)

            self.time_between_task = int(file.readline())
            self.refresh_rate = int(file.readline())
            self.auction_timeout = int(file.readline())
