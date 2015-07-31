import time


def print_completed_processes(completed_processes):
    for completed_process in completed_processes:
        print_complete(completed_process)
        print_elapsed_time(completed_process[2])


def print_complete(process_info):
    print('[Process %02d] Complete' % process_info[0])


def print_elapsed_time(start_time):
    time_to_complete = time.time() - start_time
    hours, remainder = divmod(time_to_complete, 3600)
    minutes, seconds = divmod(remainder, 60)
    print('\tTime Elapsed: %02d:%02d:%02.2f' % (int(hours), int(minutes), seconds))
