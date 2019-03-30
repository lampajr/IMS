import random

from utility import Topic, Subject, Logger
from abc import ABC, abstractmethod
from termcolor import cprint


class Task(Logger, ABC):

    """ Abstract representation of a single Task """

    def __init__(self,
                 name,
                 length,
                 subjects,
                 min_progress,
                 difficulty,
                 color="grey",
                 write_on_terminal=True,
                 verbose=True,
                 attrs=None,
                 level=3):
        super(Task, self).__init__(name, color, attrs, write_on_terminal, verbose, level)

        # task information
        self.task_id = 0 # TODO: generate random task id
        self.length = length
        if subjects is None:
            subjects = []
        self.subjects = subjects
        self.difficulty = difficulty

        # task progress
        self.min_progress = min_progress
        self.progress = 0
        self.previous_progress = None
        self.terminated = False

    @abstractmethod
    def metric(self, ability):
        """ metric function that given the ability of the agent
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

    def __print_progress(self):
        percentage = (self.progress * 100) / self.length

        if percentage <= 100:
            self.log(message="execution {perc}% complete".format(perc=percentage), kind='d')


    def flog(self, message, kind, level):
        pass


class CookTask(Task):

    def __init__(self, name, length, min_progress, difficulty,
                 color="grey", write_on_terminal=True, verbose=True, attrs=None):
        super(CookTask, self).__init__(name=name,
                                       length=length,
                                       subjects=[Subject.COOKERS, Subject.KITCHEN, Subject.INGREDIENTS],
                                       min_progress=min_progress,
                                       difficulty=difficulty,
                                       color=color,
                                       write_on_terminal=write_on_terminal,
                                       verbose=verbose,
                                       attrs=attrs)

    def metric(self, ability):

        # linear combination among all abilities but cleverness
        deterministic_fitness = 0.5 * 20 * ability.stars + 0.4 * ability.energy + 0.1 * ability.speed
        random_fitness = random.randint(0, 30)

        return deterministic_fitness + random_fitness



