# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Entry point for the Forest CLI application."""

from forest.bin import tree_cli

if __name__ == "__main__":
    tree_cli.cli().cmdloop()