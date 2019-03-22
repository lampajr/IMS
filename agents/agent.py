from abc import ABC, abstractmethod
from pubsub import pub


# TODO: consider this class as a thread
class AbstractAgent(ABC):

    """ Abstract Agent implementation """

    # TODO: in the child classes add their specific properties
    def __init__(self, id, name):
        super(AbstractAgent, self).__init__()
        self.agent_name = name
        self.agent_id = id

    @abstractmethod
    def body(self):

        """ the body of the agent, what it should do when requested """

        pass


