"""
PNL Command line tools for build local environment and deploying an environment on AWS
Elastic Beanstalk.

Usage: cw
    cw <command> [<command_arg>...] [--config-file=<filename>]
    cw --help
    cw --version
    cw (-l | --list-commands) [--config-file=<filename>]


Options:
    --help                  Show this screen
    --version               Show the version
    -l, --list-commands     List the commands from the config file

"""

from docopt import docopt
from subprocess import call
import json
import os


VERSION = '0.10'


def init(args):
    """
    Use to initialize your pnl dev environment. It will set following config:
        - AWS credentials
        - Docker credentials (required?)
        -...

    @param args:
    @return:
    """
    pass


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
    for command in command_list:
        command_with_args = command.format(*command_args)
        call(command_with_args, shell=True)


def parse_config(filename=None):
    default_file = os.path.abspath('commands.json')
    config_filename = default_file if filename is None else os.path.abspath(filename)
    with open(config_filename, 'r') as f:
        config = json.loads(f.read())
    return config


def main():
    arguments = docopt(__doc__)
    print arguments

    # Load config files
    global CONFIG_COMMANDS
    try:
        if arguments['--config-file'] is None:
            CONFIG_COMMANDS = parse_config()
        else:
            CONFIG_COMMANDS = parse_config(arguments['--config-file'])
    except IOError:
        print ("Config file cannot be found, name must commands.json, or pass custom location")
        exit(1)

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
    except (KeyError, ValueError):
        print ("Command not found")


if __name__ == '__main__':
    main()
