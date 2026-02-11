from .base import BaseCommand
import argparse

class Command2(BaseCommand):
    @property
    def name(self):
        return 'cmd-2'

    @property
    def help(self):
        return 'Process something after cmd-1'

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument('--id', type=str, required=True, help='ID to process')
        parser.add_argument('--filter', type=str, choices=['a', 'b'], default='a', help='Filter to apply')

    def run(self, args):
        print(f"Processing something with ID: {args.id}")
        print(f"Applying filter: {args.filter}")
