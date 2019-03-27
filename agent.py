import datetime
import random
import threading

from termcolor import colored

from auctioneer import get_time
from message import *
from pubsub import pub


def update_state(agent):
    return None


class State:

    def __init__(self, energy, cleverness, speed):
        self.energy = energy            # max value 100%
        self.cleverness = cleverness    # value from 0 to 5
        self.speed = speed              # value from 0 to 5


# TODO: fix a state for the agent
class Agent(threading.Thread):

    """ Abstract Agent implementation """

    # TODO: in the child classes add their specific properties
    def __init__(self, agent_id, name, topic, contract_time, min_progress):
        super(Agent, self).__init__()
        self.agent_name = name
        self.agent_id = agent_id
        self.topic = topic
        self.invalidated = False
        self.occupied = False
        self.state = None
        self.current_task = None
        self.current_auction = None
        self.last_renewal = None
        self.min_progress = min_progress
        self.contract_time = contract_time
        self.start()

    def run(self):
        self.log("I'm agent " + self.agent_name + " and I'm subscribing to the following topic = " + self.topic.value)
        pub.subscribe(self.body, self.topic.value)

    def invalidate(self):
        self.invalidated = True

    def restore(self):
        self.invalidated = False

    def execute_task(self):
        if self.current_task is not None:
            if self.current_task.is_terminated:
                self.reset()
            else:
                self.log("I'm executing the " + self.current_task.name)
                self.current_task.execute(value=random.randint(0, 100))

    def reset(self):
        self.current_task = None
        self.current_auction = None
        self.occupied = False
        self.state = update_state(self)

    def body(self, arg1):

        """ the body of the agent, what it should do when requested
            in according to the kind of message received (arg1)"""

        if self.invalidated:
            # simulate the robot's failed state
            # so discard everything
            return

        if arg1.msg_type == MessageType.ANNOUNCEMENT:
            # this means that the auctioneer has reallocated my task
            # limit needs to be the same or greater wrt the contract limit of
            # the auctioneer
            if self.occupied and (self.current_task.progress - self.current_task.previous_progress) < self.min_progress:
                self.reset()
            if not self.occupied:
                self.log("new message received = " + str(arg1.msg_type.name))
                self.on_announce(msg=arg1)
        elif arg1.msg_type == MessageType.RENEWAL and arg1.winner_id == self.agent_id:
            self.log("new message received = " + str(arg1.msg_type.name))
            if self.current_task is not None and not self.current_task.is_terminated:
                self.on_renewal(msg=arg1)
        elif arg1.msg_type == MessageType.CLOSE:
            self.log("new message received = " + str(arg1.msg_type.name))
            self.on_close(msg=arg1)

    def on_announce(self, msg):
        self.current_auction = msg.auction_id
        self.current_task = msg.task
        self.occupied = True

        fitness = self.current_task.metric(state=self.state)

        # generate bid message
        msg = BidMessage(auction_id=self.current_auction,
                         agent_id=self.agent_id,
                         value=fitness)
        self.log("sending BID message..")
        # send bid to the auctioneer
        pub.sendMessage(topicName=self.topic.value, arg1=msg)

    def on_renewal(self, msg):
        if self.check_msg(msg):
            # discard any message not related to the current auction
            # or if i'm not the winner
            return

        self.log("contract renewal occurred..")
        self.last_renewal = get_time()
        self.execute_task()

        # generate ack message
        msg = AcknowledgementMessage(auction_id=self.current_auction,
                                     ack_id=msg.renewal_id)
        # notify auctioneer that I'm working
        self.log("sending ACK message..")
        pub.sendMessage(topicName=self.topic.value, arg1=msg)

    def on_close(self, msg):
        if self.check_msg(msg):
            # discard any message not related to the current auction
            # or if i'm not the winner
            self.reset()
            return
        self.log("I'm the winner!!")
        self.log("I'm going to start the task.")
        self.occupied = True
        self.execute_task()

    def check_msg(self, msg):
        return msg.auction_id != self.current_auction or msg.winner_id != self.agent_id

    def log(self, message, use_time=False):
        prefix = '      [' + str(self.agent_id) + ':' + self.agent_name + ']'
        color = 'grey' if self.current_task is None else self.current_task.color
        res = ""
        if use_time:
            res += colored('{' + str(datetime.datetime.now().time()) + '}', "grey")
        print(res + colored(prefix + " -> " + message, color=color))

