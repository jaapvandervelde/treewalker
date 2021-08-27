from treewalker import TreeWalker

with TreeWalker('test.sqlite') as tree_walker:
    tree_walker.walk('data')
