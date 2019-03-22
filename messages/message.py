from enum import Enum
from abc import ABC, abstractmethod


class MessageType(Enum):
    ANNOUNCEMENT = 0
    BID = 1
    CLOSE = 2
    RENEWAL = 3
    ACKNOWLEDGEMENT = 4


class GenericMessage(ABC):

    """ generic message exchanged among agents """

    def __init__(self, auction_id, msg_type):
        super(GenericMessage, self).__init__()
        self.msg_type = msg_type
        self.auction_id = auction_id


class AnnouncementMessage(GenericMessage):

    """ Task Announcement message """

    def __init__(self, auction_id, bid_callback):
        super(AnnouncementMessage, self).__init__(auction_id, MessageType.ANNOUNCEMENT)
        self.bid_callback = bid_callback


class RenewalMessage(GenericMessage):

    """ Renewal message sent by auctioneer toward the winner agent """

    def __init__(self,auction_id, winner_id, ack_callback):
        super(RenewalMessage).__init__(auction_id, MessageType.RENEWAL)
        self.winner_id = winner_id
        self.ack_callback = ack_callback


class CloseMessage(GenericMessage):

    """ Close message, sent by the auctioneer towards all other agents """

    def __init__(self, auction_id, winner_id, task):
        super(CloseMessage, self).__init__(auction_id, MessageType.CLOSE)
        self.winner_id = winner_id
        self.task = task


class AcknowledgementMessage(GenericMessage):

    def __init__(self, auction_id):
        super(AcknowledgementMessage, self).__init__(auction_id, MessageType.ACKNOWLEDGEMENT)


class BidMessage(GenericMessage):
    """ Bid message sent by agent toward auctioneer """

    def __init__(self, auction_id, agent_id, value):
        super(BidMessage).__init__(auction_id, MessageType.BID)
        self.value = value
        self.agent_id = agent_id
