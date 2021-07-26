# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""A simple CLI application."""

import cmd
from typing import Optional

from forest import tree_exceptions
from forest.binary_trees import avl_tree
from forest.binary_trees import binary_search_tree
from forest.binary_trees import binary_tree
from forest.binary_trees import red_black_tree
from forest.binary_trees import single_threaded_binary_trees
from forest.binary_trees import double_threaded_binary_trees
from forest.binary_trees import traversal


class cli(cmd.Cmd):
    """A CLI for operating tree data structures."""
    
    intro = "Welcome to the Tree CLI. Type help or ? to list available commands.\n"
    prompt = "tree> "
    
    def __init__(self) -> None:
        cmd.Cmd.__init__(self)
        self._tree: Optional[binary_tree.BinaryTree] = None
    
    def do_build(self, line):
        """Build a binary tree.
        
        Options: avl, bst, rb, threaded
        
        Example
        -------
        tree> build avl
        """
        try:
            if self._tree is not None:
                print(f"ERROR: A tree of type {type(self._tree)} already exists.")
                return
            
            tree_type = self._get_single_arg(line=line).lower()
            if tree_type == "avl":
                self._tree = avl_tree.AVLTree()
            elif tree_type == "bst":
                self._tree == binary_search_tree.BinarySearchTree()
            elif tree_type == "rb":
                self._tree == red_black_tree.RBTree()
            elif tree_type == "threaded":
                threaded_type = input(
                    "Please input threaded BST type (left, right, double): "
                ).lower()
                if threaded_type == "left":
                    self._tree = single_threaded_binary_trees.LeftThreadedBinaryTree()
                elif threaded_type == "right":
                    self._tree = single_threaded_binary_trees.RightThreadedBinaryTree()
                elif threaded_type == "double":
                    self._tree = double_threaded_binary_trees.DoubleThreadedBinaryTree()
                else:
                    print(f"ERROR: {threaded_type} is an invalid threaded type.")
            else:
                print(f"ERROR: {tree_type} is an invalid tree type.")
        except KeyError as error:
            print(error)
        
    def do_search(self, line):
        """Search data by a given key.
        
        Example
        -------
        tree> search 3
        """
        try:
            key = self._get_key(line=line)
            output = self._tree.search(key=key)
            if output is None:
                print(f"ERROR: A node with key {key} does not exist.")
            else:
                print(output.key, output.data)
        except KeyError as error:
            print(error)
    
    def do_insert(self, line):
        """Insert a (key, data) pair. The key must be an integer.
        
        Example
        -------
        tree> insert 7 data
        """
        args = line.split()
        # Note: the `insert` is not included in `args`.
        if len(args) != 2:
            print("ERROR: Invalid number of arguments: Two expected.")
            return
        try:
            key = self._get_key(line=line)
            self._tree.insert(key=key, data=args[1])
            print(f"(key, data) = ({args[0]}, {args[1]}) has been inserted.")
        except tree_exceptions.DuplicateKeyError:
            print(f"ERROR: A node with {key} already exists.")
        except KeyError as error:
            print(error)
    
    def do_delete(self, line):
        """Delete an item by the given key.
        
        Example
        -------
        tree> delete 5
        """
        try:
            key = self._get_key(line=line)
            self._tree.delete(key=key)
            print(f"Key {key} has been removed.")
        except KeyError as error:
            print(error)
    
    def do_traverse(self, line):
        """Traverse the binary tree.
        
        Options: pre, in, post, reverse
        
        Example
        -------
        tree> traverse pre
        """
        try:
            arg = self._get_single_arg(line=line).lower()
            
            if isinstance(
                self._tree, single_threaded_binary_trees.LeftThreadedBinaryTree
            ):
                if arg == "reverse":
                    for item in self._tree.reverse_inorder_traverse():
                        print(item)
                else:
                    print(f"ERROR: {arg} is an invalid traversal type for this tree.")
            elif isinstance(
                self._tree, single_threaded_binary_trees.RightThreadedBinaryTree
            ):
                if arg == "pre":
                    for item in self._tree.preorder_traverse():
                        print(item)
                elif arg == "in":
                    for item in self._tree.inorder_traverse():
                        print(item)
                else:
                    print(f"ERROR: {arg} is an invalid traversal type for this tree.")
            elif isinstance(
                self._tree, double_threaded_binary_trees.DoubleThreadedBinaryTree
            ):
                if arg == "pre":
                    for item in self._tree.preorder_traverse():
                        print(item)
                elif arg == "in":
                    for item in self._tree.inorder_traverse():
                        print(item)
                elif arg == "reverse":
                    for item in self._tree.reverse_inorder_traverse():
                        print(item)
                else:
                    print(f"ERROR: {arg} is an invalid traversal type for this tree.")
            elif isinstance(self._tree, red_black_tree.RBTree):
                if arg == "pre":
                    for item in self._tree.preorder_traverse():
                        print(item)
                elif arg == "in":
                    for item in self._tree.inorder_traverse():
                        print(item)
                elif arg == "post":
                    for item in self._tree.postorder_traverse():
                        print(item)
                else:
                    print(f"ERROR: {arg} is an invalid traversal type for this tree.")
            else:
                # For avl and bst
                if arg == "pre":
                    for item in traversal.preorder_traverse(tree=self._tree):
                        print(item)
                elif arg == "in":
                    for item in traversal.inorder_traverse(tree=self._tree):
                        print(item)
                elif arg == "post":
                    for item in traversal.postorder_traverse(tree=self._tree):
                        print(item)
                elif arg == "reverse":
                    for item in traversal.reverse_inorder_traverse(tree=self._tree):
                        print(item)
                else:
                    print(f"ERROR: {arg} is an invalid traversal type.")
        except KeyError as error:
            print(error)
    
    def do_display(self, line):
        """Display the tree."""
        if isinstance(self._tree.root, binary_tree.Node):
            if isinstance(
                self._tree, single_threaded_binary_trees.LeftThreadedBinaryTree
            ) or isinstance(
                self._tree, single_threaded_binary_trees.RightThreadedBinaryTree
            ) or isinstance(
                self._tree, double_threaded_binary_trees.DoubleThreadedBinaryTree
            ):
                self._tree.root.display_keys(self._tree)
            else:
                self._tree.root.display_keys()
    
    def do_destroy(self, line):
        """Destroy the existing tree."""
        self._tree = None
        print("The tree has been destroyed.")
        
    def do_exit(self, line):
        """Exit the application."""
        print("Bye!")
        raise SystemExit()                
    
    def _get_single_arg(self, line):
        # Get only the only argument from the line of input.
        arg = line.split()
        if len(arg) > 1:
            raise KeyError("Too many arguments! Only one expected.")
        return arg[0]
    
    def _get_key(self, line):
        # Get the key of a node from the line of input.
        arg = line.split()
        if len(arg) == 0:
            raise KeyError("ERROR: No argument provided!")
        # str.isdigit() checks if str is made ONLY of digits
        if not arg[0].isdigit():
            raise KeyError("ERROR: The key must be an integer!")
        else:
            return int(arg[0])


def main():
    """Entry point for the tree CLI."""
    cli().cmdloop()