import sys

from auctioneer import Auctioneer
from loader import Loader, time
from monitor import Monitor

if __name__ == '__main__':
    filename = ""
    use_clear = None
    try:
        if len(sys.argv) > 1:
            filename = sys.argv[1]
            if len(sys.argv) > 2:
                use_clear = sys.argv[2].lower() == "true"
        else:
            filename = input("Insert file's path.. ")
            use_clear = input("Use terminal clear..").lower() == "true"

        use_clear = True if use_clear is None else use_clear

        loader = Loader(filename=filename)
        Monitor(tasks=loader.tasks, agents=loader.agents, use_clear=use_clear, refresh_rate=loader.refresh_rate).start()

        for t in loader.starter_tasks:
            try:
                auct = Auctioneer(auction_timeout=loader.auction_timeout, contract_time=loader.auctioneer_contract_time)
                auct.allocate_task(t)
                time.sleep(loader.time_between_task)
            except KeyboardInterrupt:
                pass
    except FileNotFoundError:
        print("ERROR: File not found named '{}'\nTry again!".format(filename))
