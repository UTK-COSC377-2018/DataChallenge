import sys
import os

from DataChallenge.JsonParser import JSONParser

import json

def test_creationStr():
    fname = os.path.abspath("./tests/JSON/test1.json")
    parse = JSONParser(fname)
    assert(parse.files == [fname])
    f = open(fname)
    assert(parse[0] == json.load(f))

def test_creationList():
    fnames = []
    for dirpath, _, filenames in os.walk(os.path.abspath("./tests/JSON")):
        for f in filenames:
            fnames.append(os.path.abspath(os.path.join(dirpath, f)))
    parse = JSONParser(fnames)
    assert(parse.files == fnames)
    for d, f in zip(parse, fnames):
        with open(f) as fo:
            assert(d == json.load(fo))

def test_creationTuple():
    fnames = []
    for dirpath, _, filenames in os.walk(os.path.abspath("./tests/JSON")):
        for f in filenames:
            fnames.append(os.path.abspath(os.path.join(dirpath, f)))
    fnames = tuple(fnames)
    parse = JSONParser(fnames)
    assert(parse.files == list(fnames))
    for d, f in zip(parse, fnames):
        with open(f) as fo:
            assert(d == json.load(fo))

def test_addJSONStr():
    fname = os.path.abspath("./tests/JSON/test1.json")
    parse = JSONParser()
    parse.addJSON(fname)
    assert(parse.files == [fname])
    with open(fname) as f:
        assert(parse[0] == json.load(f))

def test_addJSONList():
    fnames = []
    for dirpath, _, filenames in os.walk(os.path.abspath("./tests/JSON")):
        for f in filenames:
            fnames.append(os.path.abspath(os.path.join(dirpath, f)))
    parse = JSONParser()
    parse.addJSON(fnames)
    assert(parse.files == fnames)
    for d, f in zip(parse, fnames):
        with open(f) as fo:
            assert(d == json.load(fo))

def test_addJSONTuple():
    fnames = []
    for dirpath, _, filenames in os.walk(os.path.abspath("./tests/JSON")):
        for f in filenames:
            fnames.append(os.path.abspath(os.path.join(dirpath, f)))
    fnames = tuple(fnames)
    parse = JSONParser()
    parse.addJSON(fnames)
    assert(parse.files == list(fnames))
    for d, f in zip(parse, fnames):
        with open(f) as fo:
            assert(d == json.load(fo))

def test_addJSONError():
    try:
        parse = JSONParser()
        parse.addJSON(52)
    except TypeError as te:
        assert(True)

def test_getitem():
    fname = os.path.abspath("./tests/JSON/test1.json")
    parse = JSONParser(fname)
    with open(fname) as f:
        assert(parse[0] == json.load(f))

def test_len():
    fnames = []
    for dirpath, _, filenames in os.walk(os.path.abspath("./tests/JSON")):
        for f in filenames:
            fnames.append(os.path.abspath(os.path.join(dirpath, f)))
    parse = JSONParser(fnames)
    assert(len(parse) == len(fnames))

def test_contains():
    fname = os.path.abspath("./tests/JSON/test1.json")
    parse = JSONParser(fname)
    assert("Course" in parse)
    assert(not ("COSC377" in parse))
