import random
from threading import Thread

import json_reader
import utils.logger as logger
from entities.machine import BeverageMachine
from entities.maker import BeverageMaker
from utils.hash_utils import deep_get


def main():
    data = json_reader.read_file('input/data.json')
    outlet_count = int(deep_get(data, "machine", "outlets", "count_n"))
    beverages = deep_get(data, "machine", "beverages") or {}
    initial_refill = deep_get(data, "machine", "total_items_quantity") or {}

    beverage_machine = BeverageMachine(outlet_count)
    beverage_machine.turn_on()
    beverage_machine.refill_ingredients(initial_refill)
    for beverage_name, composition in beverages.items():
        wait_time_sec = random.randint(1, 4)
        beverage_machine.configure_beverage(BeverageMaker(beverage_name, composition, wait_time_sec))

    supported_beverages = beverage_machine.get_supported_beverages()

    user_requests = supported_beverages[:]
    random.shuffle(user_requests)
    request_threads = []
    logger.info("---Started serving requests---")
    for user_request in user_requests:
        request_thread = Thread(target=beverage_machine.serve_beverage, args=(user_request,), )
        request_thread.start()
        request_threads.append(request_thread)

    for t in request_threads:
        t.join()

    beverage_machine.turn_off()
    logger.info("End of simulation")


if __name__ == '__main__':
    main()
