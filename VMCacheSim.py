"""Virtual Memory & Cache Simulator
CS 3853 Computer Architecture - Team 15

Usage:
    python VMCacheSim.py -s 512 -b 16 -a 4 -r rr -p 1024 -n 100 -u 75 -f Trace1.trc [-f ...]
"""
from params import parse_args
from calc import cache_values, memory_values
from output import (
    print_header,
    print_inputs,
    print_cache_values,
    print_memory_values,
    print_vm_results,
)
from vm import simulate


def main(argv=None):
    p = parse_args(argv)

    # Milestone 1: input parameters and calculated values
    print_header(p)
    print_inputs(p)
    print_cache_values(cache_values(p))
    print_memory_values(memory_values(p))

    # Milestone 2: virtual memory simulation
    print_vm_results(p, simulate(p))

    # Milestone 3: cache simulation


if __name__ == "__main__":
    main()
