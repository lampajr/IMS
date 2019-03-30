from abc import ABC
from utility import MessageType


class GenericMessage(ABC):

    """ generic message exchanged among agents """

    def __init__(self, auction_id, msg_type):
        super(GenericMessage, self).__init__()
        self.msg_type = msg_type
        self.auction_id = auction_id


class AnnouncementMessage(GenericMessage):

    """ Task Announcement message """

    def __init__(self, auction_id, task):
        super(AnnouncementMessage, self).__init__(auction_id, MessageType.ANNOUNCEMENT)
        self.task = task


class BidMessage(GenericMessage):

    """ Bid message sent by agent toward auctioneer """

    def __init__(self, auction_id, agent_id, value):
        super(BidMessage, self).__init__(auction_id, MessageType.BID)
        self.value = value
        self.agent_id = agent_id


class RenewalMessage(GenericMessage):

    """ Renewal message sent by auctioneer toward the winner agent """

    def __init__(self,auction_id, winner_id, renewal_id):
        super(RenewalMessage, self).__init__(auction_id, MessageType.RENEWAL)
        self.winner_id = winner_id
        self.renewal_id = renewal_id


class CloseMessage(GenericMessage):

    """ Close message, sent by the auctioneer towards all other agents """

    def __init__(self, auction_id, winner_id):
        super(CloseMessage, self).__init__(auction_id, MessageType.CLOSE)
        self.winner_id = winner_id


class AcknowledgementMessage(GenericMessage):

    def __init__(self, auction_id, ack_id):
        super(AcknowledgementMessage, self).__init__(auction_id, MessageType.ACKNOWLEDGEMENT)
        self.ack_id = ack_id