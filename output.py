"""Printing for each section of the output (spec section 4.3)."""
import os

from calc import COST_PER_KB
from params import POLICIES

TEAM = 15
COL = 32  # values line up in this column


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
    print("***** Cache Calculated Values *****")
    print()
    line("Total # Blocks:", v["blocks"])
    line("Tag Size:", f"{v['tag_bits']} bits")
    line("Index Size:", f"{v['index_bits']} bits")
    line("Total # Rows:", v["rows"])
    line("Overhead Size:", f"{v['overhead']} bytes")
    line("Implementation Memory Size:", f"{v['impl_kb']:.2f} KB  ({v['impl_bytes']} bytes)")
    line("Cost:", f"${v['cost']:.2f} @ ${COST_PER_KB:.2f} per KB")
    print()


def print_memory_values(v):
    # TODO
    raise NotImplementedError
