import datetime
import random

from pubsub import pub
import time
import threading as threading

from termcolor import colored, cprint

from message import *
from task import get_topic


def get_time():
    return int(round(time.time() * 1000))


def generate_auctioneer(max_elapsed_bids_time=5, contract_time=10,
                        min_progress=30, write_on_terminal=False, max_id=500):

    return Auctioneer(auction_id="auct" + str(random.randint(0, max_id)),
                      max_elapsed_bids_time=int(max_elapsed_bids_time),
                      contract_time=int(contract_time),
                      min_progress=int(min_progress),
                      write_terminal=write_on_terminal)


class Auctioneer(threading.Thread):

    """ Auctioneer implementation """

    def __init__(self, auction_id, max_elapsed_bids_time, contract_time,
                 min_progress, write_terminal=False, discard_task=False,
                 details=False):
        super(Auctioneer, self).__init__()
        # message data
        self.details = details
        self.task = None
        self.topic = None
        self.write_on_terminal = write_terminal
        self.discard_task=discard_task

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
        self.ack_stack = []

    def run(self):
        pub.subscribe(self.on_msg_received, topicName=self.topic)
        self.announce_task()

    def compute_winner(self):

        """ compute the winner agent and returns its id """

        if len(self.bids) == 0:
            if self.discard_task:
                self.log(message="There are no bids.. task discarded!")
                return None
            else:
                self.announce_task()
                return
        else:
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
            self.log("bid received from agent " + str(agent_id) + ", value of " + str(value))

    def on_acknowledge(self, ack_id):

        """ callback method used by winner agent after a renewal
            of the contract.
            note: this function needs to be passed in the renewal message """

        last_id = self.ack_stack.pop()

        if last_id != ack_id:
            # wrong order renewal-ack
            pass

        if self.task.is_terminated and not self.terminated:
            # terminate the execution
            self.terminated = True
            self.log(self.task.name + " task terminated!", color="red")

    def announce_task(self):

        """ publish a TASK ANNOUNCEMENT message on the specific topic
            starting the Auction for the allocation of the task """

        self.auction_opened = True
        self.reset_bids()
        announcement_message = AnnouncementMessage(auction_id=self.auction_id,
                                                   task=self.task)
        self.log("------------------------------------------------------")
        if self.task.progress == 0:
            # new task
            self.log("new task triggered : " + str(self.task.name))
        else:
            # task re-allocation
            self.log("task reallocation : " + str(self.task.name))
        self.log("sending TASK ANNOUNCEMENT on " + self.topic + " topic")
        self.log("awaiting bids..")
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

        if self.winner is None:
            return

        if self.details:
            self.log("there is a winner => " + str(self.winner))
        close_message = CloseMessage(auction_id=self.auction_id,
                                     winner_id=self.winner)
        if self.details:
            self.log("sending CLOSE message..")
        pub.sendMessage(self.topic, arg1=close_message)

        self.start_loop_check_progress()

    def start_loop_check_progress(self):
        while not self.task.is_terminated and (self.task.progress - self.task.previous_progress) >= self.min_progress:
            if len(self.ack_stack) != 0:
                # the ack msg related to the previous renewal was not yet received
                self.reallocate(log_msg=" task cause no ack received!")
            self.send_renewal()
            time.sleep(3)

        if not self.task.is_terminated:
            self.reallocate(log_msg=" task cause the progress wasn't enough!")
        else:
            # terminate the execution
            if not self.terminated:
                self.terminated = True
                self.log(self.task.name + " task terminated!", color="red")

    def reallocate(self, log_msg):

        """ reallocate the current task """

        # we need to reallocate the task
        self.log("I need to reallocate the " + self.task.name + log_msg)
        # change auction id
        self.auction_id = self.auction_id + str(random.randint(0, 50))
        self.reset_bids()
        self.trigger_task(task=self.task)

    def send_renewal(self):

        """ send a RENEWAL message on the specific topic,
            it is addressed to the previous winner """

        renewal_id = random.randint(0, 500)
        self.ack_stack.append(renewal_id)
        renewal_message = RenewalMessage(auction_id=self.auction_id,
                                         winner_id=self.winner,
                                         renewal_id=renewal_id)
        self.last_renewal = get_time()
        if self.details:
            self.log("sending RENEWAL of task " + str(self.task.task_id) + " to agent " + str(self.winner) + "..")
        pub.sendMessage(self.topic, arg1=renewal_message)

    def on_msg_received(self, arg1):
        if arg1.auction_id != self.auction_id:
            # discard any message on the topic that is not related to
            # the current auction
            return

        if arg1.msg_type == MessageType.BID:
            if self.details:
                self.log("new message received " + str(arg1.msg_type.name))
            self.bid(agent_id=arg1.agent_id,
                     value=arg1.value)
        elif arg1.msg_type == MessageType.ACKNOWLEDGEMENT:
            if self.details:
                self.log("new message received " + str(arg1.msg_type.name))
            self.on_acknowledge(arg1.ack_id)


    ##### LOG METHODS #####


    def log(self, message, color=None, use_time=False):
        if self.write_on_terminal:
            self.terminal_log(message=message,
                              color=color,
                              use_time=use_time)
        else:
            self.file_log(message=message,
                          use_time=use_time)

    def file_log(self, message, use_time):
        with open("output.txt", "a+") as f:
            prefix = '[' + str(self.auction_id) + ':auctioneer]'
            res = ""
            if use_time:
                res += '{' + str(datetime.datetime.now().time()) + '}'
            f.write(res + prefix + " -> " + message + "\n")

    def terminal_log(self, message, color, use_time):
        lo = threading.Lock()
        lo.acquire()
        prefix = '[' + str(self.auction_id) + ':auctioneer]'
        if color is None:
            color = self.task.color
        attrs = self.task.attrs
        if use_time:
            cprint('{' + str(datetime.datetime.now().time()) + '}', "grey", end=' ')
        cprint(prefix + " -> " + message, color=color, attrs=attrs)
        lo.release()
