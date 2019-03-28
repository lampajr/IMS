from agent import Agent
from auctioneer import *
from task import *

# TODO: change metric computation
# TODO: setup state of the agent (think if add env or not)


if __name__ == '__main__':
    contract_time = 40
    min_progress = 10

    ##### TASKS ####

    task1 = CookTask(task_id="c" + str(1),
                     name="amatriciana",
                     length=200,
                     difficulty=5,
                     color="green",
                     write_on_terminal=True)

    task2 = CookTask(task_id="c" + str(2),
                     name="carbonara",
                     length=200,
                     difficulty=5,
                     color="blue",
                     write_on_terminal=True)

    #### AGENTS #####

    agent1 = Agent(agent_id=1,
                   name="Main-Chef",
                   topic=Topic.COOK,
                   contract_time=contract_time,
                   write_terminal=True)

    agent2 = Agent(agent_id=2,
                   name="Sub-Chef",
                   topic=Topic.COOK,
                   contract_time=contract_time,
                   write_terminal=True)

    agent3 = Agent(agent_id=3,
                   name="Sub-Chef",
                   topic=Topic.COOK,
                   contract_time=contract_time,
                   write_terminal=True)

    agent4 = Agent(agent_id=4,
                   name="Sub-Chef",
                   topic=Topic.COOK,
                   contract_time=contract_time,
                   write_terminal=True)

    agent5 = Agent(agent_id=5,
                   name="Sub-Chef",
                   topic=Topic.COOK,
                   contract_time=contract_time,
                   write_terminal=True)

    agent6 = Agent(agent_id=6,
                   name="Sub-Chef",
                   topic=Topic.COOK,
                   contract_time=contract_time,
                   write_terminal=True)

    agent7 = Agent(agent_id=7,
                   name="Waiter George",
                   topic=Topic.DISH_OUT,
                   contract_time=contract_time,
                   write_terminal=True)

    agent8 = Agent(agent_id=8,
                   name="Waiter Mike",
                   topic=Topic.DISH_OUT,
                   contract_time=contract_time,
                   write_terminal=True)

    agent9 = Agent(agent_id=9,
                   name="Waiter George",
                   topic=Topic.DISH_OUT,
                   contract_time=contract_time,
                   write_terminal=True)

    agent10 = Agent(agent_id=10,
                    name="Waiter Mike",
                    topic=Topic.DISH_OUT,
                    contract_time=contract_time,
                    write_terminal=True)

    agent11 = Agent(agent_id=11,
                    name="Cashier Melania",
                    topic=Topic.HANDLE_PAYMENTS,
                    contract_time=contract_time,
                    write_terminal=True)

    agent12 = Agent(agent_id=12,
                    name="Cashier John",
                    topic=Topic.HANDLE_PAYMENTS,
                    contract_time=contract_time,
                    write_terminal=True)

    ##### AUCTIONEERS #####

    auctioneer1 = generate_auctioneer(contract_time=contract_time,
                                      min_progress=min_progress,
                                      write_on_terminal=True)

    auctioneer2 = generate_auctioneer(contract_time=contract_time,
                                      min_progress=min_progress,
                                      write_on_terminal=True)

    auctioneer1.trigger_task(task=task1)

    time.sleep(5)

    auctioneer2.trigger_task(task=task2)
