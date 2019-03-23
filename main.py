from agents.agent import Agent
from agents.auctioneer import Auctioneer
from utilities.message import *
from utilities.task import *

# TODO: change metric computation
# TODO: setup state of the agent (think if add env or not)


if __name__ == '__main__':
    contract_time = 40
    min_progress = 40

    ##### TASKS ####

    task1 = CookTask(task_id=1,
                     name="Cook spaghetti",
                     length=500,
                     difficulty=5,
                     color="green")

    task2 = DishOutTask(task_id=2,
                        name="Dish out spaghetti",
                        length=200,
                        difficulty=5,
                        color="blue")

    #### AGENTS #####

    agent1 = Agent(agent_id=1,
                   name="Main-Chef",
                   topic=Topic.COOK,
                   contract_time=contract_time,
                   min_progress=min_progress)

    agent2 = Agent(agent_id=2,
                   name="Sub-Chef",
                   topic=Topic.COOK,
                   contract_time=contract_time,
                   min_progress=min_progress)

    agent3 = Agent(agent_id=3,
                   name="Waiter George",
                   topic=Topic.DISH_OUT,
                   contract_time=contract_time,
                   min_progress=min_progress)

    agent4 = Agent(agent_id=4,
                   name="Waiter Mike",
                   topic=Topic.DISH_OUT,
                   contract_time=contract_time,
                   min_progress=min_progress)

    ##### AUCTIONEERS #####

    auctioneer1 = Auctioneer(auction_id="a1",
                             max_elapsed_bids_time=3,
                             contract_time=contract_time,
                             min_progress=min_progress)

    auctioneer1.trigger_task(task=task1)

    auctioneer2 = Auctioneer(auction_id="a2",
                             max_elapsed_bids_time=3,
                             contract_time=contract_time,
                             min_progress=min_progress)

    #auctioneer2.trigger_task(task=task2)
