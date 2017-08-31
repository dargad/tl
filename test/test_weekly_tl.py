import unittest
import sys
import tempfile
import os
import re
import shutil
import datetime
import argparse
from mock import patch
import weekly_tl


class WeeklyTlTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.args = argparse.Namespace()
        self.args.logfile = None
        self.args.no_time = None
        self.args.user = None
        self.args.minutes = True
        self.regex = re.compile(r'SF7-openafs.*1:10\n')
        self.regex_with_minutes = re.compile(r'SF7-openafs.*1:10.*70\n')
        self.regex_notime = re.compile(r'SF7-openafs * \n')
        self.regex_defuser = re.compile(r'replace by your user identification')
        self.workdir = tempfile.mkdtemp()
        self.LogFile = os.path.join(self.workdir, 'timelog.txt')
        self.back = datetime.datetime.today()
        self.back = self.back.replace(year=2015, month=3, day=16, hour=0,
                                      minute=0, second=0, microsecond=0)
        self.week_first = (self.back -
                           datetime.timedelta(days=self.back.weekday()))
        self.week_last = self.week_first + datetime.timedelta(days=6)
        self.week_last = self.week_last.replace(hour=23, minute=59, second=59)
        # Prepare timelog file with existing tasks
        with open(self.LogFile, 'w') as timelog:
            timelog.write("2015-03-13 13:21: lunch** :\n")
            timelog.write("2015-03-13 16:34: Launchpad & Public :  lp1415880\n"
                          )
            timelog.write("2015-03-13 17:45: L3 / L3 support :  SF7-openafs\n")
            timelog.write("2015-03-16 08:41: arrived\n")
            timelog.write("2015-03-16 09:57: Personal management :  email\n")
            timelog.write("2015-03-16 11:07: L3 / L3 support :  SF7-openafs\n")
            timelog.write("2015-03-16 11:11: L3 / L3 support :  SF801-kdump\n")
            timelog.write(("2015-03-17 11:01: Mentoring / Edu / Training :  "
                          "python\n"))
            timelog.write(("2015-03-17 11:02: Mentoring / Edu / Training :  "
                          "ruby\n"))
            timelog.write("2015-03-17 11:03: Mentoring / Edu / Training :  c\n"
                          )
            timelog.write(("2015-03-17 11:04: Mentoring / Edu / Training :  "
                          "apl\n"))
            timelog.write(("2015-03-17 11:05: Mentoring / Edu / Training :  "
                          "perl\n"))
            timelog.write(("2015-03-17 11:06: Mentoring / Edu / Training :  "
                           "go\n"))
            timelog.write(("2015-03-17 11:07: Mentoring / Edu / Training :  "
                           "java\n"))
            timelog.write(("2015-03-17 11:08: Mentoring / Edu / Training :  "
                           "nodejs\n"))
            timelog.write(("2015-03-17 11:09: Mentoring / Edu / Training :  "
                           "erlang\n"))
            timelog.write(("2015-03-17 11:10: Mentoring / Edu / Training :  "
                           "basic\n"))
            timelog.write(("2015-03-17 11:11: Mentoring / Edu / Training :  "
                           "pascal\n"))
            timelog.write("2015-03-18 11:10: Meetings : maas\n")
            timelog.write("2015-03-18 11:11: Meetings : juju\n")
            timelog.write("2015-03-18 11:12: Meetings : supp\n")
            timelog.write("2015-03-18 11:13: Meetings : team\n")
            timelog.write("2015-03-18 11:14: Meetings : mgr\n")
            timelog.write("2015-03-18 11:15: Meetings : foundation\n")
            timelog.write("2015-03-18 11:16: Meetings : server\n")
            timelog.write("2015-03-18 11:17: Meetings : sabdfl\n")
            timelog.write("2015-03-18 11:18: Meetings : kernel\n")
            timelog.write("2015-03-18 11:19: Meetings : mom\n")
            timelog.write("2015-03-19 11:10: Launchpad & Public : maas\n")
            timelog.write("2015-03-19 11:11: Launchpad & Public : juju\n")
            timelog.write("2015-03-19 11:12: Launchpad & Public : supp\n")
            timelog.write("2015-03-19 11:13: Launchpad & Public : team\n")
            timelog.write("2015-03-19 11:14: Launchpad & Public : mgr\n")
            timelog.write("2015-03-19 11:15: Launchpad & Public : foundation\n"
                          )
            timelog.write("2015-03-19 11:16: Launchpad & Public : server\n")
            timelog.write("2015-03-19 11:17: Launchpad & Public : sabdfl\n")
            timelog.write("2015-03-19 11:18: Launchpad & Public : kernel\n")
            timelog.write("2015-03-19 11:19: Launchpad & Public : mom\n")
            timelog.write("2015-03-19 11:20: Launchpad & Public : rsyslog\n")
            timelog.write("2015-03-19 11:21: Launchpad & Public : sleep\n")
            timelog.write("2015-03-19 11:22: Launchpad & Public : binutils\n")
            timelog.write("2015-03-19 11:23: Launchpad & Public : awk\n")
            timelog.write("2015-03-19 11:24: Launchpad & Public : grep\n")
            timelog.write("2015-03-19 11:25: Launchpad & Public : make\n")
            timelog.write("2015-03-19 11:26: Launchpad & Public : autotools\n")
            timelog.write("2015-03-19 11:27: Launchpad & Public : autoconf\n")
            timelog.write("2015-03-19 11:28: Launchpad & Public : ifenslave\n")
            timelog.write("2015-03-19 11:29: Launchpad & Public : true\n")
            timelog.write("2015-03-19 11:30: Launchpad & Public : false\n")
            timelog.write("2015-03-19 11:31: Launchpad & Public : what\n")

    @classmethod
    def tearDownClass(self):
        shutil.rmtree(self.workdir)

    def test_weekly_tl(self):
        '''testing default'''
        self.args.minutes = False
        with patch('argparse.ArgumentParser.parse_args',
                   return_value=self.args):
            with patch('weekly_tl.get_time',
                       return_value=(self.week_first, self.week_last)):
                with patch('weekly_tl.set_logfile',
                           return_value=self.LogFile):
                    weekly_tl.main()
                    output = sys.stdout.getvalue().strip()
                    self.assertRegex(output, self.regex)
                    self.assertRegex(output, self.regex_defuser)

    def test_weekly_tl_with_minutes(self):
        '''testing with --minutes argument'''
        self.args.minutes = True
        with patch('argparse.ArgumentParser.parse_args',
                   return_value=self.args):
            with patch('weekly_tl.get_time',
                       return_value=(self.week_first, self.week_last)):
                with patch('weekly_tl.set_logfile',
                           return_value=self.LogFile):
                    weekly_tl.main()
                    output = sys.stdout.getvalue().strip()
                    self.assertRegex(output, self.regex_with_minutes)
                    self.assertRegex(output, self.regex_defuser)

    def test_weekly_tl_with_notime(self):
        '''testing weekly_tl with --notime argument'''
        self.args.no_time = True
        with patch('argparse.ArgumentParser.parse_args',
                   return_value=self.args):
            with patch('weekly_tl.get_time',
                       return_value=(self.week_first, self.week_last)):
                with patch('weekly_tl.set_logfile',
                           return_value=self.LogFile):
                    weekly_tl.main()
                    output = sys.stdout.getvalue().strip()
                    self.assertRegex(output, self.regex_notime)

    def test_weekly_tl_with_logfile(self):
        '''testing weekly_tl with --logfile argument'''
        self.args.logfile = [self.LogFile]
        with patch('argparse.ArgumentParser.parse_args',
                   return_value=self.args):
            with patch('weekly_tl.get_time',
                       return_value=(self.week_first, self.week_last)):
                weekly_tl.main()
                output = sys.stdout.getvalue().strip()
                self.assertRegex(output, self.regex)

    def test_weekly_tl_with_env_variable(self):
        '''testing only 'new' argument with GTIMELOG_FILE env variable'''
        with patch('argparse.ArgumentParser.parse_args',
                   return_value=self.args):
            with patch('weekly_tl.get_time',
                       return_value=(self.week_first, self.week_last)):
                with patch('os.environ.get', return_value=self.LogFile):
                    weekly_tl.main()
                    output = sys.stdout.getvalue().strip()
                    self.assertRegex(output, self.regex)

    def test_weekly_tl_with_user_variable(self):
        '''testing weekly_tl with GTIMELOG_USER env variable'''
        with patch('argparse.ArgumentParser.parse_args',
                   return_value=self.args):
            with patch('weekly_tl.get_time',
                       return_value=(self.week_first, self.week_last)):
                with patch('os.environ.get', return_value='my-user'):
                    weekly_tl.main()
                    user_regex = re.compile(r'my-user')
                    output = sys.stdout.getvalue().strip()
                    self.assertRegex(output, user_regex)

    def test_weekly_tl_with_user_arg(self):
        '''testing weekly_tl with GTIMELOG_USER env variable'''
        self.args.user = ['my-user']
        with patch('argparse.ArgumentParser.parse_args',
                   return_value=self.args):
            with patch('weekly_tl.get_time',
                       return_value=(self.week_first, self.week_last)):
                weekly_tl.main()
                user_regex = re.compile(r'my-user')
                output = sys.stdout.getvalue().strip()
                self.assertRegex(output, user_regex)
