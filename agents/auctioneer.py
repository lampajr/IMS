import random

from pubsub import pub
import time
import threading as threading

from termcolor import colored

from utilities.message import *
from utilities.task import get_topic


def get_time():
    return int(round(time.time() * 1000))


class Auctioneer(threading.Thread):

    """ Auctioneer implementation """

    def __init__(self, auction_id, max_elapsed_bids_time, contract_time, min_progress):
        super(Auctioneer, self).__init__()
        # message data
        self.task = None
        self.topic = None

        # auction data
        self.auction_id = auction_id
        self.last_renewal = None
        self.bids = []
        self.min_progress = min_progress
        self.max_elapsed_bids_time = max_elapsed_bids_time  # in seconds
        self.contract_time = contract_time
        self.auction_opened = False
        self.winner = None
        self.terminated = False

    def run(self):
        pub.subscribe(self.on_msg_received, topicName=self.topic)
        self.announce_task()

    def compute_winner(self):

        """ compute the winner agent and returns its id """

        winner = None
        for agent_id, value in self.bids:
            if winner is None or value > winner[1]:
                winner = (agent_id, value)

        return winner[0]

    def reset_bids(self):
        self.bids = []

    def trigger_task(self, task):
        self.topic = get_topic(task.subjects).value
        self.task = task
        if not self.isAlive():
            self.start()
        else:
            self.announce_task()

    ###### PUBLISH/SUBSCRIBER COMMUNICATION MODEL ######

    def bid(self, agent_id, value):

        """ callback method used by agents for submitting a bid for claiming a specific task """

        if self.auction_opened:
            self.bids.append((agent_id, value))
            self.my_print("bid received from agent " + str(agent_id) + ", value of " + str(value))

    def acknowledge(self):

        """ callback method used by winner agent after a renewal
            of the contract.
            note: this function needs to be passed in the renewal message """

        if self.task.is_terminated and not self.terminated:
            # terminate the execution
            self.terminated = True
            self.my_print(self.task.name + " task terminated!", color="red")

    def announce_task(self):

        """ publish a TASK ANNOUNCEMENT message on the specific topic
            starting the Auction for the allocation of the task """

        self.auction_opened = True
        self.reset_bids()
        announcement_message = AnnouncementMessage(auction_id=self.auction_id,
                                                   task=self.task)
        self.my_print("new task triggered : " + str(self.task.name))
        self.my_print("sending TASK ANNOUNCEMENT on " + self.topic + " topic")
        self.my_print("awaiting bids..")
        pub.sendMessage(self.topic, arg1=announcement_message)

        # put current execution at sleep for 'time limit' slot
        time.sleep(self.max_elapsed_bids_time)
        # enough time was passed.. close the auction and choose the winner
        self.close_auction()

    def close_auction(self):

        """ publish a CLOSE AUCTION message that will close the auction,
            it encapsulate the id of the winner agent such that it will
            recognize the fact that it has to perform that task """

        self.auction_opened = False

        self.winner = self.compute_winner()
        self.my_print("there is onw winner => " + str(self.winner))
        close_message = CloseMessage(auction_id=self.auction_id,
                                     winner_id=self.winner)
        self.my_print("sending CLOSE message..")
        pub.sendMessage(self.topic, arg1=close_message)

        self.start_loop_check_progress()

    def start_loop_check_progress(self):
        while not self.task.is_terminated and (self.task.progress - self.task.previous_progress) >= self.min_progress:
            self.send_renewal()
            time.sleep(3)

        if not self.task.is_terminated:
            # we need to reallocate the task
            self.my_print("I need to reallocate the " + self.task.name + " task cause something went wrong")
            # change auction id
            self.auction_id = "a" + str(random.randint(0, 500))
            self.reset_bids()
            self.trigger_task(task=self.task)
        else:
            # terminate the execution
            if not self.terminated:
                self.terminated = True
                self.my_print(self.task.name + " task terminated!", color="red")

    def send_renewal(self):

        """ send a RENEWAL message on the specific topic,
            it is addressed to the previous winner """

        renewal_message = RenewalMessage(auction_id=self.auction_id,
                                         winner_id=self.winner)
        self.last_renewal = get_time()
        self.my_print("sending RENEWAL of task" + str(self.task.task_id) + " to agent " + str(self.winner) + "..")
        pub.sendMessage(self.topic, arg1=renewal_message)

    def on_msg_received(self, arg1):
        if arg1.auction_id != self.auction_id:
            # discard any message on the topic that is not related to
            # the current auction
            return

        if arg1.msg_type == MessageType.BID:
            self.my_print("new message received " + str(arg1.msg_type.name))
            self.bid(agent_id=arg1.agent_id,
                     value=arg1.value)
        elif arg1.msg_type == MessageType.ACKNOWLEDGEMENT:
            self.my_print("new message received " + str(arg1.msg_type.name))
            self.acknowledge()

    def my_print(self, message, color=None):
        prefix = '[' + str(self.auction_id) + ':auctioneer]'
        if color is None:
            color = self.task.color
        print(colored(prefix + " -> " + message, color=color))
