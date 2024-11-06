#!/usr/bin/env python
from unittest import TestCase

from bson import dumps, loads


class TestBinary(TestCase):
    def setUp(self):
        lyrics = b"""
        I've Had Enough - Earth Wind and Fire

        Getting down, there's
        a party in motion
        Everybody's on the scene
        And I can hear the sound, like the roar of the ocean
        As it rushes to the stream

        Live it up, don't ya hear people screaming
        Gotta do it all their way
        Until they burn it up and the lights nowhere gleaming
        What a price you have to pay

        Why do we feel whe have to feed the fire
        We're only caught up in our desire, ooh

        I've had enough, it's just too tough
        To keep it up, so I am calling out to you
        To lift us up, the world is rough
        I am so tired and I've had enough

        Spinning' round in perpetual motion
        Like a crystal ball of dreams
        And moving in the crowd, there's a hint of a notion
        That you never will be seen

        Slow it down, feel some emotion
        'Cause there's nothing in between
        Reaching that higher ground, but your faith and devotion
        To be on the winning team

        Why do we feel we have to feed the fire
        We're only caught up in our own desire, ooh

        I've had enough, it's just too tough
        To keep it up, so I am calling out to you
        To lift us up, the world is rough
        I am so tired and I've had enough
        """.strip().split(b"\n")
        self.doc = {"lyrics": lyrics}

    def test_binary(self):
        dump = dumps(self.doc)
        decoded = loads(dump)
        self.assertEqual(decoded, self.doc)

    def test_utf8_binary(self):
        self.doc[u"\N{SNOWMAN}"] = u"\N{SNOWMAN WITHOUT SNOW}"
        self.test_binary()
