"""PMeter a tool to measure the TCP/UDP network conditions that the running host experiences

Usage:
  pmeter_cli.py measure <INTERFACE> [-K=KER_BOOL -N=NET_BOOL -F=FILE_NAME -S=STD_OUT_BOOL --interval=INTERVAL --measure=MEASUREMENTS --length=LENGTH --user=USER --file_name=FILENAME --folder_path=FOLDERPATH --folder_name=FOLDERNAME]

Commands:
    measure     The command to start measuring the computers network activity on the specified network devices. This command accepts a list of interfaces that you wish to monitor

Options:
  -h --help                Show this screen
  --version                Show version
  -N --measure_network     Set if we monitor only the network interface [default: True]
  -K --measure_kernel      Set if we monitor only the kernel [default: True]
  -U --measure_udp         Set UDP monitoring only [default: True]
  -T --measure_tcp         Set TCP monitoring only [default: True]
  -S --enable_std_out      Disable printing the results to standard output [default: False]
  --file_name=FILENAME     Set the file name used to measure [default: pmeter_measure.txt]
  --folder_path=FOLDERPATH Set the path to store the measurement files in the default is the users home directory under ~/.pmeter/
  --folder_name=FOLDERNAME Set the folder name for pmeter to dump data into [default: .pmeter]
  --interval=INTERVAL      Set the time to run the measurement in the format HH:MM:SS [default: 00:00:01]
  --measure=MEASUREMENTS   The max number of times to measure your system. Set this value to 0 to ignore this and use only the length [default: 1]
  --length=LENGTH          The amount of time to run for: 5w, 4d 3h, 2m, 1s are some examples of 5 weeks, 4 days, 3 hours, 2 min, 1 sec. Set this value to '-1s' to ignore this field and use only measurement [default: 10s]
  --user=USER              This will override the user we try to pick up from the environment variable(ODS_USER). If no user is passed then we will not submit the data generated to the ODS backend [default: ]

"""

from docopt import docopt
import constants
from datetime import datetime, timedelta
from file_writer import ODS_Metrics
import time
import copy

old_measure_dict = {}  # this is hackish but the keyis the interface name and for every metric we run of that interface name we replace and then run


def convert_to_endate(length):
    end_date = datetime.now()
    num = int(length[:-1])
    if "s" in length:
        end_date += timedelta(seconds=num)
    if "m" in length:
        end_date += timedelta(minutes=num)
    if "d" in length:
        end_date += timedelta(days=num)
    if "w" in length:
        end_date += timedelta(weeks=num)
    if "h" in length:
        end_date += timedelta(hours=num)
    return end_date


# run measurement using time only
def measure_using_length(interface_list, metric, folder_path, file_name, folder_name, measure_tcp=True,
                         measure_udp=True, measure_kernel=True, measure_network=True, print_to_std_out=False,
                         latency_host="http://google.com", interval=1, length="0s"):
    end_date = convert_to_endate(length)
    current_date = datetime.now()
    while (current_date < end_date):
        print("Current date is less than end date=", current_date < end_date)
        metric.measure_latency_rtt(latency_host)
        for intr_name in interface_list:
            metric.measure(intr_name, measure_tcp, measure_udp, measure_kernel, measure_network, print_to_std_out,
                           latency_host)
            if intr_name in old_measure_dict:
                metric.do_deltas(old_measure_dict[intr_name])
            old_measure_dict[intr_name] = copy.deepcopy(metric)
            metric.to_file(file_name=file_name, folder_path=folder_path, folder_name=folder_name)
        current_date = datetime.now()
        time.sleep(interval)


def measure_using_measurements(interface_list, metric, folder_path, file_name, folder_name, measure_tcp=True,
                               measure_udp=True, measure_kernel=True, measure_network=True, print_to_std_out=False,
                               latency_host="http://google.com", interval=1, measurement=1):
    for i in range(0, measurement):
        metric.measure_latency_rtt(latency_host)
        print("measurement: ", i)
        for intr_name in interface_list:
            metric.measure(intr_name, measure_tcp, measure_udp, measure_kernel, measure_network, print_to_std_out,
                           latency_host)
            if intr_name in old_measure_dict:
                metric.do_deltas(old_measure_dict[intr_name])
            old_measure_dict[intr_name] = copy.deepcopy(metric)
            metric.to_file(file_name=file_name, folder_path=folder_path, folder_name=folder_name)
        time.sleep(interval)


