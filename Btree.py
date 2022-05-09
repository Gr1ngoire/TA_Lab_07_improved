class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.child = []


class BTree:
    def __init__(self, order):
        self.root = BTreeNode(True)
        self.order = order

    def insert(self, data):
        root = self.root
        if len(root.keys) == (2 * self.order) - 1:
            new_el = BTreeNode()
            self.root = new_el
            new_el.child.insert(0, root)
            self.split_child(new_el, 0)
            self.insert_non_full(new_el, data)
        else:
            self.insert_non_full(root, data)

    def insert_non_full(self, node, data):
        index = len(node.keys) - 1
        if node.leaf:
            node.keys.append((None, None))
            while index >= 0 and data < node.keys[index]:
                node.keys[index + 1] = node.keys[index]
                index -= 1
            node.keys[index + 1] = data
        else:
            while index >= 0 and data < node.keys[index]:
                index -= 1
            index += 1
            if len(node.child[index].keys) == (2 * self.order) - 1:
                self.split_child(node, index)
                if data > node.keys[index]:
                    index += 1
            self.insert_non_full(node.child[index], data)

    def split_child(self, node, index):
        order = self.order
        specific_child = node.child[index]
        new_node = BTreeNode(specific_child.leaf)
        node.child.insert(index + 1, new_node)
        node.keys.insert(index, specific_child.keys[order - 1])
        new_node.keys = specific_child.keys[order: (2 * order) - 1]
        specific_child.keys = specific_child.keys[0: order - 1]
        if not specific_child.leaf:
            new_node.child = specific_child.child[order: 2 * order]
            specific_child.child = specific_child.child[0: order - 1]

    def delete(self, node, data):
        order = self.order
        index = 0
        while index < len(node.keys) and data > node.keys[index]:
            index += 1
        if node.leaf:
            if index < len(node.keys) and node.keys[index] == data:
                node.keys.pop(index)
                return
            return

        if index < len(node.keys) and node.keys[index] == data:
            return self.delete_internal_node(node, data, index)
        elif len(node.child[index].keys) >= order:
            self.delete(node.child[index], data)
        else:
            if index != 0 and index + 2 < len(node.child):
                if len(node.child[index - 1].keys) >= order:
                    self.delete_sibling(node, index, index - 1)
                elif len(node.child[index + 1].keys) >= order:
                    self.delete_sibling(node, index, index + 1)
                else:
                    self.delete_merge(node, index, index + 1)
            elif index == 0:
                if len(node.child[index + 1].keys) >= order:
                    self.delete_sibling(node, index, index + 1)
                else:
                    self.delete_merge(node, index, index + 1)
            elif index + 1 == len(node.child):
                if len(node.child[index - 1].keys) >= order:
                    self.delete_sibling(node, index, index - 1)
                else:
                    self.delete_merge(node, index, index - 1)
            self.delete(node.child[index], data)

    def delete_internal_node(self, node, data, index):
        order = self.order
        if node.leaf:
            if node.keys[index] == data:
                node.keys.pop(index)
                return
            return

        if len(node.child[index].keys) >= order:
            node.keys[index] = self.delete_predecessor(node.child[index])
            return
        elif len(node.child[index + 1].keys) >= order:
            node.keys[index] = self.delete_successor(node.child[index + 1])
            return
        else:
            self.delete_merge(node, index, index + 1)
            self.delete_internal_node(node.child[index], data, self.order - 1)

    def delete_predecessor(self, node):
        if node.leaf:
            return node.pop()
        n = len(node.keys) - 1
        if len(node.child[n].keys) >= self.order:
            self.delete_sibling(node, n + 1, n)
        else:
            self.delete_merge(node, n, n + 1)
        self.delete_predecessor(node.child[n])

    def delete_successor(self, node):
        if node.leaf:
            return node.keys.pop(0)
        if len(node.child[1].keys) >= self.order:
            self.delete_sibling(node, 0, 1)
        else:
            self.delete_merge(node, 0, 1)
        self.delete_successor(node.child[0])

    def delete_merge(self, node, index, j):
        cnode = node.child[index]

        if j > index:
            rsnode = node.child[j]
            cnode.keys.append(node.keys[index])
            for k in range(len(rsnode.keys)):
                cnode.keys.append(rsnode.keys[k])
                if len(rsnode.child) > 0:
                    cnode.child.append(rsnode.child[k])
            if len(rsnode.child) > 0:
                cnode.child.append(rsnode.child.pop())
            new = cnode
            node.keys.pop(index)
            node.child.pop(j)
        else:
            lsnode = node.child[j]
            lsnode.keys.append(node.keys[j])
            for index in range(len(cnode.keys)):
                lsnode.keys.append(cnode.keys[index])
                if len(lsnode.child) > 0:
                    lsnode.child.append(cnode.child[index])
            if len(lsnode.child) > 0:
                lsnode.child.append(cnode.child.pop())
            new = lsnode
            node.keys.pop(j)
            node.child.pop(index)

        if node == self.root and len(node.keys) == 0:
            self.root = new

    def delete_sibling(self, nodex, index, j):
        cnode = nodex.child[index]
        if index < j:
            rsnode = nodex.child[j]
            cnode.keys.append(nodex.keys[index])
            nodex.keys[index] = rsnode.keys[0]
            if len(rsnode.child) > 0:
                cnode.child.append(rsnode.child[0])
                rsnode.child.pop(0)
            rsnode.keys.pop(0)
        else:
            lsnode = nodex.child[j]
            cnode.keys.insert(0, nodex.keys[index - 1])
            nodex.keys[index - 1] = lsnode.keys.pop()
            if len(lsnode.child) > 0:
                cnode.child.insert(0, lsnode.child.pop())

    def print_tree(self, node, level=0):
        print("Level ", level, end=":")
        for i in node.keys:
            print(i, end=" ")
        print()
        level += 1
        if len(node.child) > 0:
            for i in node.child:
                self.print_tree(i, level)

    def contains(self, data, node=None):
        if node is not None:
            i = 0
            while i < len(node.keys) and data > node.keys[i]:
                i += 1
            if i < len(node.keys) and data == node.keys[i]:
                return True
            elif node.leaf:
                return False
            else:
                return self.contains(data, node.child[i])

        else:
            return self.contains(data, self.root)