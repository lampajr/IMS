import random
import threading

from utility import Logger, MAX_ID
from pubsub import pub


class Auctioneer(threading.Thread):

    """ Auctioneer implementation """

    BASE_NAME = "auctioneer"

    def __init__(self,
                 max_auction_duration,
                 contract_time,
                 discard_task=False,
                 write_on_terminal=True,
                 verbose=True,
                 attrs=None,
                 color=None,
                 level=0):

        super(Auctioneer, self).__init__()

        self.auction_id = Auctioneer.BASE_NAME + "-" + str(random.randint(0, MAX_ID))
        self.logger = Logger(self.auction_id, color, attrs, write_on_terminal, verbose, level)

        # auction data
        self.contract_time = contract_time
        self.max_auction_duration = max_auction_duration
        self.discard_task = discard_task
        self.bids = []
        self.acks = []
        self.winner = None
        self.opened = False
        self.task = None
        self.topic = None
        self.last_renewal = None

    def run(self):
        pub.subscribe(self.on_message_received, topicName=self.topic)
        self.announce_task()

    def on_message_received(self, arg1):

        """ methods called whenever a new message is received
            on the subscribed topic """

        pass

    def announce_task(self):

        """ send a TASK ANNOUNCEMENT message on the current topic """

        pass

    def renewal_contract(self):

        """ renewal a pre-existing contract sending RENEWAL message on the topic """

        pass

    def close_auction(self):

        """ close the current auction, after computed the winner,
            sending a CLOSE message """

        pass

    def __add_bid(self, agent_id, value):
        if self.opened:
            self.bids.append((agent_id, value))

    def __clear_bids(self):
        self.bids.clear()
