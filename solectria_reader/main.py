import time

import comms
import emitter
import metrics

def main():
    carbon_emitter = emitter.CarbonEmitter()
    with comms.Connection() as connection:
        while True:
            next_time = time.time() + 1

            for each_metric in metrics.all_metrics:
                try:
                    value = each_metric.fetch(connection)
                except Exception, e:
                    print >> sys.stderr, each_metric.name, e
                    continue
                carbon_emitter.emit(each_metric, value)
                print each_metric.name, value, each_metric.unit

            print ''
            to_sleep = max(0, next_time - time.time())
            time.sleep(to_sleep)

if __name__ == '__main__':
    main()
