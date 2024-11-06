#!/usr/bin/env python
from unittest import TestCase

from bson import dumps, loads
from six import PY3


class TestArray(TestCase):
    def setUp(self):
        lyrics = u"""
        Viva La Vida lyrics

        I used to rule the world
        Seas would rise when I gave the word
        Now in the morning I sleep alone
        Sweep the streets I used to own

        I used to roll the dice
        Feel the fear in my enemy's eyes
        Listen as the crowd would sing
        "Now the old king is dead! Long live the king!"

        One minute I held the key
        Next the walls were closed on me
        And I discovered that my castles stand
        Upon pillars of salt and pillars of sand

        I hear Jerusalem bells a ringing
        Roman Cavalry choirs are singing
        Be my mirror, my sword and shield
        My missionaries in a foreign field

        For some reason I can't explain
        Once you go there was never
        Never an honest word
        And that was when I ruled the world

        It was the wicked and wild wind
        Blew down the doors to let me in
        Shattered windows and the sound of drums
        People couldn't believe what I'd become

        Revolutionaries wait
        For my head on a silver plate
        Just a puppet on a lonely string
        Oh who would ever want to be king?

        I hear Jerusalem bells a ringing
        Roman Cavalry choirs are singing
        Be my mirror, my sword and shield
        My missionaries in a foreign field

        For some reason I can't explain
        I know Saint Peter won't call my name
        Never an honest word
        But that was when I ruled the world

        I hear Jerusalem bells a ringing
        Roman Cavalry choirs are singing
        Be my mirror, my sword and shield
        My missionaries in a foreign field

        For some reason I can't explain
        I know Saint Peter won't call my name
        Never an honest word
        But that was when I ruled the world
        """.strip().split(u"\n")
        self.doc = {u"lyrics": lyrics}

    def test_long_array(self):
        serialized = dumps(self.doc)
        doc2 = loads(serialized)
        self.assertEqual(self.doc, doc2)

    def test_encoded_order(self):
        serialized = dumps(self.doc)
        expected = repr(serialized)[1:] if PY3 else repr(serialized)
        self.assertEqual(expected, '\'\\xea\\x08\\x00\\x00\\x04lyrics\\x00\\xdd\\x08\\x00\\x00\\x020\\x00\\x14\\x00\\x00\\x00Viva La Vida lyrics\\x00\\x021\\x00\\x01\\x00\\x00\\x00\\x00\\x022\\x00!\\x00\\x00\\x00        I used to rule the world\\x00\\x023\\x00-\\x00\\x00\\x00        Seas would rise when I gave the word\\x00\\x024\\x00)\\x00\\x00\\x00        Now in the morning I sleep alone\\x00\\x025\\x00(\\x00\\x00\\x00        Sweep the streets I used to own\\x00\\x026\\x00\\x01\\x00\\x00\\x00\\x00\\x027\\x00 \\x00\\x00\\x00        I used to roll the dice\\x00\\x028\\x00)\\x00\\x00\\x00        Feel the fear in my enemy\\\'s eyes\\x00\\x029\\x00\\\'\\x00\\x00\\x00        Listen as the crowd would sing\\x00\\x0210\\x008\\x00\\x00\\x00        "Now the old king is dead! Long live the king!"\\x00\\x0211\\x00\\x01\\x00\\x00\\x00\\x00\\x0212\\x00"\\x00\\x00\\x00        One minute I held the key\\x00\\x0213\\x00)\\x00\\x00\\x00        Next the walls were closed on me\\x00\\x0214\\x00/\\x00\\x00\\x00        And I discovered that my castles stand\\x00\\x0215\\x001\\x00\\x00\\x00        Upon pillars of salt and pillars of sand\\x00\\x0216\\x00\\x01\\x00\\x00\\x00\\x00\\x0217\\x00)\\x00\\x00\\x00        I hear Jerusalem bells a ringing\\x00\\x0218\\x00)\\x00\\x00\\x00        Roman Cavalry choirs are singing\\x00\\x0219\\x00*\\x00\\x00\\x00        Be my mirror, my sword and shield\\x00\\x0220\\x00+\\x00\\x00\\x00        My missionaries in a foreign field\\x00\\x0221\\x00\\x01\\x00\\x00\\x00\\x00\\x0222\\x00(\\x00\\x00\\x00        For some reason I can\\\'t explain\\x00\\x0223\\x00$\\x00\\x00\\x00        Once you go there was never\\x00\\x0224\\x00\\x1d\\x00\\x00\\x00        Never an honest word\\x00\\x0225\\x00,\\x00\\x00\\x00        And that was when I ruled the world\\x00\\x0226\\x00\\x01\\x00\\x00\\x00\\x00\\x0227\\x00(\\x00\\x00\\x00        It was the wicked and wild wind\\x00\\x0228\\x00)\\x00\\x00\\x00        Blew down the doors to let me in\\x00\\x0229\\x001\\x00\\x00\\x00        Shattered windows and the sound of drums\\x00\\x0230\\x000\\x00\\x00\\x00        People couldn\\\'t believe what I\\\'d become\\x00\\x0231\\x00\\x01\\x00\\x00\\x00\\x00\\x0232\\x00\\x1d\\x00\\x00\\x00        Revolutionaries wait\\x00\\x0233\\x00&\\x00\\x00\\x00        For my head on a silver plate\\x00\\x0234\\x00)\\x00\\x00\\x00        Just a puppet on a lonely string\\x00\\x0235\\x00+\\x00\\x00\\x00        Oh who would ever want to be king?\\x00\\x0236\\x00\\x01\\x00\\x00\\x00\\x00\\x0237\\x00)\\x00\\x00\\x00        I hear Jerusalem bells a ringing\\x00\\x0238\\x00)\\x00\\x00\\x00        Roman Cavalry choirs are singing\\x00\\x0239\\x00*\\x00\\x00\\x00        Be my mirror, my sword and shield\\x00\\x0240\\x00+\\x00\\x00\\x00        My missionaries in a foreign field\\x00\\x0241\\x00\\x01\\x00\\x00\\x00\\x00\\x0242\\x00(\\x00\\x00\\x00        For some reason I can\\\'t explain\\x00\\x0243\\x00.\\x00\\x00\\x00        I know Saint Peter won\\\'t call my name\\x00\\x0244\\x00\\x1d\\x00\\x00\\x00        Never an honest word\\x00\\x0245\\x00,\\x00\\x00\\x00        But that was when I ruled the world\\x00\\x0246\\x00\\x01\\x00\\x00\\x00\\x00\\x0247\\x00)\\x00\\x00\\x00        I hear Jerusalem bells a ringing\\x00\\x0248\\x00)\\x00\\x00\\x00        Roman Cavalry choirs are singing\\x00\\x0249\\x00*\\x00\\x00\\x00        Be my mirror, my sword and shield\\x00\\x0250\\x00+\\x00\\x00\\x00        My missionaries in a foreign field\\x00\\x0251\\x00\\x01\\x00\\x00\\x00\\x00\\x0252\\x00(\\x00\\x00\\x00        For some reason I can\\\'t explain\\x00\\x0253\\x00.\\x00\\x00\\x00        I know Saint Peter won\\\'t call my name\\x00\\x0254\\x00\\x1d\\x00\\x00\\x00        Never an honest word\\x00\\x0255\\x00,\\x00\\x00\\x00        But that was when I ruled the world\\x00\\x00\\x00\'')
