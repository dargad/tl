#!/usr/bin/python3

import datetime
import argparse
import os
from gtimelog.timelog import TimeWindow, format_duration_short, as_minutes
from os.path import expanduser

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


def parse_date(datestr):
    from dateutil.parser import parse
    return parse(datestr)


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


class BaseFormatter(object):
    def format_cat_separator(self):
        print()

    def format(self, entries, totals):
        self._entries = entries
        self._totals = totals

        if self._entries:
            if None in entries:
                self._categories = sorted(entries)
                self._categories.append('No category')
                # self._entries['No category'] = e
                t = totals.pop(None)
                totals['No category'] = t
            else:
                self._categories = sorted(entries)
        else:
            return None

        for cat in self._categories:
            if not self.format_category(cat):
                continue

            work = [(entry, duration)
                    for start, entry, duration in self._entries[cat]]
            work.sort()
            for (entry, duration), has_more in lookahead(work):
                if not duration:
                    continue  # skip empty "arrival" entries

                self.format_entry(entry, duration, has_more)

            self.format_cat_separator()


class PrettyFormatter(BaseFormatter):
    BRANCH = '├──'
    BRANCH_LAST = '└──'

    def __init__(self, show_time=True, show_minutes=False):
        self._show_time = show_time
        self._show_minutes = show_minutes

    def format_category(self, cat):
        print('%s:' % cat.strip())
        return True

    def format_entry(self, entry, duration, has_more):
        if self._show_time:
            if self._show_minutes:
                print(u"%s %-61s  %+5s %+4s" %
                    (PrettyFormatter.BRANCH if has_more else
                    PrettyFormatter.BRANCH_LAST,
                    entry, format_duration_short(duration),
                    as_minutes(duration)))
            else:
                print(u"%s %-61s  %+5s" %
                      (PrettyFormatter.BRANCH if has_more else
                       PrettyFormatter.BRANCH_LAST,
                       entry, format_duration_short(duration)))
        else:
            print(u"%s %-61s  %+5s" %
                  (PrettyFormatter.BRANCH if has_more else
                   PrettyFormatter.BRANCH_LAST,
                   entry, format_duration_short(duration)))


class EmailFormatter(BaseFormatter):
    def format_category(self, cat):
        mapping = {'L3 / L3 support ' : '# Cases',
                'Launchpad & Public ' : '# LP',
                'Meetings ' : '# Meetings',
                'SEG related activities ' : '# Other'
                }
        if cat in mapping:
            header = mapping[cat]
            print("%s" % header)
            return True
        return False

    def format_entry(self, entry, duration, has_more):
        print("%s" % entry)


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
    parser.add_argument('-f', '--from-date',
                        help='Select the start date of the period to display')
    parser.add_argument('-t', '--to-date',
                        help='Select the end date of the period to display')
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
    if args.from_date:
        week_first = parse_date(args.from_date)
    if args.to_date:
        week_last = parse_date(args.to_date)
    if week_first > week_last:
        print("Starting date should be less than the ending date.")
        parser.print_usage()
        raise SystemExit

    log_entries = TimeWindow(LogFile, week_first, week_last, virtual_midnight)
    total_work, _ = log_entries.totals()
    entries, totals = log_entries.categorized_work_entries()

    formatter = None

    if args.format_email:
        formatter = EmailFormatter()
    else:
        formatter = PrettyFormatter(not args.no_time, args.minutes)

    print("[ACTIVITY] %s to %s (%s)" %
          (week_first.isoformat().split("T")[0],
           week_last.isoformat().split("T")[0],
           UserId))

    if formatter:
        formatter.format(entries, totals)
    print("Total work done : %s" % format_duration_short(total_work))


if __name__ == '__main__':

    main()
