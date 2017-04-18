import unittest
import sys
import tempfile
import os
import shutil
from mock import patch
import tl


class TlTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.workdir = tempfile.mkdtemp()
        self.LogFile = os.path.join(self.workdir, 'timelog.txt')
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

    def test_create_logfile(self):
        '''
        Test new logfile creation
        '''
        newlogfile = os.path.join(self.workdir, 'newtimelog.txt')
        self.assertFalse(os.path.exists(newlogfile),
                         '%s already exists' % newlogfile)
        argfile = [newlogfile]
        tl.set_logfile(argfile)
        self.assertTrue(os.path.exists(newlogfile),
                        '%s not created' % newlogfile)

    def test_create_logfile_no_dir(self):
        '''
        Test new logfile creation in inexistant directory
        '''
        newlogfile = os.path.join(self.workdir, 'a/b', 'newtimelog.txt')
        self.assertFalse(os.path.exists(newlogfile),
                         '%s already exists' % newlogfile)
        argfile = [newlogfile]
        tl.set_logfile(argfile)
        self.assertTrue(os.path.exists(newlogfile),
                        '%s not created' % newlogfile)
    def test_create_logfile_dir_exists(self):
        '''
        Test new logfile creation in directory that already exists
        '''
        newlogfile = os.path.join(self.workdir, 'c/d', 'newtimelog.txt')
        self.assertFalse(os.path.exists(newlogfile),
                         '%s already exists' % newlogfile)
        os.mkdir(self.workdir+'/c')
        argfile = [newlogfile]
        tl.set_logfile(argfile)
        self.assertTrue(os.path.exists(newlogfile),
                        '%s not created' % newlogfile)

    def test_new_entry(self):
        '''testing only 'new' argument'''
        tl.LogFile = self.LogFile
        tl.log_activity('new', 'Arrived')
        line = self._get_last_log_line().strip()
        self.assertTrue(line.endswith('Arrived'))

    def test_logfile_with_arg(self):
        '''testing logfile definition with --logfile argument'''
        argfile = [self.LogFile]
        logfile = tl.set_logfile(argfile)
        self.assertTrue(logfile, self.LogFile)

    def test_logfile_with_empty_env_variable(self):
        '''testing logfile definition with empty GTIMELOG_FILE env variable'''
        os.environ.setdefault('GTIMELOG_FILE', '')
        with patch('os.path.expanduser', return_value=self.workdir):
            with patch('os.path.exists', return_value=True):
                logfile = tl.set_logfile()
        default_target = '%s/.local/share/gtimelog/timelog.txt' % self.workdir
        self.assertEquals(logfile, default_target)
        os.environ.pop('GTIMELOG_FILE')

    def test_logfile_with_env_variable(self):
        '''testing logfile definition with GTIMELOG_FILE env variable'''
        os.environ.setdefault('GTIMELOG_FILE', '%s' % self.LogFile)
        logfile = tl.set_logfile()
        self.assertEquals(logfile, self.LogFile)
        os.environ.pop('GTIMELOG_FILE')

    def test_ua_entry(self):
        '''testing a UA entry'''
        tl.LogFile = self.LogFile
        tl.log_activity('ua', 'This is one entry')
        line = self._get_last_log_line().strip()
        self.assertTrue(line.endswith('L3 / L3 support : This is one entry'))

    def test_not_logged(self):
        '''testing argument with two asterix'''
        tl.LogFile = self.LogFile
        tl.log_activity('lunch**')
        line = self._get_last_log_line().strip()
        self.assertTrue(line.endswith('lunch**'))

    def test_absolutely_not_logged(self):
        '''testing argument with three asterix'''
        tl.LogFile = self.LogFile
        tl.log_activity('lunch***')
        line = self._get_last_log_line().strip()
        self.assertTrue(line.endswith('lunch***'))

    def test_help_prettytable(self):
        '''testing ? to get help when prettytable is installed'''
        tl.show_help()
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, """+-------+----------------------------+
| Key   | Description                |
+-------+----------------------------+
| charm | Charm Devel                |
| comm  | Community Involvment       |
| doc   | Documentation              |
| fan   | Fan development            |
| ib    | Mellanox related           |
| is    | IS bug work                |
| kb    | Knowledge base Work        |
| lp    | Launchpad & Public         |
| meet  | Meetings                   |
| pers  | Personal management        |
| pto   | Paid Timeout               |
| qe    | QE                         |
| seg   | SEG related activities     |
| svvp  | SVVP/Virtio dev            |
| train | Mentoring / Edu / Training |
| ua    | L3 / L3 support            |
| z     | Mainframe related          |
+-------+----------------------------+""")

    def test_select_tasks_out_of_range(self):
        '''testing category only and giving out of range answer'''
        with patch('builtins.input', return_value='3'):
            tl.select_tasks('ua')
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, """1) SF801-kdump
2) SF7-openafs
Invalid task number""")

    def test_select_tasks_select_0(self):
        '''testing category only and answering 0'''
        with patch('builtins.input', return_value='0'):
            self.assertEqual(tl.select_tasks('ua'), (None, None))
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, '1) SF801-kdump\n2) SF7-openafs')

    def test_select_tasks_select_nothing(self):
        '''testing category only and answering nothing'''
        with patch('builtins.input', return_value=''):
            self.assertEqual(tl.select_tasks('ua'), (None, None))
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, '1) SF801-kdump\n2) SF7-openafs')

    def test_select_tasks_select_first_task(self):
        '''testing category only and selecting first task'''
        with patch('builtins.input', return_value='1'):
            self.assertEqual(tl.select_tasks('ua'), ('ua', 'SF801-kdump'))
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, '1) SF801-kdump\n2) SF7-openafs')

    def test_category_with_exactly_10_items(self):
        '''testing category with 10 entries and selecting last task'''
        with patch('builtins.input', return_value='10'):
            self.assertEqual(tl.select_tasks('meet'), ('meet', 'maas'))
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, """1) mom
2) kernel
3) sabdfl
4) server
5) foundation
6) mgr
7) team
8) supp
9) juju
10) maas""", 'maas')

    def test_category_with_exactly_10_items_no_selection(self):
        '''testing category with 10 entries and no selection'''
        with patch('builtins.input', return_value=''):
            self.assertEqual(tl.select_tasks('meet'), (None, None))
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, """1) mom
2) kernel
3) sabdfl
4) server
5) foundation
6) mgr
7) team
8) supp
9) juju
10) maas""")

    def test_category_with_12_items(self):
        '''testing category with 12 entries and selecting first task'''
        with patch('builtins.input', return_value='1'):
            self.assertEqual(tl.select_tasks('train'), ('train', 'pascal'))
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, """1) pascal
2) basic
3) erlang
4) nodejs
5) java
6) go
7) perl
8) apl
9) c
10) ruby""")

    def test_category_with_12_items_no_selection(self):
        '''testing category with 12 entries and not selecting task'''
        with patch('builtins.input', return_value=''):
            self.assertEqual(tl.select_tasks('train'), (None, None))
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, """1) pascal
2) basic
3) erlang
4) nodejs
5) java
6) go
7) perl
8) apl
9) c
10) ruby
11) python""")

    def test_category_with_12_items_last_selection(self):
        '''testing category with 12 entries and selecting first task'''
        with patch('builtins.input', return_value='11'):
            self.assertEqual(tl.select_tasks('train'), ('train', 'python'))
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, """1) pascal
2) basic
3) erlang
4) nodejs
5) java
6) go
7) perl
8) apl
9) c
10) ruby""")

    def test_category_with_31_items(self):
        '''testing category with 31 entries and selecting first task'''
        with patch('builtins.input', return_value='1'):
            self.assertEqual(tl.select_tasks('lp'), ('lp', 'what'))
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, """1) what
2) false
3) true
4) ifenslave
5) autoconf
6) autotools
7) make
8) grep
9) awk
10) binutils""")

    def test_category_with_31_items_task_11(self):
        '''testing category with 31 entries and selecting eleventh task'''
        with patch('builtins.input', return_value='11'):
            self.assertEqual(tl.select_tasks('lp'), ('lp', 'sleep'))
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, """1) what
2) false
3) true
4) ifenslave
5) autoconf
6) autotools
7) make
8) grep
9) awk
10) binutils""")

    def test_category_with_31_items_task_21(self):
        '''testing category with 31 entries and selecting twenty-first task'''
        with patch('builtins.input', return_value='21'):
            self.assertEqual(tl.select_tasks('lp'), ('lp', 'juju'))
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, """1) what
2) false
3) true
4) ifenslave
5) autoconf
6) autotools
7) make
8) grep
9) awk
10) binutils""")

    def test_raw_categories(self):
        tl.print_categories()
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, """charm
comm
doc
fan
ib
is
kb
lp
meet
pers
pto
qe
seg
svvp
train
ua
z""")

    def test_print_tasks_meet(self):
        tl.print_tasks("meet")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, """mom
kernel
sabdfl
server
foundation
mgr
team
supp
juju
maas""")

    def test_print_tasks_ua(self):
        tl.print_tasks("ua")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, """SF801-kdump
SF7-openafs""")

    def test_print_tasks_train(self):
        tl.print_tasks("train")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, """pascal
basic
erlang
nodejs
java
go
perl
apl
c
ruby
python""")

    def test_logfile_default(self):
        with patch('os.path.expanduser', return_value=self.workdir):
            with patch('tl.create_logfile', return_value=self.LogFile):
                Log = tl.set_logfile()
                self.assertEqual(Log, '%s/.local/share/gtimelog/timelog.txt'
                                 % self.workdir)

    def test_logfile_arg(self):
        argline = ['%s/mylog' % self.workdir]
        Log = tl.set_logfile(argline)
        self.assertEqual(Log, '%s/mylog' % self.workdir)

    def test_logfile_env_variable(self):
        with patch('os.environ.get',
                   return_value='%s/mylogenv' % self.workdir):
            Log = tl.set_logfile()
            self.assertEqual(Log, '%s/mylogenv' % self.workdir)

    def _get_last_log_line(self):

        with open(self.LogFile, 'r') as timelog:
            for line in timelog:
                continue
        return(line)
