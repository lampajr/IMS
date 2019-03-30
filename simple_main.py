from agentBIS import Agent, Ability
from auctioneerBIS import *
from supportBIS import monitor
from taskBIS import *


if __name__ == '__main__':
    contract_time = 40
    min_progress = 0

    ##### TASKS ####

    task1 = CookTask(task_id="c" + str(1),
                     name="amatriciana",
                     length=200,
                     difficulty=5,
                     color="green",
                     write_on_terminal=True)


    tasks = [task1]
    details = False

    #### AGENTS #####

    agent1 = Agent(agent_id=1,
                   name="Main-Chef",
                   topic=Topic.COOK,
                   details=details,
                   contract_time=contract_time,
                   ability=Ability(speed=70, stars=3, energy=100),
                   write_terminal=True)

    agent2 = Agent(agent_id=2,
                   name="Sub-Chef",
                   topic=Topic.COOK,
                   details=details,
                   contract_time=contract_time,
                   ability=Ability(speed=70, stars=3, energy=100),
                   write_terminal=True)

    agent3 = Agent(agent_id=3,
                   name="Sub-Chef",
                   topic=Topic.COOK,
                   details=details,
                   contract_time=contract_time,
                   ability=Ability(speed=60, stars=3, energy=100),
                   write_terminal=True)

    agent4 = Agent(agent_id=4,
                   name="Sub-Chef",
                   topic=Topic.COOK,
                   details=details,
                   contract_time=contract_time,
                   ability=Ability(speed=75, stars=3, energy=100),
                   write_terminal=True)

    agent7 = Agent(agent_id=7,
                   name="Waiter George",
                   topic=Topic.DISH_OUT,
                   details=details,
                   contract_time=contract_time,
                   ability=Ability(speed=80, cleverness=3, energy=100),
                   write_terminal=True)

    agent8 = Agent(agent_id=8,
                   name="Waiter Mike",
                   topic=Topic.DISH_OUT,
                   details=details,
                   contract_time=contract_time,
                   ability=Ability(speed=90, cleverness=3, energy=100),
                   write_terminal=True)

    agent9 = Agent(agent_id=9,
                   name="Waiter George",
                   topic=Topic.DISH_OUT,
                   details=details,
                   contract_time=contract_time,
                   ability=Ability(speed=40, cleverness=80, energy=100),
                   write_terminal=True)

    agent10 = Agent(agent_id=10,
                    name="Waiter Mike",
                    topic=Topic.DISH_OUT,
                    details=details,
                    contract_time=contract_time,
                   ability=Ability(speed=20, cleverness=20, energy=100),
                    write_terminal=True)

    agent11 = Agent(agent_id=11,
                    name="Cashier Melania",
                    topic=Topic.HANDLE_PAYMENTS,
                    details=details,
                    contract_time=contract_time,
                    ability=Ability(speed=50, cleverness=50, energy=100),
                    write_terminal=True)

    agent12 = Agent(agent_id=12,
                    name="Cashier John",
                    topic=Topic.HANDLE_PAYMENTS,
                    details=details,
                    contract_time=contract_time,
                    ability=Ability(speed=70, cleverness=60, energy=100),
                    write_terminal=True)

    ##### AUCTIONEERS #####

    for t in tasks:
        auct = generate_auctioneer(contract_time=contract_time,
                                   min_progress=min_progress,
                                   write_on_terminal=True,
                                   details=details)
        auct.trigger_task(t)
        monitor([agent1, agent3, agent2])
        time.sleep(5)

    while True:
        monitor([agent1, agent3, agent2])
        time.sleep(6)