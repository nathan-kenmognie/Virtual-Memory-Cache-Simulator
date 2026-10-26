"""Printing for each section of the output (spec section 4.3)."""
import os

from params import POLICIES

TEAM = 15
COL = 31  # values line up in this column


def line(label, value):
    print(f"{label:<{COL}}{value}")


def print_header(p):
    print(f"Cache Simulator - CS 3853 - Team #{TEAM}")
    print()
    print("Trace File(s):")
    for name in p.traces:
        print(f"        {os.path.basename(name)}")
    print()


def print_inputs(p):
    print("***** Cache Input Parameters *****")
    print()
    line("Cache Size:", f"{p.cache_kb} KB")
    line("Block Size:", f"{p.block_size} bytes")
    line("Associativity:", p.assoc)
    line("Replacement Policy:", POLICIES[p.policy])
    line("Physical Memory:", f"{p.phys_mb} MB")
    line("Percent Memory Used by System:", f"{p.os_percent:.1f}%")
    line("Instructions / Time Slice:", "max" if p.time_slice == -1 else p.time_slice)
    print()


def print_cache_values(v):
    # TODO
    raise NotImplementedError


def print_memory_values(v):
    # TODO
    raise NotImplementedError
