from pubsub import pub
import time
import threading as threading

from utilities.message import *
from utilities.task import get_topic


def get_time():
    return int(round(time.time() * 1000))


def prova(agent_id, value):
    print(agent_id, 'received value =', value)


# TODO: consider also this class as a thread
class Auctioneer:

    """ Abstract Auctioneer implementation """

    def __init__(self, time_limit, contract_limit):
        super(Auctioneer, self).__init__()
        # message data
        self.task = None
        self.topic = None

        # auction data
        self.auction_id = None
        self.last_renewal = None
        self.bids = []
        self.lock = threading.Lock()
        self.time_limit = time_limit
        self.contract_limit = contract_limit
        self.auction_started_time = None
        self.auction_opened = False
        self.winner = None

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
        self.auction_id = task.task_id
        pub.subscribe(self.on_msg_received, topicName=self.topic)
        self.announce_task()

    ###### PUBLISH/SUBSCRIBER COMMUNICATION MODEL ######

    def bid(self, agent_id, value):

        """ callback method used by agents for submitting a bid for claiming a specific task """

        #self.lock.acquire()
        elapsed_time = get_time() - self.auction_started_time if self.auction_started_time is not None else None

        # check whether enough time is passed
        if self.auction_opened and elapsed_time is not None and elapsed_time <= self.time_limit:
            # accept the bid
            self.bids.append((agent_id, value))
            print('Bid: ', value, 'received from ', agent_id)
        elif self.auction_opened and elapsed_time is not None and elapsed_time > self.time_limit:
            print('enough time elapsed:', elapsed_time)
            self.close_auction()

        # release the lock on this method
        #self.lock.release()

    def acknowledge(self):

        """ callback method used by winner agent after a renewal
            of the contract.
            note: this function needs to be passed in the renewal message """

        elapsed_time = get_time() - self.last_renewal
        #if elapsed_time > self.contract_limit and not self.task.is_terminated():
            # resetting all the data
            # reassign the task
        #    pass
        if self.task.is_terminated():
            # terminate the execution
            print(self.auction_id, ': task n.', self.task.task_id, 'terminated!!')

    def announce_task(self):

        """ publish a TASK ANNOUNCEMENT message on the specific topic
            starting the Auction for the allocation of the task """

        self.auction_opened = True

        announcement_message = AnnouncementMessage(auction_id=self.auction_id,
                                                   task=self.task)
        print(self.auction_id, ': TASK ANNOUNCEMENT -> ', self.task.task_id, 'on topic=', self.topic)
        pub.sendMessage(self.topic, arg1=announcement_message)
        pass

    def close_auction(self):

        """ publish a CLOSE AUCTION message that will close the auction,
            it encapsulate the id of the winner agent such that it will
            recognize the fact that it has to perform that task """

        self.auction_opened = False

        self.winner = self.compute_winner()
        close_message = CloseMessage(auction_id=self.auction_id,
                                     winner_id=self.winner)
        print(self.auction_id, ': CLOSE AUCTION')
        pub.sendMessage(self.topic, arg1=close_message)

    def send_renewal(self):

        """ send a RENEWAL message on the specific topic,
            it is addressed to the previous winner """

        renewal_message = RenewalMessage(auction_id=self.auction_id,
                                         winner_id=self.winner)
        self.last_renewal = get_time()
        print(self.auction_id, ': RENEWAL to', self.winner,' of task ', self.task.task_id)
        pub.sendMessage(self.topic, arg1=renewal_message)

    def on_msg_received(self, arg1):
        if arg1.auction_id != self.auction_id:
            # discard any message on the topic that is not related to
            # the current auction
            return

        if arg1.msg_type == MessageType.BID:
            print(self.auction_id, ': new message received', arg1.msg_type)
            self.bid(agent_id=arg1.agent_id,
                     value=arg1.value)
        elif arg1.msg_type == MessageType.ACKNOWLEDGEMENT:
            print(self.auction_id, ': new message received', arg1.msg_type)
            self.acknowledge()
