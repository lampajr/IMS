import random

from auctioneer import allocate_task
from utility import Subject, Logger, MAX_ID
from abc import ABC, abstractmethod


class Task(ABC):

    """ Abstract representation of a single Task """

    BASE_NAME = "task"

    def __init__(self,
                 name,
                 length,
                 subjects,
                 min_progress,
                 difficulty,
                 color="grey",
                 write_on_terminal=True,
                 verbose=False,
                 attrs=None,
                 level=3,
                 description=None,
                 subtask=None):

        super(Task, self).__init__()

        # task information
        self.logger = Logger(name=name,
                             color=color,
                             attrs=attrs,
                             write_on_terminal=write_on_terminal,
                             verbose=verbose,
                             level=level,
                             description=description)

        self.task_id = Task.BASE_NAME + str(random.randint(0, MAX_ID))
        self.length = length
        if subjects is None:
            subjects = []
        self.subjects = subjects
        self.difficulty = difficulty
        self.subtask = subtask

        # task progress
        self.min_progress = min_progress
        self.percentage = 0
        self.progress = 0
        self.previous_progress = -1000000
        self.terminated = False
        self.allocated = False
        self.generated = False

    @abstractmethod
    def metric(self, skill):
        """ metric function that given the skills of the agent
            returns a fitness score representing how much the
            agent is good for doing this task """
        pass

    def execute(self, value):

        """ execute the task, increasing the progress """

        self.previous_progress = self.progress
        self.progress += value
        self.__print_progress()
        self.__check_termination()

    def __check_termination(self):

        """ checks whether the task is terminated or not """

        if self.progress >= self.length:
            self.terminated = True
            # start the subtask if any
            self.__start_subtask()

    def __start_subtask(self):

        """ start the next task, if any """

        if self.subtask is not None:
            allocate_task(task=self.subtask)

    def __print_progress(self):

        """ print progress information """

        self.percentage = int((self.progress * 100) / self.length)

        if self.percentage <= 100:
            self.logger.log(message="execution {perc}% complete".format(perc=self.percentage))
        else:
            self.percentage = 100
            self.logger.log(message="task completed!!!!  <---------", kind='e')


class CookTask(Task):

    def __init__(self, name, length, min_progress, difficulty, subtask=None,
                 color="grey", write_on_terminal=True, verbose=False, attrs=None, description=""):
        super(CookTask, self).__init__(name=name,
                                       length=length,
                                       subjects=[Subject.COOKERS, Subject.KITCHEN, Subject.INGREDIENTS],
                                       min_progress=min_progress,
                                       difficulty=difficulty,
                                       color=color,
                                       write_on_terminal=write_on_terminal,
                                       verbose=verbose,
                                       attrs=attrs,
                                       description=description,
                                       subtask=subtask)

    def metric(self, skill):

        # linear combination among all abilities but cleverness
        deterministic_fitness = 0.8 * 20 * skill.stars + 0.4 * skill.energy + 0.1 * skill.speed
        random_fitness = random.randint(0, 50)

        return deterministic_fitness + random_fitness


class ServeTask(Task):

    def __init__(self, name, length, min_progress, difficulty, subtask=None,
                 color="grey", write_on_terminal=True, verbose=False, attrs=None, description=""):
        super(ServeTask, self).__init__(name=name,
                                        length=length,
                                        subjects=[Subject.DISH, Subject.TRAYS],
                                        min_progress=min_progress,
                                        difficulty=difficulty,
                                        color=color,
                                        write_on_terminal=write_on_terminal,
                                        verbose=verbose,
                                        attrs=attrs,
                                        description=description,
                                        subtask=subtask)

    def metric(self, skill):

        # linear combination among all abilities but stars
        deterministic_fitness = 0.1 * skill.cleverness + 0.4 * skill.energy + 0.5 * skill.speed
        random_fitness = random.randint(0, 20)

        return deterministic_fitness + random_fitness


class HandlePaymentTask(Task):

    def __init__(self, name, length, min_progress, difficulty, subtask=None,
                 color="grey", write_on_terminal=True, verbose=False, attrs=None, description=""):
        super(HandlePaymentTask, self).__init__(name=name,
                                                length=length,
                                                subjects=[Subject.CASH_DESK],
                                                min_progress=min_progress,
                                                difficulty=difficulty,
                                                color=color,
                                                write_on_terminal=write_on_terminal,
                                                verbose=verbose,
                                                attrs=attrs,
                                                description=description,
                                                subtask=subtask)

    def metric(self, skill):

        # linear combination among all abilities but stars
        deterministic_fitness = 0.7 * skill.cleverness + 0.2 * skill.energy + 0.1 * skill.speed
        random_fitness = random.randint(0, 30)

        return deterministic_fitness + random_fitness
