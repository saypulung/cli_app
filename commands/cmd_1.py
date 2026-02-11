from .base import BaseCommand
import argparse

class Command1(BaseCommand):
    @property
    def name(self):
        return 'cmd-1'

    @property
    def help(self):
        return 'Command 1: Add a something to the system.'

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument('--path', type=str, required=True, help='Path')
        parser.add_argument('--identifier', type=str, default='default', help='Identifier')

    def run(self, args):
        print(f"Adding something from: {args.path}")
        print(f"To ID: {args.identifier}")
