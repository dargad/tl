#!/usr/bin/python3

import argparse
import datetime
import os
from gtimelog.timelog import TimeWindow, format_duration_short

virtual_midnight = datetime.time(2, 0)


def set_logfile(argfile=None):
    if argfile is not None:
        return argfile[0]
    else:
        env = os.environ.get("GTIMELOG_FILE")
        if env is not None:
            return env
    return '%s/.local/share/gtimelog/timelog.txt' % os.path.expanduser("~")


def get_time():
    today = datetime.datetime.today()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    week_first = today - datetime.timedelta(days=today.weekday())
    week_last = week_first + datetime.timedelta(days=6)
    week_last = week_last.replace(hour=23, minute=59, second=59)
    return (week_first, week_last)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--logfile', nargs=1, metavar='LOGFILE',
                        help='Path to the gtimelog logfile to be use')
    args = parser.parse_args()

    if args.logfile is not None:
        LogFile = set_logfile(args.logfile)
    else:
        LogFile = set_logfile()

    (week_first, week_last) = get_time()
    log_entries = TimeWindow(LogFile, week_first, week_last, virtual_midnight)
    total_work, _ = log_entries.totals()
    _, totals = log_entries.categorized_work_entries()

    ordered_by_time = [(time, cat) for cat, time in totals.items()]
    ordered_by_time.sort(reverse=True)
    max_cat_length = max([len(cat) for cat in totals.keys()])
    line_format = '  %-' + str(max_cat_length + 4) + 's %+5s\t %.0f%%'
    print("\nTotal work done so far : %s\n" %
          format_duration_short(total_work))
    print('Categories by time spent:')
    for time, cat in ordered_by_time:
        print(line_format % (cat, format_duration_short(time),
                             time / total_work * 100))


if __name__ == '__main__':

    main()
