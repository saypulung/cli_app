import argparse
from commands.cmd_1 import Command1
from commands.cmd_2 import Command2
from commands.cmd_3 import Command3

def main():
    parser = argparse.ArgumentParser(description="CLI Tool")
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

    # Register subcommands using the class method
    Command1.setup(subparsers)
    Command2.setup(subparsers)
    Command3.setup(subparsers)

    args = parser.parse_args()
    
    # Execute the selected command function
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
