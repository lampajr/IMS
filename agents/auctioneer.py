from pubsub import pub


# TODO: consider also this class as a thread
class Auctioneer:
    """ Abstract Auctioneer implementation """

    def __init__(self, topic):
        super(Auctioneer, self).__init__()
        self.topic = topic
        self.task = None
        self.bids = []

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
        self.task = task
        self.announce_task()

    ###### PUBLISH/SUBSCRIBER COMMUNICATION MODEL ######

    def bid(self, agent_id, value):

        """ callback method used by agents for submitting a bid for claiming a specific task """

        self.bids.append((agent_id, value))

    def acknowledge(self):

        """ callback method used by winner agent after a renewal
            of the contract.
            note: this function needs to be passed in the renewal message """

        pass

    def announce_task(self):

        """ publish a TASK ANNOUNCEMENT message on the specific topic
            starting the Auction for the allocation of the task """

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
