import time
import os
import argparse
import json
import prometheus_client

__author__ = "Worldline DevOps Team"

valid_severities = ["INFO", "WARN", "PASS", "NOTE"]
valid_times = ["second", "minute", "hour"]
metric_labels = ['id', 'desc', 'result', 'details']

parser = argparse.ArgumentParser(description="CIS Metric Exporter Usage Guide",
                    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-f", "--json_file", required=True)
parser.add_argument("-t", "--refresh_time",
                    required=True,
                    type=int,
                    help="Refreshing time between 1 and 24 hours")
parser.add_argument("--timebase", choices=valid_times,
                    required=True,
                    help="Valid times are secondly, minutely, and hourly")
parser.add_argument("-P", "--port", default=9091, type=int,
                    help="Default listening port is 9091")
parser.add_argument("--severity", choices=valid_severities, nargs='*',
                    help="Filters metrics by single or multi severity:\n"
                         "--severity WARN\n"
                         "--severity INFO PASS")
parser.add_argument("--enable_default_collectors", action="store_true",
                    help="Activates the base system metrics")
parser.add_argument("--filter_fields", choices=metric_labels, nargs='*',
                    help="Filter labels on chosed fields to display:\n"
                        "--filter_fields id desc\n"
                        "--filter_fields id desc results")
args = parser.parse_args()

if args.filter_fields is not None and len(args.filter_fields) == 0:
    parser.error("--filter_fields cannot be set empty. Check with --help to see possible fields!")

# Disables default collector metrics if it is not enabled
if not args.enable_default_collectors:
    prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
    prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
    prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)

# Create metrics from parsed json objects
metric_results = prometheus_client.Gauge(
    'cis_benchmark_result',
    'CIS Benchmark Metrics',
    args.filter_fields if args.filter_fields else metric_labels
)

def get_metrics():
    """
    Parses object from CIS output to store them in the Prometheus Gauge
    :_metrics.clear: resets the metrics data to be sure it is always up-to-dated
    :mdata['tests']: main object of CIS json log structure
    """
    if os.path.exists(args.json_file) and os.path.getsize(args.json_file) > 0:
        try:
            with open(args.json_file, 'r') as json_file:
                mdata = json.load(json_file)
        except json.decoder.JSONDecodeError:
            raise ValueError("JSON file is not valid!")
    else:
        raise ValueError("JSON file might be empty or does not exist!")

    metric_results._metrics.clear()

    for metrics in mdata['tests']:
        for output in metrics['results']:
            details = output.get("details", "None")

            if args.filter_fields:
                metric_output = []
                for field in args.filter_fields:
                    if field in output:
                        metric_output.append(output[field]) # add only defined label(s) in args.filter_fields
                    elif field == "details":
                        metric_output.append(details) # add details label if it is defined in args.filter_fields
            else:
                # displays all fields as it is if args.filter_fields is not defined
                 metric_output = (output['id'], output['desc'], output['result'], details)

            if args.severity:
                if any(severity in output['result'] for severity in args.severity):
                    metric_results.labels(*metric_output).set(1 if output['result'] == "WARN" else 0)
            else:
                metric_results.labels(*metric_output).set(1 if output['result'] == "WARN" else 0)

if __name__ == '__main__':
    # Start an HTTP server to expose Prometheus metrics
    prometheus_client.start_http_server(args.port)
    exp_msg = f"CIS Exporter is started on {args.port} port. Refresh time: {args.refresh_time} {args.timebase}(s)"

    M = 60   # In minutes
    H = 3600 # In hours

    while True:
        get_metrics()

        if args.timebase == "second":
            if args.refresh_time >= 5:
                print(f"{exp_msg}")
                time.sleep(args.refresh_time)
            else:
                raise ValueError("It must be at least 5 seconds.")

        elif args.timebase == "minute":
            if args.refresh_time >= 1:
                print(f"{exp_msg}")
                time.sleep(M * args.refresh_time)
            else:
                raise ValueError("It must be at least 1 minute.")

        elif args.timebase == "hour":
            if 1<= args.refresh_time <= 24:
                print(f"{exp_msg}")
                time.sleep(H * args.refresh_time)
            else:
                raise ValueError("Time must be between 1-24 hour")
