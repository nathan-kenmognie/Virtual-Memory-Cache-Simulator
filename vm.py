"""Milestone 2 virtual memory simulation."""

from collections import deque

from calc import PAGE_SIZE, PT_ENTRIES, memory_values
from tracefile import read_trace


def simulate(p):
    mem = memory_values(p)
    free = deque(range(mem["system_pages"], mem["phys_pages"]))
    tables = [{} for _ in p.traces]  # virtual page -> physical page, oldest first
    used = [set() for _ in p.traces]
    stats = {"mapped": 0, "hits": 0, "from_free": 0, "faults": 0, "victim": 0}

    traces = [list(read_trace(name)) for name in p.traces]
    pos = [0] * len(traces)
    running = list(range(len(traces)))

    # round robin
    while running:
        for pid in list(running):
            trace = traces[pid]
            start = pos[pid]
            if p.time_slice == -1 or start + p.time_slice > len(trace):
                # not enough trace left for a full slice, so the process finishes
                end = len(trace)
                done = True
            else:
                end = start + p.time_slice
                done = False

            for address, _, data in trace[start:end]:
                for a in (address,) + data:
                    access(pid, a, tables, used, free, stats)
            pos[pid] = end

            if done:
                end_process(pid, tables, free)
                running.remove(pid)

    stats["system_pages"] = mem["system_pages"]
    stats["user_pages"] = mem["phys_pages"] - mem["system_pages"]
    stats["processes"] = [
        {
            "used": len(u),
            "percent": len(u) * 100 / PT_ENTRIES,
            "wasted": (PT_ENTRIES - len(u)) * mem["pte_bits"] // 8,
        }
        for u in used
    ]
    return stats


def access(pid, address, tables, used, free, stats):
    stats["mapped"] += 1
    vpn = (address & 0x7FFFFFFF) // PAGE_SIZE
    table = tables[pid]
    if vpn in table:
        stats["hits"] += 1
        return

    if free:
        stats["from_free"] += 1
        ppn = free.popleft()
    else:
        stats["faults"] += 1
        victim = pick_victim(pid, tables, stats)
        if victim is None:
            return
        # take that process's oldest page
        old_vpn = list(tables[victim])[0]
        ppn = tables[victim].pop(old_vpn)

    table[vpn] = ppn
    used[pid].add(vpn)


def pick_victim(pid, tables, stats):
    # keep taking from the same process as last time, but not from ourselves
    count = len(tables)
    victim = stats["victim"]
    if victim == pid:
        victim = (victim + 1) % count
    for i in range(count):
        if len(tables[victim]) > 0:
            stats["victim"] = victim
            return victim
        victim = (victim + 1) % count
    return None


def end_process(pid, tables, free):
    free.extend(tables[pid].values())
    tables[pid].clear()
