import sys

from auctioneer import Auctioneer
from loader import Loader, time
from monitor import Monitor

if __name__ == '__main__':
    filename = ""
    try:
        if len(sys.argv) > 1:
            filename = sys.argv[1]
        else:
            filename = input("Insert file's path .. ")

        loader = Loader(filename=filename)
        Monitor(tasks=loader.tasks, agents=loader.agents, clear=True, refresh_rate=loader.refresh_rate).start()

        for t in loader.starter_tasks:
            try:
                auct = Auctioneer(auction_timeout=loader.auction_timeout, contract_time=loader.auctioneer_contract_time)
                auct.allocate_task(t)
                time.sleep(loader.time_between_task)
            except KeyboardInterrupt:
                pass
    except FileNotFoundError:
        print("ERROR: File not found named '{}'\nTry again!".format(filename))
