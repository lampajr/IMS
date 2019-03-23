import random
import threading
import time

from agents.auctioneer import get_time
from utilities.message import *
from pubsub import pub


def update_state(agent):
    return None


# TODO: consider this class as a thread ??
class Agent(threading.Thread):

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
        self.start()

    def run(self):
        print("I'm agent", self.agent_name, " and I'm subscribing to topic=", self.topic.value)
        pub.subscribe(self.body, self.topic.value)

    def execute_task(self):
        if self.current_task is not None:
            if self.current_task.is_terminated:
                self.reset()
            else:
                print('Hi! Agent ', self.agent_id, ' is executing task ', self.current_task.task_id, ':')
                self.current_task.execute(value=random.randint(0, 10))

    def reset(self):
        self.current_task = None
        self.current_auction = None
        self.state = update_state(self)

    def body(self, arg1):

        """ the body of the agent, what it should do when requested
            in according to the kind of message received (arg1)"""


        if self.last_renewal is not None and get_time() - self.last_renewal > self.time_limit:
            self.reset()

        if arg1.msg_type == MessageType.ANNOUNCEMENT:
            print(self.agent_name, ": Message received ->", arg1.msg_type)
            self.on_announce(msg=arg1)
        elif arg1.msg_type == MessageType.RENEWAL:
            print(self.agent_name, ": Message received ->", arg1.msg_type)
            self.on_renewal(msg=arg1)
        elif arg1.msg_type == MessageType.CLOSE:
            print(self.agent_name, ": Message received ->", arg1.msg_type)
            self.on_close(msg=arg1)

    def on_announce(self, msg):
        self.my_print("on announce")
        self.current_auction = msg.auction_id
        self.current_task = msg.task
        sleep = random.randint(0, 10)
        self.my_print("I will sleep for " + str(sleep))
        time.sleep(sleep)
        fitness = self.current_task.metric(state=self.state)

        # generate bid message
        msg = BidMessage(auction_id=self.current_auction,
                         agent_id=self.agent_id,
                         value=fitness)
        self.my_print("sending bid..")
        # send bid to the auctioneer
        pub.sendMessage(topicName=self.topic.value, arg1=msg)

    def on_renewal(self, msg):
        self.my_print("on renewal")
        if self.check_msg(msg):
            # discard any message not related to the current auction
            # or if i'm not the winner
            return
        self.last_renewal = get_time()
        self.execute_task()

        # generate ack message
        msg = AcknowledgementMessage(auction_id=self.current_auction)
        # notify auctioneer that I'm working
        pub.sendMessage(topicName=self.topic.value, arg1=msg)

    def on_close(self, msg):
        self.my_print("on close")
        if self.check_msg(msg):
            # discard any message not related to the current auction
            # or if i'm not the winner
            self.reset()
            return
        print("I'm agent ", self.agent_id, " and I'm the Winner!!!\n I'm going to start the task.")
        self.execute_task()
        # generate ack message
        msg = AcknowledgementMessage(auction_id=self.current_auction)
        # notify auctioneer that I'm working
        pub.sendMessage(topicName=self.topic.value, arg1=msg)

    def check_msg(self, msg):
        return msg.auction_id != self.current_auction or msg.winner != self.agent_id

    def my_print(self, message):
        print(self.agent_name, ':', message)

