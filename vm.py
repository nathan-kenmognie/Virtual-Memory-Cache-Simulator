"""Milestone 2 virtual memory simulation."""

from collections import deque

from calc import PAGE_SIZE, PT_ENTRIES, memory_values
from tracefile import read_trace


def simulate(p):
    mem = memory_values(p)
    free = deque(range(mem["system_pages"], mem["phys_pages"]))
    tables = [{} for _ in p.traces]  # virtual page -> physical page
    stats = {"mapped": 0, "hits": 0, "from_free": 0, "faults": 0}

    # TODO: round robin, p.time_slice instructions per turn
    for pid, name in enumerate(p.traces):
        for address, _, data in read_trace(name):
            for a in (address,) + data:
                access(pid, a, tables, free, stats)
        # TODO: free the process's pages when it ends

    stats["system_pages"] = mem["system_pages"]
    stats["user_pages"] = mem["phys_pages"] - mem["system_pages"]
    # TODO: count pages used, not pages still mapped, once pages get freed
    stats["processes"] = [
        {
            "used": len(t),
            "percent": len(t) * 100 / PT_ENTRIES,
            "wasted": (PT_ENTRIES - len(t)) * mem["pte_bits"] // 8,
        }
        for t in tables
    ]
    return stats


def access(pid, address, tables, free, stats):
    stats["mapped"] += 1
    vpn = (address & 0x7FFFFFFF) // PAGE_SIZE
    table = tables[pid]
    if vpn in table:
        stats["hits"] += 1
    elif free:
        stats["from_free"] += 1
        table[vpn] = free.popleft()
    else:
        stats["faults"] += 1
        # TODO: replace the oldest page (FIFO)
