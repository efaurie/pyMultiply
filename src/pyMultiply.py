import argparse
import subprocess

from file_fns import *
from Queue import Queue
from output_fns import *

POLLING_TIME = 0.1
DEVNULL = open(os.devnull, 'w')


def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('-script', help='The python script to execute on files')
    parser.add_argument('-source', help='The source directory - which files to execute on')
    parser.add_argument('-max_depth', type=int, default=0, help='The maximum number of directories it will traverse from source')
    parser.add_argument('-max_processes', type=int, default=5, help='The maximum number of processes to spawn simultaneously')
    return parser.parse_args()


def get_file_list(source, max_depth):
    if not is_file_or_directory(source):
        return list()
    else:
        return get_file_list_from_source(source, max_depth)


def construct_commands(script, file_list):
    commands = Queue()

    for file_path in file_list:
        commands.put('python {0} {1}'.format(script, file_path))

    return commands


def execute(commands, max_processes):
    process_id = 1
    processes = set()
    while not commands.empty():
        if len(processes) >= max_processes:
            processes = check_completed(processes)
        else:
            processes.add(launch_process(commands.get(), process_id))
            process_id += 1

    while len(processes) > 0:
        time.sleep(POLLING_TIME)
        completed_processes = [process for process in processes if process[3].poll() is not None]
        print_completed_processes(completed_processes)
        processes.difference_update(completed_processes)


def check_completed(processes):
    time.sleep(POLLING_TIME)
    completed_processes = [process for process in processes if process[3].poll() is not None]
    print_completed_processes(completed_processes)
    processes.difference_update(completed_processes)
    return processes


def launch_process(command, process_id):
    print '[Process %02d] Starting: %s' % (process_id, command)
    process_info = (process_id, command, time.time(), subprocess.Popen(command, stdout=DEVNULL, shell=True))
    return process_info


if __name__ == '__main__':
    arguments = init()
    file_list = get_file_list(arguments.source, arguments.max_depth)
    commands_to_execute = construct_commands(arguments.script, file_list)
    start_time = time.time()
    execute(commands_to_execute, arguments.max_processes)
    print '\n[+] All Processes Completed'
    print_elapsed_time(start_time)
