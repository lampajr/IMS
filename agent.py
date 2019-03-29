import datetime
import random
import threading
import time

from termcolor import colored, cprint

from auctioneer import get_time
from message import *
from pubsub import pub


def update_state(agent):
    return None


class Ability:

    def __init__(self, energy=100, cleverness=0, speed=0, stars=0):
        self.energy = energy            # value from 0 to 100
        self.cleverness = cleverness    # value from 0 to 100
        self.speed = speed              # value from 0 to 100
        self.stars = stars              # michelin's star 0 to 3


# TODO: fix a state for the agent
class Agent(threading.Thread):

    """ Abstract Agent implementation """

    def __init__(self, agent_id, name, topic, contract_time, ability=None, write_terminal=False, details=False):
        super(Agent, self).__init__()
        self.write_on_terminal = write_terminal
        self.details = details
        self.agent_name = name
        self.agent_id = agent_id
        self.topic = topic
        self.invalidated = False
        self.occupied = False
        self.ability = ability
        self.current_task = None
        self.current_auction = None
        self.last_renewal = None
        self.contract_time = contract_time
        self.start()
        #self.run()

    def run(self):
        self.log("I'm agent " + self.agent_name + " and I'm subscribing to the following topic = " + self.topic.value)
        pub.subscribe(self.body, self.topic.value)

    def invalidate(self):
        self.invalidated = True

    def restore(self):
        self.invalidated = False

    def execute_task(self):
        if self.current_task is not None:
            self.log("I'm executing the " + self.current_task.name)
            try:
                self.current_task.execute(value=random.randint(0, 100))
            except AttributeError:
                pass
            if self.current_task.is_terminated:
                self.reset()

    def reset(self):
        self.current_task = None
        self.current_auction = None
        self.occupied = False
        self.last_renewal = None
        self.ability = update_state(self)

    def body(self, arg1):

        """ the body of the agent, what it should do when requested
            in according to the kind of message received (arg1)"""

        if self.invalidated:
            # simulate the robot's failed state
            # so discard everything
            return

        # this means that the auctioneer has reallocated my task
        # limit needs to be the same or greater wrt the contract limit of
        # the auctioneer
        if self.occupied and self.last_renewal is not None \
                and ((get_time() - self.last_renewal) / 1000) > self.contract_time:
            self.reset()
            # invalidate myself for some time
            self.invalidate()
            self.log(message="I'm failed!")
            time.sleep(3)
            self.restore()

        if arg1.msg_type == MessageType.ANNOUNCEMENT:
            if not self.occupied:
                if self.details:
                    self.log("new message received = " + str(arg1.msg_type.name))
                self.on_announce(msg=arg1)
        elif arg1.msg_type == MessageType.RENEWAL and arg1.winner_id == self.agent_id:
            if self.details:
                self.log("new message received = " + str(arg1.msg_type.name))
            if self.current_task is not None and not self.current_task.is_terminated:
                self.on_renewal(msg=arg1)
        elif arg1.msg_type == MessageType.CLOSE:
            if self.details:
                self.log("new message received = " + str(arg1.msg_type.name))
            self.on_close(msg=arg1)

    def on_announce(self, msg):
        self.current_auction = msg.auction_id
        self.current_task = msg.task
        self.occupied = True

        fitness = self.current_task.metric(ability=self.ability)

        # generate bid message
        msg = BidMessage(auction_id=self.current_auction,
                         agent_id=self.agent_id,
                         value=fitness)
        if self.details:
            self.log("sending BID message..")
        # send bid to the auctioneer
        pub.sendMessage(topicName=self.topic.value, arg1=msg)

    def on_renewal(self, msg):
        if self.check_msg(msg):
            # discard any message not related to the current auction
            # or if i'm not the winner
            return

        if self.details:
            self.log("contract renewal occurred..")
        self.last_renewal = get_time()
        self.execute_task()

        # generate ack message
        msg = AcknowledgementMessage(auction_id=self.current_auction,
                                     ack_id=msg.renewal_id)
        # notify auctioneer that I'm working
        if self.details:
            self.log("sending ACK message..")
        pub.sendMessage(topicName=self.topic.value, arg1=msg)

    def on_close(self, msg):
        if self.check_msg(msg):
            # discard any message not related to the current auction
            # or if i'm not the winner
            self.reset()
            return
        if self.details:
            self.log("I'm the winner!!")
            self.log("I'm going to start the task.")
        self.occupied = True
        self.execute_task()

    def check_msg(self, msg):
        return msg.auction_id != self.current_auction or msg.winner_id != self.agent_id


    ##### LOG METHODS #####


    def log(self, message, use_time=False):
        if self.write_on_terminal:
            self.terminal_log(message=message,
                              use_time=use_time)
        else:
            self.file_log(message=message,
                          use_time=use_time)

    def file_log(self, message, use_time):
        with open("output.txt", "a+") as f:
            prefix = '          [' + str(self.agent_id) + ':' + self.agent_name + ']'
            res = ""
            if use_time:
                res += '{' + str(datetime.datetime.now().time()) + '}'
            f.write(res + prefix + " -> " + message + "\n")

    def terminal_log(self, message, use_time):
        lo = threading.Lock()
        lo.acquire()
        prefix = '      [' + str(self.agent_id) + ':' + self.agent_name + ']'
        color = 'grey' if self.current_task is None else self.current_task.color
        attrs = [] if self.current_task is None else self.current_task.attrs
        if use_time:
            cprint('{' + str(datetime.datetime.now().time()) + '}', "grey", end=' ')
        cprint(prefix + " -> " + message, color=color, attrs=attrs)
        lo.release()
