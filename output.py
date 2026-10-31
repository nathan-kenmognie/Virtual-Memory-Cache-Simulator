"""Output formatting."""

import os

from calc import COST_PER_KB
from params import POLICIES

TEAM = 15
COL = 32  # value column


def line(label, value, col=COL):
    print(f"{label:<{col}}{value}")


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
    print("***** Physical Memory Calculated Values *****")
    print()
    line("Number of Physical Pages:", v["phys_pages"])
    line("Number of Pages for System:", v["system_pages"])
    line("Size of Page Table Entry:", f"{v['pte_bits']} bits")
    line("Total RAM for Page Table(s):", f"{v['pt_bytes']} bytes")
    print()


def print_vm_results(p, v):
    # some values start one column further right, as in the spec's sample output
    print("***** VIRTUAL MEMORY SIMULATION RESULTS *****")
    print()
    line("Physical Pages Used By SYSTEM:", v["system_pages"])
    line("Pages Available to User:", v["user_pages"], COL + 1)
    print()
    line("Virtual Pages Mapped:", v["mapped"])
    print("        ------------------------------")
    line("        Page Table Hits:", v["hits"])
    line("        Pages from Free:", v["from_free"], COL + 1)
    line("        Total Page Faults:", v["faults"], COL + 1)
    print()
    print("Page Table Usage Per Process:")
    print("------------------------------")
    for i, (name, pt) in enumerate(zip(p.traces, v["processes"])):
        print(f"[{i}] {os.path.basename(name)}:")
        print(f"        Used Page Table Entries: {pt['used']}  ({pt['percent']:5.2f}%)")
        print(f"        Page Table Wasted: {pt['wasted']} bytes")
        print()
