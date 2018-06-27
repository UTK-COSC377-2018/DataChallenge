import sys
import os

from DataChallenge.JsonParser import JSONParser

import json

def test_creation_str():
    fname = os.path.abspath("./tests/JSON/test1.json")
    parse = JSONParser(fname)
    assert(parse.files == list(fname))
    with open(fname) as f:
        assert(parse[0] == json.load(f)
    return

def test_creation_list():
    fnames = []
    for dirpath, _, filenames in os.walk(os.path.abspath("./tests/JSON")):
        for f in filenames:
            fnames.append(os.path.abspath(os.path.join(dirpath, f)))
    parse = JSONParser(fnames)
    assert(parse.files == fnames)
    for d, f in zip(parse, fnames):
        with open(f) as fo:
            assert(d == json.load(fo))
    return

def test_creation_tuple():
    fnames = []
    for dirpath, _, filenames in os.walk(os.path.abspath("./tests/JSON")):
        for f in filenames:
            fnames.append(os.path.abspath(os.path.join(dirpath, f)))
    fnames = tuple(fnames)
    parse = JSONParser(fnames)
    assert(type(fnames) is list)
    assert(parse.files == fnames)
    for d, f in zip(parse, fnames):
        with open(f) as fo:
            assert(d == json.load(fo))
    return

def test_addJSON_str():
    fname = os.path.abspath("./tests/JSON/test1.json")
    parse = JSONParser()
    parse.addJSON(fname)
    assert(parse.files == list(fname))
    with open(fname) as f:
        assert(parse[0] == json.load(f))
    return

def test_addJSON_list():
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
    return

def test_addJSON_tuple():
    fnames = []
    for dirpath, _, filenames in os.walk(os.path.abspath("./tests/JSON")):
        for f in filenames:
            fnames.append(os.path.abspath(os.path.join(dirpath, f)))
    fnames = tuple(fnames)
    parse = JSONParser()
    parse.addJSON(fnames)
    assert(type(fnames) is list)
    assert(parse.files == fnames)
    for d, f in zip(parse, fnames):
        with open(f) as fo:
            assert(d == json.load(fo))
    return

def test_getitem():
    fname = os.path.abspath("./tests/JSON/test1.json")
    parse = JSONParser(fname)
    with open(fname) as f:
        assert(parse[0] == json.load(f)
    return

def test_len():
    fnames = []
    for dirpath, _, filenames in os.walk(os.path.abspath("./tests/JSON")):
        for f in filenames:
            fnames.append(os.path.abspath(os.path.join(dirpath, f)))
    parse = JSONParser(fnames)
    assert(len(parse) == len(fnames))
    return

def test_contains():
    fname = os.path.abspath("./tests/JSON/test1.json")
    parse = JSONParser(fname)
    assert("Course" in parse)
    assert(not ("COSC377" in parse))
    return
