bson
====


Independent BSON codec for Python that doesn't depend on MongoDB.


Installation
------------

.. sourcecode:: bash

   ~ $ python setup.py install

or can use pip

.. sourcecode:: bash

   ~ $ pip install bson


Quick start
-----------

.. sourcecode:: python

   >>> import bson
   >>> a = bson.dumps({"A":[1,2,3,4,5,"6", u"7", {"C":u"DS"}]})
   >>> b = bson.loads(a)
   >>> b
   {'A': [1, 2, 3, 4, 5, '6', u'7', {'C': u'DS'}]}


Sending and receiving BSON objects to and from network sockets.


.. sourcecode:: python

   >>> from gevent import monkey, socket
   >>> monkey.patch_all()
   >>>
   >>> import bson
   >>> bson.patch_socket()
   >>> s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   >>> s.connect(("127.0.0.1", 12345))
   >>> s.sendobj({u"message" : "hello!"})
