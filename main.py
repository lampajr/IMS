from agents.agent import Agent
from agents.auctioneer import Auctioneer
from utilities.message import *
from utilities.task import *


if __name__ == '__main__':
    time_limit = 4
    contract_limit = 1500
    task1 = CookTask(task_id=1,
                     name="Cook spaghetti",
                     length=500,
                     color="green")

    agent1 = Agent(agent_id=1,
                   name="Main Chef",
                   topic=Topic.COOK,
                   time_limit=500)

    agent2 = Agent(agent_id=2,
                   name="Sub-Chef",
                   topic=Topic.COOK,
                   time_limit=500)

    auctioneer1 = Auctioneer(auction_id="a1",
                             time_limit=time_limit,
                             contract_limit=contract_limit)

    auctioneer1.trigger_task(task=task1)