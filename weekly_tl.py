#!/usr/bin/python3

import datetime
import argparse
import os
from gtimelog.timelog import TimeWindow, format_duration_short, as_minutes
from os.path import expanduser

branch = '├──'
branch_last = '└──'
gt_file = '%s/.local/share/gtimelog/timelog.txt' % expanduser("~")
virtual_midnight = datetime.time(2, 0)


def set_logfile(argfile=None):
    if argfile is not None:
        return argfile[0]
    else:
        env = os.environ.get("GTIMELOG_FILE")
        if env is not None:
            return env
    return '%s/.local/share/gtimelog/timelog.txt' % os.path.expanduser("~")


def set_userid(user=None):
    if user is not None:
        return user[0]
    else:
        env = os.environ.get("GTIMELOG_USER")
        if env is not None:
            return env
    return '<replace by your user identification>'


def get_time():
    today = datetime.datetime.today()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    week_first = today - datetime.timedelta(days=today.weekday())
    week_last = week_first + datetime.timedelta(days=4)
    week_last = week_last.replace(hour=23, minute=59, second=59)
    return (week_first, week_last)


def lookahead(iterable):
    """Pass through all values from the given iterable, augmented by the
    information if there are more values to come after the current one
    (True), or if it is the last value (False).
    """
    # Get an iterator and pull the first value.
    it = iter(iterable)
    last = next(it)
    # Run the iterator to exhaustion (starting from the second value).
    for val in it:
        # Report the *previous* value (more to come).
        yield last, True
        last = val
    # Report the last value.
    yield last, False


def format_email(entries, categories):
    mapping = {'L3 / L3 support ' : '# Cases',
               'Launchpad & Public ' : '# LP',
               'Meetings ' : '# Meetings',
               'SEG related activities ' : '# Other'
               }

    print()
    for cat in categories:
        if cat in mapping:
            header = mapping[cat]
        else:
            continue
        print("%s" % header)
        work = [(entry, duration)
                for start, entry, duration in entries[cat]]
        work.sort()
        for (entry, duration), has_more in lookahead(work):
            print("%s" % entry)
        print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--logfile', nargs=1, metavar='LOGFILE',
                        help='Path to the gtimelog logfile to be use')
    parser.add_argument('-u', '--user', nargs=1, metavar='USER',
                        help='User Identification to be used for report')
    parser.add_argument('-n', '--no-time',
                        help='Print weekly report without spent time',
                        action='store_true')
    parser.add_argument('-m', '--minutes',
                        help='Print weekly report with spent time in minutes',
                        action='store_true')
    parser.add_argument('-e', '--format-email',
                        help='Format a status report e-mail',
                        action='store_true')
    args = parser.parse_args()

    if args.logfile is not None:
        LogFile = set_logfile(args.logfile)
    else:
        LogFile = set_logfile()

    if args.user is not None:
        UserId = set_userid(args.user)
    else:
        UserId = set_userid()

    (week_first, week_last) = get_time()
    log_entries = TimeWindow(LogFile, week_first, week_last, virtual_midnight)
    total_work, _ = log_entries.totals()
    entries, totals = log_entries.categorized_work_entries()

    print("[ACTIVITY] %s to %s (%s)" %
          (week_first.isoformat().split("T")[0],
           week_last.isoformat().split("T")[0],
           UserId))
    if entries:
        if None in entries:
            categories = sorted(entries)
            categories.append('No category')
            entries['No category'] = e
            t = totals.pop(None)
            totals['No category'] = t
        else:
            categories = sorted(entries)

        if args.format_email:
            format_email(entries, categories)
        else:

            for cat in categories:
                print('%s:' % cat.strip())

                work = [(entry, duration)
                        for start, entry, duration in entries[cat]]
                work.sort()
                for (entry, duration), has_more in lookahead(work):
                    if not duration:
                        continue  # skip empty "arrival" entries

                    entry = entry[:1].upper() + entry[1:]
                    if args.no_time:
                        print(u"%s" % entry)
                    else:
                        if args.minutes:
                            print(u"%s %-61s  %+5s %+4s" %
                                    (branch if has_more else branch_last,
                                    entry, format_duration_short(duration),
                                    as_minutes(duration)))
                        else:
                            print(u"%s %-61s  %+5s" %
                                (branch if has_more else branch_last,
                                entry, format_duration_short(duration)))

                if args.no_time:
                    print("")
                else:
                    if args.minutes:
                        print('-' * 75)
                        print(u"%+72s %4s" % (format_duration_short(totals[cat]),
                                            as_minutes(totals[cat])))
                    else:
                        print('-' * 70)
                        print(u"%+72s" % (format_duration_short(totals[cat])))
            print("Total work done : %s" % format_duration_short(total_work))


if __name__ == '__main__':

    main()
