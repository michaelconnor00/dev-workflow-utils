"""
PNL Command line tools for build local environment and deploying an environment on AWS
Elastic Beanstalk.

Usage: cw
    cw [-d | --debug] <command> [<command_arg>...] [--config-file=<filename>]
    cw --help
    cw --version
    cw (-l | --list-commands) [--config-file=<filename>]


Options:
    --help                  Show this screen
    --version               Show the version
    -l, --list-commands     List the commands from the config file
    -d, --debug

"""

from docopt import docopt
import subprocess
from subprocess import PIPE, STDOUT
import json
import os, sys
from string import Template


VERSION = '0.45'


class CWTemplate (Template):
    """
    Subclass of Python String Template to Change delimiter for IDL use.
    """
    delimiter = "#"


def version(args):
    print ('Command Wrapper v%s' % VERSION)


def list_commands(args):
    print 'Commands: '
    for command in CONFIG_COMMANDS.keys():
        print ('\t%s' % command)


def run(command_list, command_args):
    """
    Blindly run the commands provided in the list.
    :param command_list: list of commands and arguments
    """
    run_script = ['/bin/bash']
    script = '#!/bin/bash\n'
    use_script = False

    command_kwargs = {}

    # Parse kwargs
    for arg in command_args:
        if '=' in arg:
            arg_parts = arg.split('=')
            command_kwargs.update({arg_parts[0]: arg_parts[1]})

    for command in command_list:
        # The following will attempt to substitute the
        # command line args into the command.

        if len(command_args) > 0:
            # Use Python string substitution
            command_template = CWTemplate(command)
            command_with_args = command_template.substitute(
                **command_kwargs[0]
            )
        else:
            # Split the command and remove any args with # for templating.
            command_parts = command.split(' ')
            no_args_command = []
            for part in command_parts:
                if not part.startswith('#'):
                    no_args_command.append(part)
            command_with_args = ' '.join(no_args_command)

        if '--SHELL' in command:
            use_script = True

        if use_script:
            if '--SHELL' not in command:
                script += 'echo \"> %s\"\n' % command_with_args
                script += '%s\n' % command_with_args
        else:
            print '> %s' % command_with_args
            os.system(command_with_args)

    if use_script:
        if DEBUG:
            print 'SCRIPT:\n', script

        process = subprocess.Popen(run_script, stdin=PIPE, stderr=STDOUT, stdout=PIPE, env=os.environ.copy())

        # data, err = process.communicate(input=script)
        process.stdin.write(script)
        process.stdin.close()

        for line in iter(process.stdout.readline, b''):
            print line
        process.stdout.close()
        process.wait()


def parse_config(filename=None):
    default_file = os.path.abspath('commands.json')
    config_filename = default_file if filename is None else os.path.abspath(filename)
    with open(config_filename, 'r') as f:
        try:
            config = json.loads(f.read())
        except ValueError as e:
            print 'Command.json cannot be read, check the file is valid JSON and retry'
            sys.exit(1)
    return config


def main():
    arguments = docopt(__doc__)

    # Load config files
    global CONFIG_COMMANDS
    global DEBUG
    DEBUG = arguments['--debug']

    if DEBUG:
        print 'ARGS:\n', arguments

    try:
        if arguments['--config-file'] is None:
            CONFIG_COMMANDS = parse_config()
        else:
            CONFIG_COMMANDS = parse_config(arguments['--config-file'])
    except IOError:
        print ("Config file cannot be found, name must commands.json, or pass custom location")
        # exit(1)  # exit if custom commands cannot be found?

    base_commands = {
        '--version': version,
        '--list-commands': list_commands
    }

    command_found = False

    try:
        if arguments['<command>'] is not None and CONFIG_COMMANDS is not None:
            command_found = True
            run(CONFIG_COMMANDS[arguments['<command>']], command_args=arguments['<command_arg>'])

        for key, value in arguments.iteritems():
            if value and key in base_commands.keys():
                command_found = True
                base_commands[key](arguments)

        if not command_found:
            raise ValueError
    except (KeyError, ValueError) as e:
        print 'ERROR: ', e
        print ("Command not found")


if __name__ == '__main__':
    main()
