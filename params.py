"""Command line parsing for the simulator."""

import argparse
import os

CACHE_SIZES = [8 * 2**i for i in range(11)]  # 8 KB to 8192 KB
BLOCK_SIZES = [8, 16, 32, 64]
ASSOCIATIVITIES = [1, 2, 4, 8, 16]
POLICIES = {"RR": "Round Robin", "RND": "Random"}
MEMORY_SIZES = [128 * 2**i for i in range(6)]  # 128 MB to 4096 MB


def parse_args(argv=None):
    parser = argparse.ArgumentParser(prog="VMCacheSim")
    parser.add_argument(
        "-s",
        dest="cache_kb",
        type=int,
        required=True,
        choices=CACHE_SIZES,
        metavar="KB",
        help="cache size (KB)",
    )
    parser.add_argument(
        "-b",
        dest="block_size",
        type=int,
        required=True,
        choices=BLOCK_SIZES,
        metavar="BYTES",
        help="block size (bytes)",
    )
    parser.add_argument(
        "-a",
        dest="assoc",
        type=int,
        required=True,
        choices=ASSOCIATIVITIES,
        metavar="WAYS",
        help="associativity",
    )
    parser.add_argument(
        "-r",
        dest="policy",
        type=str.upper,
        required=True,
        choices=list(POLICIES),
        metavar="POLICY",
        help="RR or RND",
    )
    parser.add_argument(
        "-p",
        dest="phys_mb",
        type=int,
        required=True,
        choices=MEMORY_SIZES,
        metavar="MB",
        help="physical memory (MB)",
    )
    parser.add_argument(
        "-u",
        dest="os_percent",
        type=float,
        required=True,
        metavar="PCT",
        help="percent of memory used by the OS",
    )
    parser.add_argument(
        "-n",
        dest="time_slice",
        type=int,
        required=True,
        metavar="N",
        help="instructions per time slice (-1 = max)",
    )
    parser.add_argument(
        "-f",
        dest="traces",
        action="append",
        required=True,
        metavar="FILE",
        help="trace file (up to 3)",
    )
    args = parser.parse_args(argv)

    if not 0 <= args.os_percent <= 100:
        parser.error("-u must be 0 to 100")
    if args.time_slice != -1 and args.time_slice < 1:
        parser.error("-n must be -1 or at least 1")
    if len(args.traces) > 3:
        parser.error("at most 3 trace files")
    for name in args.traces:
        if not os.path.isfile(name):
            parser.error(f"can't open {name}")
    if args.cache_kb * 1024 >= args.phys_mb * 1024 * 1024:
        parser.error("cache must be smaller than physical memory")
    return args
