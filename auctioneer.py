import random
import threading
import time

from utility import *
from message import *
from pubsub import pub



def allocate_task(task, auction_timeout=5, contract_time=6):

    """ start allocating a new task in the environment """

    auctioneer = Auctioneer(auction_timeout=auction_timeout,
                            contract_time=contract_time)

    auctioneer.allocate_task(task=task)


class Auctioneer(threading.Thread):
    """ Auctioneer implementation """

    BASE_NAME = "auctioneer"

    def __init__(self,
                 auction_timeout,
                 contract_time,
                 discard_task=False,
                 write_on_terminal=True,
                 verbose=False,
                 attrs=None,
                 color=None,
                 level=0):

        super(Auctioneer, self).__init__()

        self.auction_id = Auctioneer.BASE_NAME + "-" + str(random.randint(0, MAX_ID))
        self.logger = Logger(self.auction_id, color, attrs, write_on_terminal, verbose, level)

        # auction data
        self.contract_time = contract_time
        self.auction_timeout = auction_timeout
        self.discard_task = discard_task
        self.bids = []
        self.acks = []
        self.winner = None
        self.opened = False
        self.task = None
        self.task_terminated = False
        self.topic = None
        self.last_renewal = None

    def run(self):
        pub.subscribe(self.on_message_received, topicName=self.topic.value)
        self.announce_task()

    def on_message_received(self, arg1):

        """ methods called whenever a new message is received
            on the subscribed topic """

        # discard any message not related to this auction
        if arg1.auction_id != self.auction_id:
            return

        if arg1.msg_type == MessageType.BID:
            self.logger.log("New message received " + str(arg1.msg_type.name))
            self.__add_bid(agent_id=arg1.agent_id,
                           value=arg1.value)
        elif arg1.msg_type == MessageType.ACKNOWLEDGEMENT:
            self.logger.log("New message received " + str(arg1.msg_type.name))
            self.__acknowledge(arg1.ack_id)

    def announce_task(self):

        """ send a TASK ANNOUNCEMENT message on the current topic """

        self.opened = True
        self.__clear_bids()
        task_announcement_message = AnnouncementMessage(auction_id=self.auction_id,
                                                        task=self.task)
        if self.task.progress == 0:
            # new task
            self.logger.log(message="New task to allocate: {name}".format(name=self.task.logger.name))
        else:
            # reallocation
            self.logger.log(message="Task reallocation of {name}".format(name=self.task.logger.name))
        self.logger.log(message="Sending TASK ANNOUNCEMENT message on {top} topic..".format(top=self.topic.value.upper()))
        pub.sendMessage(topicName=self.topic.value, arg1=task_announcement_message)
        self.logger.log(message="Awaiting bids..")

        # wait bids for auction_timeout time
        time.sleep(self.auction_timeout)

        self.close_auction()

    def renewal_contract(self):

        """ renewal a pre-existing contract sending RENEWAL message on the topic """

        renewal_id = random.randint(0, MAX_ID)
        self.acks.append(renewal_id)

        renewal_message = RenewalMessage(auction_id=self.auction_id,
                                         winner_id=self.winner,
                                         renewal_id=renewal_id)

        self.last_renewal = get_time()
        self.logger.log(message="Sending RENEWAL message of {}..".format(self.task.logger.name))
        pub.sendMessage(topicName=self.topic.value, arg1=renewal_message)

    def close_auction(self):

        """ close the current auction, after computed the winner,
            sending a CLOSE message """

        self.opened = False
        self.winner = self.__compute_winner()

        # whether there is no winner (no bids received)
        if self.winner is None:
            if self.discard_task:
                # no bids received.. discard task
                self.logger.log(message="No bids received.. discard task!")
            else:
                # no bids receive but re-allocate the task
                self.__reallocate(why="no bids received!")
        else:
            self.logger.log(message="There is a winner -> {win}".format(win=self.winner))
            close_message = CloseMessage(auction_id=self.auction_id,
                                         winner_id=self.winner)
            self.logger.log(message="Sending CLOSE message..")
            pub.sendMessage(topicName=self.topic.value, arg1=close_message)
            self.__monitor_progress()

    def allocate_task(self, task):

        """ insert a new task in the environment that has to be allocated """

        self.task = task
        self.topic = get_topic(task.subjects)
        self.logger.color = self.task.logger.color
        if not self.is_alive():
            self.start()
        else:
            self.announce_task()

    def __add_bid(self, agent_id, value):

        """ register a new bid for this auction """

        if self.opened:
            self.bids.append((agent_id, value))
            self.logger.log(message="New bid received from agent {id}, with value={val}".format(id=agent_id,
                                                                                                val=value))

    def __acknowledge(self, ack_id):

        """ check the ack received """

        if ack_id != self.acks.pop():
            # wrong order renewal-ack
            pass

    def __compute_winner(self):
        if len(self.bids) != 0:
            # compute the best bid among all the received ones
            winner = self.bids[0]
            for agent_id, bid in self.bids:
                winner = (agent_id, bid) if bid > winner[1] else winner
            return winner[0]
        else:
            return None

    def __clear_bids(self):
        self.bids.clear()

    def __monitor_progress(self):
        while not self.task.terminated and (self.task.progress - self.task.previous_progress) >= self.task.min_progress:
            self.renewal_contract()
            # wait some seconds
            time.sleep(4)
            if len(self.acks) != 0:
                # no last renewal's ack received
                self.__reallocate(why="no ack received!")

        if not self.task.terminated:
            # I'm exited the cycle due to un-sufficient progress
            self.__reallocate(why="the progress wasn't enough!")
        else:
            # The task was terminated
            self.task_terminated = True

    def __reallocate(self, why=""):

        """ reallocate the same task changing the auction id """

        self.logger.log(message="I need to reallocate the {name} task since ".format(name=self.task.logger.name) + why)

        self.auction_id = self.auction_id + str(random.randint(0, MAX_ID))
        self.allocate_task(task=self.task)