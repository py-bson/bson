from bson import dumps, loads
from random import randint
from unittest import TestCase
import os


def populate(parent, howmany, max_children):
    to_add = howmany
    if howmany > max_children:
        children = randint(2, max_children)
        distribution = []
        for i in xrange(0, children - 1):
            distribution.append(int(howmany / children))
        distribution.append(howmany - sum(distribution, 0))
        for i in xrange(0, children):
            steal_target = randint(0, children - 1)
            while steal_target == i:
                steal_target = randint(0, children -1)
            steal_count = randint(-1 * distribution[i],
                    distribution[steal_target]) / 2
            distribution[i] += steal_count
            distribution[steal_target] -= steal_count

        for i in xrange(0, children):
            make_dict = randint(0, 1)
            baby = None
            if make_dict:
                baby = {}
            else:
                baby = []
            populate(baby, distribution[i], max_children)
            if isinstance(parent, dict):
                parent[os.urandom(8).encode("hex")] = baby
            else:
                parent.append(baby)
    else:
        populate_with_leaves(parent, howmany)


def populate_with_leaves(parent, howmany):
    for i in xrange(0, howmany):
        leaf = os.urandom(4).encode("hex")
        make_unicode = randint(0, 1)
        if make_unicode:
            leaf = unicode(leaf)
        if isinstance(parent, dict):
            parent[os.urandom(4).encode("hex")] = leaf
        else:
            parent.append(leaf)


class TestRandomTree(TestCase):
    def test_random_tree(self):
        for i in xrange(0, 16):
            p = {}
            populate(p, 256, 4)
            sp = dumps(p)
            p2 = loads(sp)
            self.assertEquals(p, p2)
