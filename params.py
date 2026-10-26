"""Command line parsing for the simulator."""
import argparse

CACHE_SIZES = [8 * 2**i for i in range(11)]      # 8 KB to 8192 KB
BLOCK_SIZES = [8, 16, 32, 64]
ASSOCIATIVITIES = [1, 2, 4, 8, 16]
POLICIES = {"RR": "Round Robin", "RND": "Random"}
MEMORY_SIZES = [128 * 2**i for i in range(6)]    # 128 MB to 4096 MB


def parse_args(argv=None):
    parser = argparse.ArgumentParser(prog="VMCacheSim",
                                     description="Virtual memory and cache simulator")
    parser.add_argument("-s", dest="cache_kb", type=int, required=True,
                        choices=CACHE_SIZES, metavar="KB",
                        help="cache size in KB (8 to 8192, powers of 2)")
    parser.add_argument("-b", dest="block_size", type=int, required=True,
                        choices=BLOCK_SIZES, metavar="BYTES",
                        help="block size in bytes (8, 16, 32, 64)")
    parser.add_argument("-a", dest="assoc", type=int, required=True,
                        choices=ASSOCIATIVITIES, metavar="WAYS",
                        help="associativity (1, 2, 4, 8, 16)")
    parser.add_argument("-r", dest="policy", type=str.upper, required=True,
                        choices=list(POLICIES), metavar="POLICY",
                        help="replacement policy (RR or RND)")
    parser.add_argument("-p", dest="phys_mb", type=int, required=True,
                        choices=MEMORY_SIZES, metavar="MB",
                        help="physical memory in MB (128 to 4096, powers of 2)")
    parser.add_argument("-u", dest="os_percent", type=float, required=True,
                        metavar="PCT",
                        help="percent of physical memory used by the OS (0 to 100)")
    parser.add_argument("-n", dest="time_slice", type=int, required=True,
                        metavar="N",
                        help="instructions per time slice (-1 for max)")
    parser.add_argument("-f", dest="traces", action="append", required=True,
                        metavar="FILE",
                        help="trace file, one -f per file (1 to 3 files)")
    args = parser.parse_args(argv)

    # TODO: input checks - -u in 0..100, -n is -1 or >= 1, 1 to 3 trace files,
    #       trace files exist, cache smaller than physical memory
    return args
