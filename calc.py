"""Milestone 1 calculated values."""

import math

COST_PER_KB = 0.07
PAGE_SIZE = 4096  # 4 KB pages
PT_ENTRIES = 512 * 1024  # 31-bit virtual addresses


def cache_values(p):
    cache_bytes = p.cache_kb * 1024
    blocks = cache_bytes // p.block_size
    rows = blocks // p.assoc

    offset_bits = int(math.log2(p.block_size))
    index_bits = int(math.log2(rows))
    # tag is based on physical memory size
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
    phys_pages = p.phys_mb * 1024 * 1024 // PAGE_SIZE
    system_pages = int(phys_pages * p.os_percent / 100)

    # a page table entry is a valid bit plus the physical page number
    pte_bits = 1 + int(math.log2(phys_pages))
    # one page table per trace
    pt_bytes = PT_ENTRIES * len(p.traces) * pte_bits // 8

    return {
        "phys_pages": phys_pages,
        "system_pages": system_pages,
        "pte_bits": pte_bits,
        "pt_bytes": pt_bytes,
    }
