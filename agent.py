import random
import threading
import time

from pubsub import pub
from termcolor import cprint

from message import BidMessage, AcknowledgementMessage
from utility import MAX_ID, Logger, get_time, MessageType


class Skill:

    """ represents the skills of an agent """

    def __init__(self, energy=100, cleverness=0, speed=0, stars=0):
        self.energy = energy            # value from 0 to 100
        self.cleverness = cleverness    # value from 0 to 100
        self.speed = speed              # value from 0 to 100
        self.stars = stars              # michelin's star 0 to 3


class Agent(threading.Thread):

    """ Agent implementation """

    BASE_NAME = "Agent"

    def __init__(self,
                 name,
                 topic,
                 contract_time,
                 skill,
                 write_on_terminal=True,
                 verbose=False,
                 attrs=None,
                 color=None,
                 level=1):

        super(Agent, self).__init__()

        self.agent_id = Agent.BASE_NAME + str(random.randint(0, MAX_ID))
        self.logger = Logger(name, color, attrs, write_on_terminal, verbose, level)
        self.skill = skill
        self.topic = topic
        self.contract_time = contract_time
        self.failed = False
        self.occupied = False
        self.executing = False
        self.current_task = None
        self.current_auction = None
        self.last_renewal = None
        self.run()

    def run(self):
        self.logger.log(message="I'm {name} with {id} id and {top} topic!!".format(name=self.logger.name,
                                                                                   id=self.agent_id,
                                                                                   top=self.topic.value))
        pub.subscribe(self.on_message_received, topicName=self.topic.value)

    def invalidate(self):

        """ fail the current agent """

        self.failed = True
        self.__reset()
        self.logger.log(message="I'm failed!! :(")

    def repair(self):

        """ repair the current agent """

        self.failed = False
        self.__reset()
        self.logger.log(message="I'm back! :)")

    def on_message_received(self, arg1):

        """ callback methods called whenever a new message is received on my topic """

        # discard any message if the agent has failed
        if self.failed:
            return

        # this means that the auctioneer has reallocated my task
        # limit needs to be the same or greater wrt the contract limit of
        # the auctioneer
        if self.executing and self.last_renewal is not None and ((get_time() - self.last_renewal) / 1000) > self.contract_time:
            # invalidate myself for a while
            self.invalidate()
            time.sleep(5)
            self.repair()

        if not self.failed:
            if arg1.msg_type == MessageType.ANNOUNCEMENT:
                if not self.occupied:
                    self.logger.log("New message received = " + str(arg1.msg_type.name))
                    self.on_announce(msg=arg1)
            elif arg1.msg_type == MessageType.RENEWAL and self.current_auction is not None \
                    and arg1.auction_id == self.current_auction and arg1.winner_id == self.agent_id:
                self.logger.log("New message received = " + str(arg1.msg_type.name))
                if self.current_task is not None and not self.current_task.terminated:
                    self.on_renewal(msg=arg1)
            elif arg1.msg_type == MessageType.CLOSE and not self.executing and self.occupied:
                self.logger.log("New message received = " + str(arg1.msg_type.name))
                self.on_close(msg=arg1)

    def on_announce(self, msg):

        """ react to the task announcement computing the fitness and
            sending a BID message back to the auctioneer """

        self.current_task = msg.task
        self.current_auction = msg.auction_id
        self.occupied = True

        fitness = self.current_task.metric(skill=self.skill)
        # generate bid message
        bid_message = BidMessage(auction_id=self.current_auction,
                                 agent_id=self.agent_id,
                                 value=fitness)
        self.logger.log(message="Sending BID message..")
        pub.sendMessage(topicName=self.topic.value, arg1=bid_message)

    def on_close(self, msg):

        """ react to the close auction message checking whether I'm the winner """

        if msg.winner_id != self.agent_id:
            self.__reset()
        else:
            # i'm the winner.. time-limited contract established
            self.logger.log(message="I'm the winner!!!")
            self.logger.log(message="I'm going to execute the task..")
            self.executing = True
            self.logger.color = self.current_task.logger.color
            self.__execute_task()


    def on_renewal(self, msg):

        """ react to the contract renewal executing a portion of task
            and replying back with the ACK message """

        self.logger.log(message="Time-limited contract renewed!")
        self.last_renewal = get_time()
        self.__execute_task()

        # generate ack message
        ack_message = AcknowledgementMessage(auction_id=self.current_auction,
                                             ack_id=msg.renewal_id)
        # notify auctioneer that I'm working
        self.logger.log("Sending ACK message..")
        pub.sendMessage(topicName=self.topic.value, arg1=ack_message)

    def __execute_task(self):
        try:
            self.current_task.execute(value=random.randint(0, 100))
            self.logger.log("I'm performing the task..")
            if self.current_task.terminated:
                self.__reset()
        except AttributeError:
            pass

    def __reset(self):
        self.current_task = None
        self.current_auction = None
        self.occupied = False
        self.executing = False
        self.last_renewal = None
        self.logger.color = None
