from enum import Enum
from abc import ABC, abstractmethod


class MessageType(Enum):
    ANNOUNCEMENT = 0
    BID = 1
    CLOSE = 2
    RENEWAL = 3
    ACKNOWLEDGEMENT = 4


class Message(ABC):

    """ generic message exchanged among agents """

    def __init__(self, auction_id, msg_type):
        super(Message, self).__init__()
        self.msg_type = msg_type
        self.auction_id = auction_id


class Announcement(Message):

    """ Task Announcement message """

    def __init__(self, auction_id, bid_callback):
        super(Announcement, self).__init__(auction_id, MessageType.ANNOUNCEMENT)
        self.bid_callback = bid_callback


class RenewalMessage(Message):

    """ Renewal message sent by auctioneer toward the winner agent """

    def __init__(self,auction_id, winner_id, ack_callback):
        super(RenewalMessage).__init__(auction_id, MessageType.RENEWAL)
        self.winner_id = winner_id
        self.ack_callback = ack_callback


class CloseMessage(Message):

    """ Close message, sent by the auctioneer towards all other agents """

    def __init__(self, auction_id, winner_id, task):
        super(CloseMessage, self).__init__(auction_id, MessageType.CLOSE)
        self.winner_id = winner_id
        self.task = task


# TODO: non penso sia necessario, usare metodi callback
class AcknowledgementMessage(Message):

    def __init__(self, auction_id):
        super(AcknowledgementMessage, self).__init__(auction_id, MessageType.ACKNOWLEDGEMENT)


# TODO: non penso sia necessario, usare metodi callback
class BidMessage(Message):
    """ Bid message sent by agent toward auctioneer """

    def __init__(self, auction_id, agent_id, value):
        super(BidMessage).__init__(auction_id, MessageType.BID)
        self.value = value
        self.agent_id = agent_id
