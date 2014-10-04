import time

import comms
import metrics

def main():
    with comms.Connection() as connection:
        while True:
            start_time = time.time()
            next_time = start_time + 1

            for each_metric in metrics.all_metrics:
                value = each_metric.fetch(connection)
                print each_metric.name, value

            to_sleep = max(0, next_time - time.time())
            time.sleep(to_sleep)

if __name__ == '__main__':
    main()
