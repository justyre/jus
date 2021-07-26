"""Compare the performance of BST, AVL Tree, and Red-Black Tree."""

import random

from forest import metrics
from forest.binary_trees import avl_tree, binary_search_tree, red_black_tree


insert_data = random.sample(range(1, 2000), 1000)
delete_data = random.sample(insert_data, 1000)

registry = metrics.MetricRegistry()
bstree = binary_search_tree.BinarySearchTree(registry=registry)
avltree = avl_tree.AVLTree(registry=registry)
rbtree = red_black_tree.RBTree(registry=registry)

for key in insert_data:
    bstree.insert(key=key, data=str(key))
    avltree.insert(key=key, data=str(key))
    rbtree.insert(key=key, data=str(key))

for key in delete_data:
    bstree.delete(key=key)
    avltree.delete(key=key)
    rbtree.delete(key=key)

print("Binary Search Tree:")
bst_report = registry.get_metric(name="bst.height").report()
print(f"  Height:  {bst_report}")
print()

print("AVL Tree:")
avlt_rotation_count = registry.get_metric(name="avlt.rotate").count
print(f"  Rotation:  {avlt_rotation_count}")
avlt_report = registry.get_metric(name="avlt.height").report()
print(f"  Height:  {avlt_report}")
print()

print("Red-Black Tree:")
rbt_rotation_count = registry.get_metric(name="rbt.rotate").count
print(f"  Rotation: {rbt_rotation_count}")
rbt_report = registry.get_metric(name="rbt.height").report()
print(f"  Height:  {rbt_report}")

# RESULT ANALYSIS
# 
# 1. The max heights for AVLT and RBT are ~11, and the medium and mean of their heights 
#    are also very close to the max. Also, their percentiles are close to the medium, 
#    and the stdDev is relatively low. So both AVLT and RBT are pretty well balanced.
# 2. On the contrary, BST has a worse max height, and the stdDev of BST is greater.
# 3. As with rotations, AVLT needs more rotations than RBT to keep balanced.