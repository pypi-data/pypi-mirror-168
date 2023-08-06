def terminal():
    try:
        import argparse
        parser = argparse.ArgumentParser(prog="clixdev", description="Clix.dev command line tool.")
        parser.add_argument('action', choices=['generate', 'sync'])
        parser.add_argument('terminal_token', type=str)
        parser.add_argument('project_token', type=str)
        parser.add_argument('-dir', type=str, required=False)
        args = parser.parse_args()

        if args.action == 'generate':
            from .commands import generate
            return generate(args.terminal_token, args.project_token, args.dir)

        if args.action == 'sync':
            from .commands import sync
            return sync(args.terminal_token, args.project_token, args.dir)
        
        return False
    except Exception as e:
        print(e)
        return False