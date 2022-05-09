from random import randrange
from Btree import BTree

btree = BTree(3)

for i in range(10):
    btree.insert(i)

btree.delete(btree.root, 8)
print(btree.contains(7))
btree.print_tree(btree.root)
