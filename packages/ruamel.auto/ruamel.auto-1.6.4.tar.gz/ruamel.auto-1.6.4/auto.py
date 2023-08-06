# coding: utf-8

from __future__ import print_function

"""
run
  unittest
  python
  pep8
on a program file (first argument) every time any of the argument files
are touched

if you have an alias for auto:
alias auto="history -a; auto"

"""

# testing new functionality in auto.py:
# python -m ruamel.auto --command "auto --errorexit adding_argcomplete.rst" ~/src/site-packages/ruamel/auto.py


import sys
import os
import stat
import time
import datetime
import shlex
import platform
from glob import glob


def is_windows():
    return platform.system() == "Windows"


def string_in_file(string, fname):
    """test for a string to be in a file"""
    data = open(fname, 'r').read()
    return string in data


class Auto:
    def __init__(self, args, config=None):
        self._args = args
        self._config = config
        self.stats = None

    def run(self):
        # if you need to test whether this was started from "auto"
        os.environ['RUAMELAUTOTEST'] = os.environ.get('RUAMELAUTOTEST', '1')
        os.environ['RUAMELDEBUG'] = "1"
        # allow for unicode output
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        filenames = self._args.filenames
        if self._args.last:
            # test piped from stdin
            mode = os.fstat(0).st_mode
            if stat.S_ISFIFO(mode):
                lines = sys.stdin.read().splitlines()
                for cmd in reversed(lines[:-1]):
                    # skip number
                    cmd = cmd.split(None, 1)[1]
                    if cmd[0] == 'vi':
                        continue
                    if not cmd.startswith('auto '):
                        break
                print('auto: reusing command "{}"'.format(shlex.split(cmd)))
                if self._args.command is None:
                    self._args.command = []
                self._args.command.append(cmd)
                if self._args.verbose > 0:
                    print('cmd', cmd)
            else:
                return '--last expects history information piped to stdin'
        if self._args.todo_pdf or self._args.todo_html:
            todo_pattern = os.path.expanduser('~/.config/todo/{}.rst')
            w = os.path.basename(glob(todo_pattern.format('*'))[0]).index('-')
            if self._args.todo_pdf:
                num = int(self._args.todo_pdf)
            elif self._args.todo_html:
                num = int(self._args.todo_html)
            else:
                raise NotImplementedError
            numstr = "{:0{}}-*".format(num, w)
            print('numstr', numstr)
            filenames.insert(0, glob(todo_pattern.format(numstr))[0])
        if not filenames:
            print("auto: you have to provide at least one filename")
            sys.exit(1)
        if self._args.cligen and '__main__.py' in filenames:
            filenames.remove('__main__.py')
        if self._args.verbose > 0:  # can be negative with --quiet
            print(filenames)
        self._cmd = []
        self._cmds_once_after_first_run = []
        # self._args.no_clear = True
        if self._args.python2:
            # py = '/home/venv/dev/bin/python'
            py = '/opt/util/py27/bin/python'
        else:
            # py = '/home/venv/dev3/bin/python'
            py = '/opt/util/py310/bin/python'
        if not self._args.no_clear:
            if is_windows():
                self._cmd.append(['cls'])
            else:
                self._cmd.append(['/usr/bin/clear'])
        if self._args.cligen:
            self._cmd.append(['cligen'])
        if self._args.pep8:
            # should read max-line-length from tox.ini
            # self._cmd.append(['pep8', '--max-line-length=95'] + self._args.filenames)
            # self._cmd.append(['flake8'] + self._args.filenames)
            self._args.flake8 = True
        if self._args.flake8:
            self._cmd.append(['flake8'] + self._args.filenames)
        if (self._args.pep8 or self._args.flake8) and not self._args.proceed:
            pass
        elif os.path.isdir(filenames[0]):
            if filenames[0] == '_test':
                self._cmd.append(['py.test', '_test', '--ignore="_test/*_flymake.py"'])
                filenames = glob('*.py') + glob('_test/*.py')
                # print('cmd', self._cmd[-1])
                # print('fns', filenames)
            # sys.exit(0)
        elif self._args.command:
            for command in self._args.command:
                # start with a slash -> explicit python
                if command[0] != '/' and not 'ruamel.eu' in command and \
                   'ruamel.' in command and '.tar.' not in command:
                    self._cmd.append([py, '-m'] +
                                     shlex.split(command))
                else:
                    self._cmd.append(shlex.split(command))
        elif self._args.todo_html:
            self._cmd.append(['todo', 'html', str(self._args.todo_html)])
        elif self._args.todo_pdf:
            self._cmd.append(['todo', 'pdf', str(self._args.todo_pdf)])
        elif self._args.display:
            self._cmd.extend([['/usr/bin/clear'],
                              ['/bin/cat', self._args.display]])
        else:
            fn0 = filenames[0]
            is_python = fn0.endswith('.py')
            if is_python and string_in_file('pytest', filenames[0]):
                cmd = ['py.test', ]
                if self._args.testverbose > 0:
                    cmd.append('-v')
                cmd.append(filenames[0])
                self._cmd.append(cmd)
            elif is_python and string_in_file('unittest', filenames[0]):
                cmd = ['python', '-m', 'unittest', ]
                if self._args.testverbose > 0:
                    cmd.append('-v')
                cmd.append(filenames[0].replace('.py', ''))
                self._cmd.append(cmd)
            else:
                if self._args.each:
                    self._cmd = {}  # ToDo use different name
                    for filename in filenames:
                        if os.path.exists(filename):
                            self._cmd[filename] = self.do_command(filename, py)
                else:
                    self._cmd.append(self.do_command(filenames[0],
                                     self._cmds_once_after_first_run, py))
        if self._args.verbose > 0:
            print('cmds', self._cmd)
        self._ts = self.set_start_times(filenames)
        #print('ts', self._ts)
        try:
            # self.test_run_and_sleep(1, self._args.filenames, self._cmd,
            #                        self._cmds_once_after_first_run)
            self.test_run_and_sleep(1, filenames, self._cmd,
                                    self._cmds_once_after_first_run)
        except KeyboardInterrupt:
            # to prevent history editing from being offset by ^C
            sys.stdout.write('\r   \r')
            return 0
        except:
            raise
        return 0

    def set_start_times(self, filenames):
        retval = {}
        for filename in filenames:
            root, ext = os.path.splitext(filename)
            if ext == '.rst':
                try:
                    pdf = root + '.pdf'
                    if os.path.exists(pdf):
                        retval[filename] = os.path.getmtime(pdf)
                        continue
                except IOError:
                    pass
            retval[filename] = 0
        return retval

    def do_command(self, arg, cmds_once_after_first_run, py):
        root, ext = os.path.splitext(arg)
        cmd = None
        if ext == '.py':
            cmd = ['python' if is_windows() else py, ]
            cmd.append(arg)
        elif ext == '.rst':
            cmd = ['rst2pdf']
            cmd.append(arg)
            cmds_once_after_first_run.append(['atril', root + '.pdf', '&'])
        elif ext == '.ryd':
            cmd = ['ryd', '--force']
            cmd.append(arg)
            # should only do this when pdf generation is specified in the first
            # YAML document in the file
            if gen_pdf_from_ryd(arg):
                cmds_once_after_first_run.append(['atril', root + '.pdf', '&'])
        elif ext == '.nim':
            cmd = ['nim', 'compile', '--run', '--verbosity:0', '--implicitStatic:on']
            cmd.append(arg)
            # only should show output when error exit, rerun with verbosity:2 or
            # do that in the first place and not show output?
        elif ext == '':
            with open(arg) as fp:
                head = fp.read(80)
            if head.startswith('#!'):
                if True:
                    cmd = [arg]
                elif 'python2.7' in head:
                    cmd = ['python2.7', ]
                    cmd.append(arg)
                elif 'python3' in head:
                    cmd = ['python3', ]
                    cmd.append(arg)
                elif 'python' in head:
                    cmd = ['python', ]
                    cmd.append(arg)
            if cmd is None:
                raise NotImplementedError
        else:
            raise NotImplementedError
        if self._args.testverbose > 0:
            cmd.append('-v')
        if self._args.prof:
            prof = ['-m', 'cProfile']
            prof.extend(self._args.prof_arg if self._args.prof_arg else ['-s', 'time'])
            cmd[1:1] = prof
        if self._args.arg:
            cmd.extend(self._args.arg)
        return cmd

    def test_run_and_sleep(self, seconds, filenames=None, cmd = None, cmds_after_first_run=[]):
        if cmd is None:
            cmd = self._cmd
        if cmd is None:
            return
        # can be list of list for multiple commands
        cmds = cmd if isinstance(cmd[0], list) else [cmd]
        cafr = cmds_after_first_run[:]
        if filenames is None:
            filenames = self._args.filenames
        while True:
            if not self._args.no_auto_dev:
                self.restart_if_changed()
            changed = False
            index = -1
            for fn in filenames:
                while True:
                    try:
                        ts = os.path.getmtime(fn)
                        break
                    except FileNotFoundError:
                        time.sleep(1)
                        if index == -1:
                            print('\nwaiting for file {} to reappear'.format(fn))
                            index = 0
                        sys.stdout.write('-\|/'[index])
                        index = (index + 1) % 4
                        sys.stdout.write('\r')
                        sys.stdout.flush()
                if ts > self._ts[fn]:
                    self._ts[fn] = ts  # set the rest of the ts as well
                    if isinstance(self._cmd, dict):
                        cmd = self._cmd.get(fn)
                        print(datetime.datetime.now().replace(microsecond=0), cmd)
                        res = self.call(cmd)
                        # print('auto res', res, self._args.errorexit)
                        if res and self._args.errorexit:
                            return
                    else:
                        changed = True
            if changed:
                for cmd in cmds:
                    print(datetime.datetime.now().replace(microsecond=0), cmd)
                    try:
                        if is_windows() and cmd[0] in ['cls']:
                            shell = True
                        else:
                            shell = False
                        res = self.call(cmd, shell=shell)
                        if res and self._args.errorexit:
                            break
                    except OSError:
                        if not is_windows():
                            # see if this is an alias
                            with open(os.path.expanduser('~/.aliases')) as ifp:
                                for line in ifp:
                                    if line.startswith('alias ' + cmd[0]):
                                        alias = line.split("=", 1)[1].lstrip()
                                        # next line does not handle escaped quotes
                                        alias = alias[1:].split(alias[0], 1)[0]
                                        alias = alias.split()
                                        # print('found alias', line.rstrip(), alias)
                                        # insert the alias, into the command,
                                        #  this is done once
                                        cmd[0] = alias[-1]
                                        alias = alias[:-1]
                                        while alias:
                                            cmd.insert(0, alias[-1])
                                            alias = alias[:-1]
                            res = self.call(cmd)
                            sys.stdout.flush()
                            if res and self._args.errorexit:
                                break
                    if self.stats is not None:
                        print('size: {0}Mb, user: {user}s, '
                              'system: {system}s, {elapsed}'.format(
                                  self.stats['size'] // 1000, **self.stats))
                        self.stats = None
                    # print('res', res)
                    try:
                        if res and self._args.errorexit:
                            break
                    except UnboundLocalError:
                        print('cmd', cmd)
                        raise
            # changed or not, the result file should be there (e.g. PDF file, need to show)
            if cafr:
                for cmd in cafr:
                    print(datetime.datetime.now(), cmd)
                    res = self.call(cmd, shell=True)
                cafr = None
            time.sleep(seconds)

    def call(self, cmd, stdin=None, stdout=None, stderr=None, out=None,
             dryrun=None, verbose=None, shell=False):
        # print(os.environ['PATH'])
        from ruamel.showoutput import ShowOutput
        stats = self._args.stats
        show_output = ShowOutput(stats=stats)
        import subprocess
        if cmd[-1] == '&':
            print('spawning')
            subprocess.Popen(cmd[:-1])
            return 0
        verbose = verbose if verbose is not None else self._args.verbose
        try:
            res = None
            if cmd[0] in ['/usr/bin/clear', ]:
                # showoutput does break the clear binary
                subprocess.check_call(cmd, stderr=subprocess.STDOUT)
            else:
                res = show_output(cmd, stderr=subprocess.STDOUT)  # NOQA
                if stats:
                    self.stats = show_output.stats.copy()
        except subprocess.CalledProcessError as e:
            if self._args.flake8:
                file_name, line_nr, col = None, None, None
                for line in e.output.splitlines():
                    if '.py:' not in line:
                        continue
                    try:
                        file_name, line_nr, col, rest = line.split(':', 3)
                    except:
                        pass
                if file_name is not None:
                    subprocess.call(['em', '+{}:{}'.format(line_nr, col), file_name])
                    # subprocess.call(['wing5.1', '{}:{}'.format(file_name, line_nr)])
                #     # print(file_name, line_nr, col)
            return 1
        return 0
        # return self._call(cmd, stdin=stdin, stdout=stdout, stderr=stderr,
        #                   out=out, dryrun=dryrun, verbose=verbose, shell=shell)

    def restart_if_changed(self):
        if _file_updated():
            args = sys.argv[:]
            args.insert(0, sys.executable)
            print('\n################# restarting ###############')
            time.sleep(1)
            os.execl(sys.executable, *args)


# from ruamel.util.scandir, should be packed in a class/library
_file_to_observe = __file__.replace('.pyc', '.py').replace('.pyo', '.py')
_file_ts = os.path.getmtime(_file_to_observe)


def _file_updated():
    return os.path.getmtime(_file_to_observe) > _file_ts



'''

from oruamel.doc.txt import string_in_file
from oruamel.util._argcomplete import filescompleter



'''


def gen_pdf_from_ryd(ryd_file):
    from ruamel.yaml import YAML
    yaml = YAML(typ='safe')
    for data in yaml.load_all(open(ryd_file)):
        break
    return data.get('pdf')
