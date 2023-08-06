# coding: utf-8
# flake8: noqa
# cligen: 0.2.0, dd: 2022-09-21


import argparse
import importlib
import sys
import typing

from . import __version__


class HelpFormatter(argparse.RawDescriptionHelpFormatter):
    def __init__(self, *args: typing.Any, **kw: typing.Any):
        kw['max_help_position'] = 40
        super().__init__(*args, **kw)

    def _fill_text(self, text: str, width: int, indent: str) -> str:
        import textwrap

        paragraphs = []
        for paragraph in text.splitlines():
            paragraphs.append(textwrap.fill(paragraph, width,
                             initial_indent=indent,
                             subsequent_indent=indent))
        return '\n'.join(paragraphs)


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args: typing.Any, **kw: typing.Any):
        kw['formatter_class'] = HelpFormatter
        super().__init__(*args, **kw)


class DefaultVal(str):
    def __init__(self, val: typing.Any):
        self.val = val

    def __str__(self) -> str:
        return str(self.val)


class CountAction(argparse.Action):
    """argparse action for counting up and down

    standard argparse action='count', only increments with +1, this action uses
    the value of self.const if provided, and +1 if not provided

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action=CountAction, const=1,
            nargs=0)
    parser.add_argument('--quiet', '-q', action=CountAction, dest='verbose',
            const=-1, nargs=0)
    """

    def __call__(
        self,
        parser: typing.Any,
        namespace: argparse.Namespace,
        values: typing.Union[str, typing.Sequence[str], None],
        option_string: typing.Optional[str] = None,
    ) -> None:
        if self.const is None:
            self.const = 1
        try:
            val = getattr(namespace, self.dest) + self.const
        except TypeError:  # probably None
            val = self.const
        setattr(namespace, self.dest, val)


