import re
import sys
import os 
import datetime
import json 
import time 

def ping(host):
    import subprocess, platform

    cmd = "ping -c 2 -W 1 %s" % (host)

    # Ping
    try:
        output = subprocess.check_output(cmd, shell=True)
        return output
    except:
        return None

def main():
    ping_host = os.environ['PING_HOST']
    output = ping(ping_host)
    metrics = {}
    ts = datetime.datetime.utcnow()
    ts = "%sZ" % (ts.isoformat())
    metrics['@timestamp'] = ts 
    metrics['doctype'] = 'ping-metrics'
    metrics['ping_host'] = ping_host

    if output:
        ping_stats = re.search('^(.*?) packets transmitted, (.*?) packets received, (.*?)% packet loss$', output, re.I|re.M)
        round_trip_metrics = re.search('^.*? min\/avg\/max\/stddev = (.*?)\/(.*?)\/(.*?)/(.*?) (.*?)$', output, re.I|re.M)

        if ping_stats:
            packets_transmitted, packets_received, packet_loss = ping_stats.groups()[0:]

        if round_trip_metrics:
            min, avg, max, stddev, time_metric = round_trip_metrics.groups()[0:]

        metrics['route_to_host'] = 'yes'
        metrics['min_ping_time'] = float(min)
        metrics['max_ping_time'] = float(max) 
        metrics['stddev_ping_time'] = float(stddev)
        metrics['time_metric'] = time_metric
        metrics['avg_ping_time'] = float(avg)
        metrics['packet_loss'] = float(packet_loss)
        metrics['host_up'] = 'yes'
    else:
        metrics['route_to_host'] = 'no'
        metrics['avg_ping_time'] = 0
        metrics['host_up'] = 'no'
        metrics['packet_loss'] = 100


    sys.stdout.write("%s\n" % json.dumps(metrics))

if __name__ == "__main__":
    while True:
        main()
        time.sleep(5)