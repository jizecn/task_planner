#!/usr/bin/env python
import json
from StringIO import StringIO

def test():
    json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
    print json.dumps("\"foo\bar")
    print json.dumps(u'\u1234')
    print json.dumps('\\')
    print json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True)
    io = StringIO()
    json.dump(['streaming API'], io)
    io.getvalue()

def decodeSparQLResult(res):
    decres = json.loads(res)
    return decres
