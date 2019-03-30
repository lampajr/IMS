from agent import Agent, Skill
from auctioneer import *
from task import *

# TODO: change metric computation
# TODO: setup state of the agent (think if add env or not)


if __name__ == '__main__':
    contract_time = 40
    min_progress = 0

    ##### TASKS ####

    task1 = CookTask(name="amatriciana",
                     length=200,
                     min_progress=min_progress,
                     difficulty=5,
                     color="yellow",
                     write_on_terminal=True)

    task2 = CookTask(name="carbonara",
                     length=300,
                     min_progress=min_progress,
                     difficulty=5,
                     color="blue",
                     write_on_terminal=True)

    task3 = CookTask(name="risotto",
                     length=500,
                     min_progress=min_progress,
                     difficulty=5,
                     color="cyan",
                     write_on_terminal=True)

    task4 = CookTask(name="puttanesca",
                     length=200,
                     min_progress=min_progress,
                     difficulty=5,
                     color="magenta",
                     write_on_terminal=True)

    task5 = CookTask(name="scoglio",
                     length=250,
                     min_progress=min_progress,
                     difficulty=5,
                     color="yellow",
                     write_on_terminal=True)

    tasks = [task1, task2, task3, task4, task5]

    #### AGENTS #####

    agent1 = Agent(name="Main-Chef",
                   topic=Topic.COOK,
                   contract_time=contract_time+50,
                   skill=Skill(speed=70, stars=3, energy=100))

    agent2 = Agent(name="Chef-Marco",
                   topic=Topic.COOK,
                   contract_time=contract_time+50,
                   skill=Skill(speed=70, stars=3, energy=100))

    agent3 = Agent(name="Sub-Chef-Hilary",
                   topic=Topic.COOK,
                   contract_time=contract_time+50,
                   skill=Skill(speed=60, stars=3, energy=100))

    agent4 = Agent(name="Sub-Chef-Michael",
                   topic=Topic.COOK,
                   contract_time=contract_time+50,
                   skill=Skill(speed=75, stars=3, energy=100))

    agent7 = Agent(name="Waiter-George",
                   topic=Topic.DISH_OUT,
                   contract_time=contract_time+50,
                   skill=Skill(speed=80, cleverness=3, energy=100))

    agent8 = Agent(name="Waiter-Mike",
                   topic=Topic.DISH_OUT,
                   contract_time=contract_time+50,
                   skill=Skill(speed=90, cleverness=3, energy=100))

    agent9 = Agent(name="Waiter-George",
                   topic=Topic.DISH_OUT,
                   contract_time=contract_time+50,
                   skill=Skill(speed=40, cleverness=80, energy=100))

    agent10 = Agent(name="Waiter-Mike",
                    topic=Topic.DISH_OUT,
                    contract_time=contract_time+50,
                    skill=Skill(speed=20, cleverness=20, energy=100))

    agent11 = Agent(name="Cashier-Melania",
                    topic=Topic.HANDLE_PAYMENTS,
                    contract_time=contract_time+50,
                    skill=Skill(speed=50, cleverness=50, energy=100))

    agent12 = Agent(name="Cashier-John",
                    topic=Topic.HANDLE_PAYMENTS,
                    contract_time=contract_time+50,
                    skill=Skill(speed=70, cleverness=60, energy=100))

    ##### AUCTIONEERS #####

    for t in tasks:
        auct = Auctioneer(auction_timeout=3, contract_time=contract_time)
        auct.allocate_task(t)
        time.sleep(5)
