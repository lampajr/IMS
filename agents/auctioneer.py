from pubsub import pub
import time
import threading as threading


def get_time():
    return int(round(time.time() * 1000))


# TODO: consider also this class as a thread
class Auctioneer:

    """ Abstract Auctioneer implementation """

    def __init__(self, time_limit):
        super(Auctioneer, self).__init__()
        # message data
        self.task = None
        self.topic = None

        # auction data
        self.bids = []
        self.lock = threading.Lock()
        self.time_limit = time_limit
        self.auction_started_time = None
        self.auction_opened = False

    def compute_winner(self):

        """ compute the winner agent and returns its id """

        winner = None
        for agent_id, value in self.bids:
            if winner is None or value > winner[1]:
                winner = (agent_id, value)

        return winner[0]

    def reset_bids(self):
        self.bids = []

    def trigger_task(self, topic, task):
        self.topic = topic
        self.task = task
        self.announce_task()

    ###### PUBLISH/SUBSCRIBER COMMUNICATION MODEL ######

    def bid(self, agent_id, value):

        """ callback method used by agents for submitting a bid for claiming a specific task """

        self.lock.acquire()
        elapsed_time = get_time() - self.auction_started_time

        # check whether enough time is passed
        if self.auction_opened and elapsed_time <= self.time_limit:
            # accept the bid
            self.bids.append((agent_id, value))
        elif self.auction_opened and elapsed_time > self.time_limit:
            # TODO: close the auction
            self.auction_opened = False

        # release the lock on this method
        self.lock.release()

    def acknowledge(self):

        """ callback method used by winner agent after a renewal
            of the contract.
            note: this function needs to be passed in the renewal message """

        pass

    def announce_task(self):

        """ publish a TASK ANNOUNCEMENT message on the specific topic
            starting the Auction for the allocation of the task """

        self.auction_opened = True
        pass

    def close_auction(self):

        """ publish a CLOSE AUCTION message that will close the auction,
            it encapsulate the id of the winner agent such that it will
            recognize the fact that it has to perform that task """

        pass

    def send_renewal(self):

        """ send a RENEWAL message on the specific topic,
            it is addressed to the previous winner """

        pass
