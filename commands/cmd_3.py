from .base import BaseCommand
import argparse

class Command3(BaseCommand):
    @property
    def name(self):
        return 'cmd-3'

    @property
    def help(self):
        return 'Advanced processing to tag something'

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument('--id', type=str, required=True, help='ID of the item to tag')
        parser.add_argument('--tags', type=str, nargs='+', required=True, help='List of tags')

    def run(self, args):
        print(f"Tagging item ID: {args.id}")
        print(f"Tags: {', '.join(args.tags)}")