def main(cmdarg: typing.Optional[typing.List[str]]=None) -> int:
    cmdarg = sys.argv if cmdarg is None else cmdarg
    parsers = []
    parsers.append(ArgumentParser())
    parsers[-1].add_argument('--no-clear', default=None, dest='_gl_no_clear', action='store_true', help='test and clear between runs')
    parsers[-1].add_argument('--display', default=None, dest='_gl_display', metavar='DISPLAY', help='test and clear + display file contents of DISPLAY', action='store')
    parsers[-1].add_argument('--show-pdf', default=None, dest='_gl_show_pdf', action='store_true', help='show pdf file once (when auto-ing an .rst file)')
    parsers[-1].add_argument('--each', '-e', default=None, dest='_gl_each', action='store_true', help='test and try each argument seperately')
    parsers[-1].add_argument('--testverbose', '-t', default=DefaultVal(0), dest='_gl_testverbose', action='store_true', help='add -v to py.test invocation')
    parsers[-1].add_argument('--pep8', '-p', default=None, dest='_gl_pep8', action='store_true', help='run pep8 on all argument files')
    parsers[-1].add_argument('--flake8', default=None, dest='_gl_flake8', action='store_true', help='run flake8 on all argument files')
    parsers[-1].add_argument('--proceed', '-P', default=None, dest='_gl_proceed', action='store_true', help='proceed with command after running pep8/flake8')
    parsers[-1].add_argument('--todo-pdf', default=None, dest='_gl_todo_pdf', metavar='ID', help='run todo --show-pdf on todo item %(metavar)s', action='store')
    parsers[-1].add_argument('--todo-html', default=None, dest='_gl_todo_html', metavar='ID', help='run todo --show-html on todo item %(metavar)s', action='store')
    parsers[-1].add_argument('--stats', default=None, dest='_gl_stats', action='store_true', help='show statistics after run')
    parsers[-1].add_argument('--prof', default=None, dest='_gl_prof', action='store_true', help='run -m cProfile [-s time|--prof-arg]')
    parsers[-1].add_argument('--prof-arg', default=None, dest='_gl_prof_arg', metavar='PROF_ARG', action='append')
    parsers[-1].add_argument('--prof-lines', default=DefaultVal(30), dest='_gl_prof_lines', metavar='PROF_LINES', type=int, action='store')
    parsers[-1].add_argument('--python2', '--py2', '-2', default=None, dest='_gl_python2', action='store_true', help='run with python2')
    parsers[-1].add_argument('--python3', '--py3', '-3', default=None, dest='_gl_python3', action='store_true', help='run with python3')
    parsers[-1].add_argument('--last', '-l', default=None, dest='_gl_last', action='store_true', help='this sets the command to the first previous command,\n        from the bash commandline, that does not start with "auto ".\n        Normally used in order not to retype and/or quote something\n        your tried just before. Set \'alias auto="history -a | auto"\'.\n        ')
    parsers[-1].add_argument('--cligen', '-C', default=None, dest='_gl_cligen', action='store_true', help="run cligen, ignore change of __main__.py, so you can use 'auto --cligen -c xxx *.py'")
    parsers[-1].add_argument('--errorexit', '-E', default=None, dest='_gl_errorexit', action='store_true', help='used to test autotest.py, stop processing further commands on error')
    parsers[-1].add_argument('--command', '-c', default=None, dest='_gl_command', metavar='COMMAND', action='append', help='command to be run on changes (multiple)')
    parsers[-1].add_argument('--arg', default=None, dest='_gl_arg', metavar='ARG', action='append', help='arguments to pass to file to test')
    parsers[-1].add_argument('filenames', nargs='*', action='store')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(0), dest='_gl_verbose', metavar='VERBOSE', nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--quiet', '-q', default=DefaultVal(0), dest='_gl_quiet', metavar='QUIET', nargs=0, help='decrease verbosity level', action=CountAction, const=-1)
    parsers[-1].add_argument('--no-auto-dev', default=None, dest='_gl_no_auto_dev', metavar='NO_AUTO_DEV', help='do not check and restart auto when **its** sources change', action='store')
    parsers[-1].add_argument('--version', action='store_true', help='show program\'s version number and exit')
    if '--version' in cmdarg[1:]:
        if '-v' in cmdarg[1:] or '--verbose' in cmdarg[1:]:
            return list_versions(pkg_name='ruamel.auto', version=None, pkgs=['ruamel.yaml', 'ruamel.std.pathlib'])
        print(__version__)
        return 0
    if '--help-all' in cmdarg[1:]:
        try:
            parsers[0].parse_args(['--help'])
        except SystemExit:
            pass
        for sc in parsers[1:]:
            print('-' * 72)
            try:
                parsers[0].parse_args([sc.prog.split()[1], '--help'])
            except SystemExit:
                pass
        sys.exit(0)
    args = parsers[0].parse_args(args=cmdarg[1:])
    for gl in ['no_clear', 'display', 'show_pdf', 'each', 'testverbose', 'pep8', 'flake8', 'proceed', 'todo_pdf', 'todo_html', 'stats', 'prof', 'prof_arg', 'prof_lines', 'python2', 'python3', 'last', 'cligen', 'errorexit', 'command', 'arg', 'verbose', 'quiet', 'no_auto_dev']:
        glv = getattr(args, '_gl_' + gl, None)
        setattr(args, gl, glv)
        delattr(args, '_gl_' + gl)
        if isinstance(getattr(args, gl, None), DefaultVal):
            setattr(args, gl, getattr(args, gl).val)
    cls = getattr(importlib.import_module('ruamel.auto.auto'), 'Auto')
    obj = cls(args)
    funcname = getattr(args, 'subparser_func', None)
    if funcname is None:
        funcname = 'run'
    fun = getattr(obj, funcname + '_subcommand', None)
    if fun is None:
        fun = getattr(obj, funcname)
    ret_val = fun()
    if ret_val is None:
        return 0
    if isinstance(ret_val, int):
        return ret_val
    return -1

def list_versions(pkg_name: str, version: typing.Union[str, None], pkgs: typing.Sequence[str]) -> int:
    version_data = [
        ('Python', '{v.major}.{v.minor}.{v.micro}'.format(v=sys.version_info)),
        (pkg_name, __version__ if version is None else version),
    ]
    for pkg in pkgs:
        try:
            version_data.append(
                (pkg,  getattr(importlib.import_module(pkg), '__version__', '--'))
            )
        except ModuleNotFoundError:
            version_data.append((pkg, 'NA'))
        except KeyError:
            pass
    longest = max([len(x[0]) for x in version_data]) + 1
    for pkg, ver in version_data:
        print('{:{}s} {}'.format(pkg + ':', longest, ver))
    return 0


if __name__ == '__main__':
    sys.exit(main())
