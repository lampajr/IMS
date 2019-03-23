import random
import threading
import time

from termcolor import colored

from agents.auctioneer import get_time
from utilities.message import *
from pubsub import pub


def update_state(agent):
    return None


# TODO: consider this class as a thread ??
class Agent():

    """ Abstract Agent implementation """

    # TODO: in the child classes add their specific properties
    def __init__(self, agent_id, name, topic, time_limit):
        super(Agent, self).__init__()
        self.agent_name = name
        self.agent_id = agent_id
        self.topic = topic
        self.state = None
        self.current_task = None
        self.current_auction = None
        self.last_renewal = None
        self.time_limit = time_limit
        self.run()

    def run(self):
        print("I'm agent " + self.agent_name + " and I'm subscribing to the following topic = " + self.topic.value)
        pub.subscribe(self.body, self.topic.value)

    def execute_task(self):
        if self.current_task is not None:
            if self.current_task.is_terminated:
                self.reset()
            else:
                self.my_print("I'm executing the " + self.current_task.name)
                self.current_task.execute(value=random.randint(0, 100))

    def reset(self):
        self.current_task = None
        self.current_auction = None
        self.state = update_state(self)

    def body(self, arg1):

        """ the body of the agent, what it should do when requested
            in according to the kind of message received (arg1)"""

        if arg1.msg_type == MessageType.ANNOUNCEMENT:
            self.my_print("new message received = " + str(arg1.msg_type.name))
            self.on_announce(msg=arg1)
        elif arg1.msg_type == MessageType.RENEWAL and arg1.winner_id == self.agent_id:
            self.my_print("new message received = " + str(arg1.msg_type.name))
            if self.current_task is not None and not self.current_task.is_terminated:
                self.on_renewal(msg=arg1)
        elif arg1.msg_type == MessageType.CLOSE:
            self.my_print("new message received = " + str(arg1.msg_type.name))
            self.on_close(msg=arg1)

    def on_announce(self, msg):
        self.current_auction = msg.auction_id
        self.current_task = msg.task

        fitness = self.current_task.metric(state=self.state)

        # generate bid message
        msg = BidMessage(auction_id=self.current_auction,
                         agent_id=self.agent_id,
                         value=fitness)
        self.my_print("sending BID message..")
        # send bid to the auctioneer
        pub.sendMessage(topicName=self.topic.value, arg1=msg)

    def on_renewal(self, msg):
        if self.check_msg(msg):
            # discard any message not related to the current auction
            # or if i'm not the winner
            return

        self.my_print("contract renewal occurred..")
        self.last_renewal = get_time()
        self.execute_task()

        # generate ack message
        msg = AcknowledgementMessage(auction_id=self.current_auction)
        # notify auctioneer that I'm working
        self.my_print("sending ACK message..")
        pub.sendMessage(topicName=self.topic.value, arg1=msg)

    def on_close(self, msg):
        if self.check_msg(msg):
            # discard any message not related to the current auction
            # or if i'm not the winner
            self.reset()
            return
        self.my_print("I'm the winner!!")
        self.my_print("I'm going to start the task.")
        self.execute_task()

    def check_msg(self, msg):
        return msg.auction_id != self.current_auction or msg.winner_id != self.agent_id

    def my_print(self, message):
        prefix = '      [' + str(self.agent_id) + ':' + self.agent_name + ']'
        color = 'blue' if self.current_task is None else self.current_task.color
        print(colored(prefix + " -> " + message, color=color))

