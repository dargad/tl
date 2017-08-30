#!/usr/bin/python3

import datetime
import argparse
from os.path import expanduser
from gtimelog.timelog import TimeWindow, format_duration_short, as_minutes

branch = '├──'
branch_last = '└──'
gt_file = '%s/.local/share/gtimelog/timelog.txt' % expanduser("~")
virtual_midnight = datetime.time(2, 0)
userid = 'dgadomski'


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


def main():
    (week_first, week_last) = get_time()
    log_entries = TimeWindow(gt_file, week_first, week_last, virtual_midnight)
    total_work, _ = log_entries.totals()
    entries, totals = log_entries.categorized_work_entries()

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--no-time',
                        help='Print weekly report without spent time',
                        action='store_true')
    args = parser.parse_args()

    print("[ACTIVITY] %s to %s (%s)" %
          (week_first.isoformat().split("T")[0],
           week_last.isoformat().split("T")[0],
           userid))
    if entries:
        if None in entries:
            categories = sorted(entries)
            categories.append('No category')
            entries['No category'] = e
            t = totals.pop(None)
            totals['No category'] = t
        else:
            categories = sorted(entries)
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
                    print(u"%s %-62s%+5s %+4s" %
                          (branch if has_more else branch_last,
                           entry, format_duration_short(duration),
                           as_minutes(duration)))

            if args.no_time:
                print("")
            else:
                print('-' * 75)
                print(u"%+71s %4s" % (format_duration_short(totals[cat]),
                                      as_minutes(totals[cat])))
        print("Total work done : %s" % format_duration_short(total_work))
if __name__ == '__main__':

    main()
