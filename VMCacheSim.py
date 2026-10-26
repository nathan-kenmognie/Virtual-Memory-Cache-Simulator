"""Virtual Memory & Cache Simulator
CS 3853 Computer Architecture - Team 15

Usage:
    python VMCacheSim.py -s 512 -b 16 -a 4 -r rr -p 1024 -n 100 -u 75 -f Trace1.trc [-f ...]
"""
from params import parse_args
from output import print_header, print_inputs


def main(argv=None):
    p = parse_args(argv)

    # Milestone 1: input parameters and calculated values
    print_header(p)
    print_inputs(p)
    # TODO: cache calculated values (calc.cache_values -> output.print_cache_values)
    # TODO: physical memory calculated values (calc.memory_values -> output.print_memory_values)

    # Milestone 2: virtual memory simulation
    # Milestone 3: cache simulation


if __name__ == "__main__":
    main()
