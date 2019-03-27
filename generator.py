from agent import Agent
from auctioneer import Auctioneer
from task import *
import random


MAX_N = 500

agents = []
tasks = []


def trigger_task():
    print("TRIGGER NEW TASK:")
    name = input("Insert task name.. ")
    length = input("Insert task length..")
    color = input("Insert color..")
    topic = None
    while topic != "a" and topic != "b" and topic != "c":
        print("Which is the topic of the task?")
        print("a) --> Cook topic")
        print("b) --> Handle payments")
        print("c) --> Dish out")
        topic = input()

    if topic == "a":
        task = CookTask(task_id="t" + str(random.randint(0, MAX_N)),
                        name=name,
                        length=int(length),
                        difficulty=5,
                        color=color)
    elif topic == "b":
        task = None
    else:
        task = DishOutTask(task_id=str(random.randint(0, MAX_N)),
                           name=name,
                           length=int(length),
                           difficulty=5,
                           color=color)

    tasks.append(task)
    auctioneer = generate_auctioneer()
    auctioneer.trigger_task(task=task)


def generate_auctioneer():
    max_elapsed_bids_time, contract_time, min_progress = 5, 10, 30

    return Auctioneer(auction_id="auct" + str(random.randint(0, MAX_N)),
                      max_elapsed_bids_time=int(max_elapsed_bids_time),
                      contract_time=int(contract_time),
                      min_progress=int(min_progress))


def insert_agent():
    print("INSERT NEW AGENT:")
    name = input("Insert agent name.. ")
    topic = None
    while topic != "a" and topic != "b" and topic != "c":
        print("Which is the topic on which it will be listening?")
        print("a) --> Cook topic")
        print("b) --> Handle payments")
        print("c) --> Dish out")
        topic = input()

    if topic == "a":
        topic = Topic.COOK
    elif topic == "b":
        topic = Topic.HANDLE_PAYMENTS
    else:
        topic = Topic.DISH_OUT

    # contract time and min_progress are now manually inserted

    contract_time = input("Insert contract time..")
    min_progress = input("Insert minimum progress allowed..")

    agents.append(Agent(agent_id="ag" + str(random.randint(0, MAX_N)),
                        name=name,
                        topic=topic,
                        contract_time=int(contract_time),
                        min_progress=int(min_progress)))
    print("New agent correctly inserted in the environment!")


def invalidate_agent():
    pos = int(input("Insert position of agent to invalidate.."))

    if pos < 0 or pos > len(agents):
        return

    agents[pos].invalidate()


def restore_agent():
    pos = int(input("Insert position of agent to restore.."))

    if pos < 0 or pos > len(agents):
        return

    agents[pos].restore()

if __name__ == '__main__':
    cmd = None

    try:
        while cmd != "0":
            print("What do you want to do?")
            print("1) --> Insert new agent")
            print("2) --> Trigger a new task")
            print("3) --> Invalidate agent")
            print("4) --> Restore agent")
            print("h) --> Repeat menu")
            print("0) --> exit")

            cmd = input()
            print(cmd)
            if cmd == "1":
                insert_agent()
            elif cmd == "2":
                trigger_task()
            elif cmd == "3":
                invalidate_agent()
            elif cmd == "4":
                restore_agent()
            elif cmd == "h":
                continue

    except KeyboardInterrupt:
        exit(0)
