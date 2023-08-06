import argparse
import pathlib
import os


class ResolveDirectoryAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values is None:
            return

        current_path = pathlib.Path(os.getcwd())
        current_path = current_path.joinpath(values).resolve()
        setattr(namespace, self.dest, str(current_path))
