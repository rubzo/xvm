#!/usr/bin/env python

import os, sys, pprint

class X:
    def __init__(self):
        self.stack = list()
        self.variables = dict()
        self.pc_updated = False
        self.pc = 0
        self.running = True
        self.insns = list()
        self.equal = False

def load(x, v):
    x.stack.append(v)

def concat_string(x, v):
    if len(x.stack) == 0:
        x.stack.append(v)
    else:
        x.stack[-1] = (x.stack[-1] + v)

def duplicate(x, v):
    x.stack.append(x.stack[-1])

def read(x, v):
    if v not in x.variables:
        print("ERROR: No var '{}' in variables!".format(v))
    else:
        x.stack.append(x.variables[v])

def write(x, v):
    x.variables[v] = x.stack.pop()

def read_input(x, v):
    result = raw_input()
    x.stack.append(int(result))

def add(x, v):
    a = x.stack.pop()
    b = x.stack.pop()
    x.stack.append(a + b)

def sub(x, v):
    a = x.stack.pop()
    b = x.stack.pop()
    x.stack.append(a - b)

def mul(x, v):
    a = x.stack.pop()
    b = x.stack.pop()
    x.stack.append(a * b)

def print_top(x, v):
    print(x.stack[-1])

def branch(x, v):
    x.pc += v
    x.pc_updated = True

def cond_branch(x, v):
    if x.equal:
        x.pc += v
        x.pc_updated = True
    x.equal = False

def equal(x, v):
    a = x.stack.pop()
    b = x.stack.pop()
    x.equal = (a == b)

def not_equal(x, v):
    a = x.stack.pop()
    b = x.stack.pop()
    x.equal = (a != b)

def null(v):
    return None

opcode_table = {\
  'l': (int, load),
  's': (str, load),
  'S': (str, concat_string),

  'r': (str, read),
  'w': (str, write),

  'i': (null, read_input),

  'd': (null, duplicate),

  '+': (null, add),
  '-': (null, sub),
  '*': (null, mul),

  'b': (lambda s: int(s, 16), branch),
  'B': (lambda s: -int(s, 16), branch),

  'c': (lambda s: int(s, 16), cond_branch),
  'C': (lambda s: -int(s, 16), cond_branch),

  'e': (null, equal),
  'E': (null, not_equal),

  'p': (null, print_top)
}


def parse_insn(insn):
    global opcode_table
    return (insn[0], opcode_table[insn[0]][0](insn[1]))


def parse(code):
    insns = list()
    i = 0
    while i < len(code):
        insns.append(parse_insn(code[i:i+2]))
        i += 2
    return insns


def run(x):
    global opcode_table
    while x.running:
        (o, v) = x.insns[x.pc]
        opcode_table[o][1](x, v)
        if not x.pc_updated:
            x.pc += 1
        else:
            x.pc_updated = False
        if x.pc >= len(x.insns):
            x.running = False

x = X()

with open(sys.argv[1], "r") as fh:
    code = fh.read().replace("\n", "")
    x.insns = parse(code)
    run(x)
