# coding: utf-8

from __future__ import print_function
from __future__ import absolute_import

_package_data = dict(
    full_package_name='ruamel.auto',
    version_info=(1, 6, 4),
    __version__='1.6.4',
    version_timestamp='2022-09-21 10:06:53',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description='automate testing and pep8 conformance of python code',
    toxver=['2.7'],
    entry_points='auto=ruamel.auto.__main__:main',
    since=1998,
    install_requires=['ruamel.yaml', 'ruamel.std.pathlib', 'ruamel.showoutput'],
    universal=True,
)


version_info = _package_data['version_info']
__version__ = _package_data['__version__']

_cligen_data = """\
# all tags start with an uppercase char and can often be shortened to three and/or one
# characters. If a tag has multiple uppercase letter, only using the uppercase letters is a
# valid shortening
# Tags used:
# !Commandlineinterface, !Cli,
# !Option, !Opt, !O
  # - !Option [all, !Action store_true, !Help build sdist and wheels for all platforms]
# !PreSubparserOption, !PSO
# !Alias for a subparser
# - !DefaultSubparser  # make this (one) subparser default
# !Help, !H
# !HelpWidth 40    # width of the left side column width option details
# !Argument, !Arg
  # - !Arg [files, nargs: '*', !H files to process]
# !Module   # make subparser function calls imported from module
# !Instance # module.Class: assume subparser method calls on instance of Class imported from module
# !Main     # function to call/class to instantiate, no subparsers
# !Action # either one of the actions in cligen subdir _action (by stem of the file) or e.g. "store_action"
# !Config YAML/INI/PON  read defaults from config file
# !AddDefaults ' (default: %(default)s)'
# !Prolog (sub-)parser prolog/description text (for multiline use | ), used as subparser !Help if not set
# !Epilog (sub-)parser epilog text (for multiline use | )
# !NQS used on arguments, makes sure the scalar is non-quoted e.g for instance/method/function
#      call arguments, when cligen knows about what argument a keyword takes, this is not needed
!Cli 0:
- !PSO [no-clear, !Action store_true, !Help test and clear between runs]
- !PSO [display, !Help test and clear + display file contents of DISPLAY]
- !PSO [show-pdf, !Action store_true, !Help show pdf file once (when auto-ing an .rst file)]
- !PSO [each, e, !Action store_true, !Help test and try each argument seperately]
- !PSO [testverbose, t, default: 0, !Action store_true, !Help add -v to py.test invocation]
- !PSO [pep8, p, !Action store_true, !Help run pep8 on all argument files]
- !PSO [flake8, !Action store_true, !Help run flake8 on all argument files]
- !PSO [proceed, P, !Action store_true, !Help proceed with command after running pep8/flake8]
- !PSO [todo-pdf, metavar: ID, !Help run todo --show-pdf on todo item %(metavar)s]
- !PSO [todo-html, metavar: ID, !Help run todo --show-html on todo item %(metavar)s]
- !PSO [stats, !Action store_true, !Help show statistics after run]
- !PSO [prof, !Action store_true, !Help 'run -m cProfile [-s time|--prof-arg]']
- !PSO [prof-arg, !Action append]
- !PSO [prof-lines, type: int, default: 30]
- !PSO [python2, py2, '2', !Action store_true, !Help run with python2]
- !PSO [python3, py3, '3', !Action store_true, !Help run with python3]
- !PSO [last, l, !Action store_true, !Help "this sets the command to the first previous command,\n        from the bash commandline, that does not start with \"auto \".\n        Normally used in order not to retype and/or quote something\n        your tried\
    \ just before. Set 'alias auto=\"history -a | auto\"'.\n        "]
- !PSO [cligen, C, !Action store_true, !Help "run cligen, ignore change of __main__.py, so you can use 'auto --cligen -c xxx *.py'"]
- !PSO [errorexit, E, !Action store_true, !Help 'used to test autotest.py, stop processing further commands on error']
- !PSO [command, c, !Action append, !Help command to be run on changes (multiple)]
- !PSO [arg, !Action append, !Help arguments to pass to file to test]
- !Arg [filenames, nargs: '*']
- !Opt [verbose, v, !Help increase verbosity level, !Action count, const: 1, nargs: 0, default: 0]
- !Opt [quiet, q, !Help decrease verbosity level, !Action count, const: -1, nargs: 0]
- !PSO [no-auto-dev, !Help do not check and restart auto when **its** sources change]
- !Instance ruamel.auto.auto.Auto
"""  # NOQA