def begin_measuring(user, folder_path, file_name, folder_name, interface='', measure_tcp=True, measure_udp=True,
                    measure_kernel=True, measure_network=True, print_to_std_out=False, interval=1,
                    latency_host="http://google.com", measurement=1, length="0s"):
    metric = ODS_Metrics()
    metric.set_user(user)
    interface_list = []
    if interface == "all":
        for inter_name in metric.get_system_interfaces():
            interface_list.append(inter_name)
    else:
        interface_list.append(interface)
    if measurement == 0:
        print("Measuring by using the duration specified with interval")
        measure_using_length(interface_list=interface_list, metric=metric, folder_path=folder_path, file_name=file_name,
                             folder_name=folder_name, measure_tcp=measure_tcp, measure_udp=measure_udp,
                             measure_kernel=measure_kernel, measure_network=measure_network,
                             print_to_std_out=print_to_std_out, latency_host=latency_host, interval=interval,
                             length=length)
    if length == '0':
        print("Measuring by using the number of measurments to perform with interval")
        measure_using_measurements(interface_list=interface_list, metric=metric, folder_path=folder_path,
                                   file_name=file_name, folder_name=folder_name, measure_tcp=measure_tcp,
                                   measure_udp=measure_udp, measure_kernel=measure_kernel,
                                   measure_network=measure_network, print_to_std_out=print_to_std_out,
                                   latency_host=latency_host, interval=interval, measurement=measurement)
    else:
        measurements_counter = 0
        end_date = convert_to_endate(length)
        current_date = datetime.now()
        while current_date < end_date and measurements_counter < measurement:
            print("Current date= ", str(current_date), "is less than end date=", str(end_date), " is =",
                  current_date < end_date)
            print("currentMeasurement is less than the max measurements", measurements_counter < measurement)
            for intr_name in interface_list:
                metric.measure(intr_name, measure_tcp, measure_udp, measure_kernel, measure_network, print_to_std_out,
                               latency_host)
                if intr_name in old_measure_dict:
                    metric.do_deltas(old_measure_dict[intr_name])
                old_measure_dict[intr_name] = copy.deepcopy(metric)
                metric.to_file(file_name=file_name, folder_path=folder_path, folder_name=folder_name)
            current_date = datetime.now()
            measurements_counter += 1
            time.sleep(interval)

def main():
    arguments = docopt(__doc__, version='PMeter 1.0')
    if arguments['measure']:
        interface = arguments['<INTERFACE>']
        file_name = arguments['--file_name']
        folder_path = arguments['--folder_path']
        folder_name = arguments['--folder_name']
        network_only = arguments['--measure_network']
        kernel_only = arguments['--measure_kernel']
        udp_only = arguments['--measure_udp']
        tcp_only = arguments['--measure_tcp']
        std_out_print = arguments['--enable_std_out']
        interval = arguments['--interval']
        pause_between_measure = constants.get_sec(interval)
        times_to_measure = arguments['--measure']
        lengthOfExperiment = arguments['--length']
        user = arguments['--user']
        if folder_name is None: folder_name = ".pmeter"
        print("Parameters recieved: \n", "interface=", interface, "measure network=", network_only, "measure kernel=",
              kernel_only, "interval between measurements=", pause_between_measure, "times to measure default is 1=",
              times_to_measure, 'file_name=', file_name, 'folder_name=', folder_name, 'folder_path=', folder_path)
        begin_measuring(folder_path=folder_path, folder_name=folder_name, file_name=file_name, user=user,
                        interface=interface, measure_tcp=tcp_only, measure_kernel=kernel_only,
                        measure_network=network_only, measure_udp=udp_only, print_to_std_out=std_out_print,
                        interval=pause_between_measure, length=lengthOfExperiment, measurement=int(times_to_measure))
        print("Done Measuring")


if __name__ == '__main__':
    main()