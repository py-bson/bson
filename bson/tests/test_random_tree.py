import os
from binascii import hexlify
from random import randint
from unittest import TestCase

from six import text_type, PY3
from six.moves import xrange

from bson import dumps, loads


def populate(parent, howmany, max_children):
    if howmany > max_children:
        children = randint(2, max_children)
        distribution = []
        for _ in xrange(0, children - 1):
            distribution.append(int(howmany / children))
        distribution.append(howmany - sum(distribution, 0))
        for i in xrange(0, children):
            steal_target = randint(0, children - 1)
            while steal_target == i:
                steal_target = randint(0, children -1)
            steal_count = int(randint(-1 * distribution[i],
                    distribution[steal_target]) / 2)
            distribution[i] += steal_count
            distribution[steal_target] -= steal_count

        for i in xrange(0, children):
            make_dict = randint(0, 1)
            if make_dict:
                baby = {}
            else:
                baby = []
            populate(baby, distribution[i], max_children)
            if isinstance(parent, dict):
                key = os.urandom(8)
                key = "".join(chr(c) for c in hexlify(key)) if PY3 else key.encode("hex")
                parent[key] = baby
            else:
                parent.append(baby)
    else:
        populate_with_leaves(parent, howmany)


def populate_with_leaves(parent, howmany):
    for _ in xrange(0, howmany):
        leaf = os.urandom(4)
        leaf = "".join(chr(c) for c in hexlify(leaf)) if PY3 else leaf.encode("hex")
        make_unicode = randint(0, 1)
        if make_unicode:
            leaf = text_type(leaf)
        if isinstance(parent, dict):
            key = os.urandom(4)
            key = "".join(chr(c) for c in hexlify(key)) if PY3 else key.encode("hex")
            parent[key] = leaf
        else:
            parent.append(leaf)


class TestRandomTree(TestCase):
    def test_random_tree(self):
        for _ in xrange(0, 16):
            p = {}
            populate(p, 256, 4)
            sp = dumps(p)
            p2 = loads(sp)
            self.assertEquals(p, p2)
