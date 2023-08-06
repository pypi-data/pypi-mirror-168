import os
from termcolor import colored

def terminal():
    try:
        def colored_text(text, color):
            return colored(str(text), str(color))

        import argparse
        parser = argparse.ArgumentParser(prog="clixdev", usage=colored_text("\rusage: clixdev (--help -h) [generate, sync, docs] <token1> <token2> (--path -p)", "yellow"),
                                         description=colored_text("The Command Line Interface for Clix (clix.dev). run clixdev -h for more.", 'green'), epilog=colored_text("What can be better? Tell us https://clix.dev/contact", "grey"))
        parser.add_argument('action', choices=['generate', 'sync', 'docs'], help="""You can use this cli to generate a new project, sync your project as you develop, and create a simple documentation for your project.""", metavar=colored_text("action\t", "cyan"))
        parser.add_argument('terminal_token', help='The 6 character token in your account page at clix.dev.', type=str)
        parser.add_argument('project_token', help='The 6 character token in your projects page at clix.dev.', type=str)
        parser.add_argument('-p', '--path', dest="path", help="Please specify an optional path to your Clix project.", type=lambda p: p if os.path.isdir(p) else NotADirectoryError(p), required=False, metavar='')
        args = parser.parse_args()

        if args.action == 'generate':
            from .commands import Commands
            return Commands(args.terminal_token, args.project_token, args.path, args).generate()

        if args.action == 'sync':
            from .commands import Commands
            return Commands(args.terminal_token, args.project_token, args.path, args).sync()
        
        if args.action == 'docs':
            from .commands import Commands
            return Commands(args.terminal_token, args.project_token, args.path, args).docs()
        return False
    except Exception as e:
        print(e)
        return False
