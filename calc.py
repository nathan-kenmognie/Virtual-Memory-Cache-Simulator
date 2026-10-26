"""Milestone 1 calculated values."""
import math

COST_PER_KB = 0.07


def cache_values(p):
    """Total blocks, tag and index size, rows, overhead, implementation size, cost."""
    cache_bytes = p.cache_kb * 1024
    blocks = cache_bytes // p.block_size
    rows = blocks // p.assoc

    offset_bits = int(math.log2(p.block_size))
    index_bits = int(math.log2(rows))
    # tag is based on the actual physical memory, not the full 32-bit address
    phys_bits = int(math.log2(p.phys_mb * 1024 * 1024))
    tag_bits = phys_bits - index_bits - offset_bits

    # each block stores its tag plus a valid bit
    overhead = (tag_bits + 1) * blocks // 8
    impl_bytes = cache_bytes + overhead
    impl_kb = impl_bytes / 1024

    return {
        "blocks": blocks,
        "tag_bits": tag_bits,
        "index_bits": index_bits,
        "rows": rows,
        "overhead": overhead,
        "impl_bytes": impl_bytes,
        "impl_kb": impl_kb,
        "cost": impl_kb * COST_PER_KB,
    }


def memory_values(p):
    """Physical pages, pages for the system, page table entry size, page table RAM."""
    # TODO
    raise NotImplementedError
