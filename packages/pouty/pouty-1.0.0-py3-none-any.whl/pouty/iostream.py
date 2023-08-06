import sys
import ctypes
from math import *


class ref: #because python doesn't support pass-by-reference
    def __init__(self, value):
        self.value = value
    
    def __getitem__(self, index: Ellipsis):
        if index == ...:
            return self.value
    def __setitem__(self, index: Ellipsis, value: any):
        if index == ...:
            self.value = value

    def __str__(self):
        return str(self.value)

def _cround(number: float, precision: int):
    #round to sig figs
    return round(number, -int(floor(log10(abs(number))))+precision-1)

class modifier_base:
    ...

class cout_base:
    def __init__(self, stream=sys.stdout):
        self.stream = stream
        self.float_precision = 6
    #left shift operator
    def __lshift__(self, other):
        if isinstance(other, modifier_base):
            other(self)
            return self
        elif isinstance(other, float):
            self.stream.write(str(_cround(other, self.float_precision)))
            return self
        else:
            #check if lshift operator is overloaded
            if "is_pouty_stream" in other.__class__.__dict__ and other.__class__.is_pouty_stream:
                other.__lshift__(self)
            else:
                sys.stdout.write(str(other))
            return self

class cin_base:
    def __init__(self, stream=sys.stdin):
        self.stream = stream
    #right shift operator
    def __rshift__(self, other: ref):
        if "is_pouty_stream" in other.__class__.__dict__ and other.__class__.is_pouty_stream:
            other.__rshift__(self)
            return self
        if isinstance(other[...], str):
            other[...] = sys.stdin.readline()
        elif isinstance(other[...], float):
            other[...] = float(sys.stdin.readline())
        elif isinstance(other[...], int):
            other[...] = int(sys.stdin.readline())
        elif hasattr(other[...], "__rshift__"):
            other[...] = other[...].__rshift__(self)
        else:
            raise RuntimeError("Not implemented yet")
        return self

def modifier(function: callable): #e.g. std.endl
    class _modifier(modifier_base):
        def __call__(self, streamer):
            return function(streamer)
    return _modifier()

def nested_modifier(function: callable): #e.g. std.precision()
    def modifier_generator(*args):
        class _modifier(modifier_base):
            def __call__(self, streamer: cout_base):
                return function(streamer, *args)
        return _modifier()
    return modifier_generator
            
class std:
    cout = cout_base(sys.stdout)
    cerr = cout_base(sys.stderr)
    clog = cerr
    cin = cin_base(sys.stdin)

    @modifier
    def endl(streamer):
        streamer.stream.write("\n")
        streamer.stream.flush()
    
    @nested_modifier
    def precision(streamer, precision: int):
        streamer.float_precision = precision

def using_namespace(globals_ref, namespace):
    if namespace == "std":
        for key, value in std.__dict__.items():
            if key[:2] != "__" and key[-2:] != "__":
                globals_ref[key] = value