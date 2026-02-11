from abc import ABC, abstractmethod
import argparse

class BaseCommand(ABC):
    @property
    @abstractmethod
    def name(self):
        """The name of the subcommand."""
        pass

    @property
    @abstractmethod
    def help(self):
        """Help string for the subcommand."""
        pass

    @abstractmethod
    def add_arguments(self, parser: argparse.ArgumentParser):
        """Method to add arguments to the parser."""
        pass

    @abstractmethod
    def run(self, args):
        """The main execution method for the command."""
        pass

    @classmethod
    def setup(cls, subparsers):
        """Setup method to be called from main.py"""
        instance = cls()
        parser = subparsers.add_parser(instance.name, help=instance.help)
        instance.add_arguments(parser)
        parser.set_defaults(func=instance.run)
