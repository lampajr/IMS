from agent import Agent, Skill
from auctioneer import *
from monitor import Monitor
from task import *
from utility import *

# TODO: change metric computation
# TODO: setup state of the agent (think if add env or not)


if __name__ == '__main__':
    contract_time = 5
    min_progress = 40

    ##### TASKS ####
    tasks = []

    task1_2 = DishOutTask(name="dish-out-amatriciana",
                          length=200,
                          min_progress=min_progress,
                          difficulty=5,
                          color="yellow",
                          write_on_terminal=True,
                          description="dish out pasta all'amatriciana")

    task1 = CookTask(name="amatriciana",
                     length=200,
                     min_progress=min_progress,
                     difficulty=5,
                     color="yellow",
                     write_on_terminal=True,
                     description="cooking amatriciana",
                     subtask=task1_2)
    tasks.append(task1)

    task2 = CookTask(name="carbonara",
                     length=300,
                     min_progress=min_progress,
                     difficulty=5,
                     color="blue",
                     write_on_terminal=True,
                     description="cooking carbonara with guanciale")

    tasks.append(task2)

    task3 = CookTask(name="risotto",
                     length=500,
                     min_progress=min_progress,
                     difficulty=5,
                     color="cyan",
                     write_on_terminal=True,
                     description="cooking risotto with zafferano")

    tasks.append(task3)

    task4 = CookTask(name="puttanesca",
                     length=200,
                     min_progress=min_progress,
                     difficulty=5,
                     color="magenta",
                     write_on_terminal=True,
                     description="cooking puttanesca")

    tasks.append(task4)

    task5 = CookTask(name="scoglio",
                     length=250,
                     min_progress=min_progress,
                     difficulty=5,
                     color="yellow",
                     write_on_terminal=True,
                     description="cooking pasta allo scoglio")

    tasks.append(task5)

    tasks.append(task1_2)

    #### AGENTS #####

    agent1 = Agent(name="Main-Chef",
                   topic=Topic.COOK,
                   contract_time=contract_time,
                   skill=Skill(speed=70, stars=3, energy=100))

    agent2 = Agent(name="Chef-Marco",
                   topic=Topic.COOK,
                   contract_time=contract_time,
                   skill=Skill(speed=70, stars=3, energy=100))

    agent3 = Agent(name="Sub-Chef-Hilary",
                   topic=Topic.COOK,
                   contract_time=contract_time,
                   skill=Skill(speed=60, stars=3, energy=100))

    agent4 = Agent(name="Sub-Chef-Michael",
                   topic=Topic.COOK,
                   contract_time=contract_time,
                   skill=Skill(speed=75, stars=3, energy=100))

    agent7 = Agent(name="Waiter-George",
                   topic=Topic.DISH_OUT,
                   contract_time=contract_time,
                   skill=Skill(speed=80, cleverness=3, energy=100))

    agent8 = Agent(name="Waiter-Mike",
                   topic=Topic.DISH_OUT,
                   contract_time=contract_time,
                   skill=Skill(speed=90, cleverness=3, energy=100))

    agent9 = Agent(name="Waiter-George",
                   topic=Topic.DISH_OUT,
                   contract_time=contract_time,
                   skill=Skill(speed=40, cleverness=80, energy=100))

    agent10 = Agent(name="Waiter-Mike",
                    topic=Topic.DISH_OUT,
                    contract_time=contract_time,
                    skill=Skill(speed=20, cleverness=20, energy=100))

    agent11 = Agent(name="Cashier-Melania",
                    topic=Topic.HANDLE_PAYMENTS,
                    contract_time=contract_time,
                    skill=Skill(speed=50, cleverness=50, energy=100))

    agent12 = Agent(name="Cashier-John",
                    topic=Topic.HANDLE_PAYMENTS,
                    contract_time=contract_time,
                    skill=Skill(speed=70, cleverness=60, energy=100))

    agents = [agent1, agent2, agent3, agent4, agent7, agent8, agent9, agent10, agent11, agent12]

    ##### AUCTIONEERS #####

    Monitor(tasks=tasks, agents=agents, refresh_rate=1).start()

    for t in tasks:
        try:
            auct = Auctioneer(auction_timeout=3, contract_time=contract_time)
            auct.allocate_task(t)
            time.sleep(5)
        except KeyboardInterrupt:
            pass
