"""Milestone 2 virtual memory simulation."""

from collections import OrderedDict, deque

from calc import PAGE_SIZE, PT_ENTRIES, memory_values
from tracefile import read_trace


def simulate(p):
    mem = memory_values(p)
    free = deque(range(mem["system_pages"], mem["phys_pages"]))
    tables = [{} for _ in p.traces]  # virtual page -> physical page
    used = [set() for _ in p.traces]
    owners = OrderedDict()  # physical page -> (pid, virtual page)
    stats = {"mapped": 0, "hits": 0, "from_free": 0, "faults": 0}

    traces = [list(read_trace(name)) for name in p.traces]
    pos = [0] * len(traces)
    running = list(range(len(traces)))

    # round robin
    while running:
        for pid in list(running):
            trace = traces[pid]
            start = pos[pid]
            if p.time_slice == -1:
                end = len(trace)
            else:
                end = min(start + p.time_slice, len(trace))

            for address, _, data in trace[start:end]:
                for a in (address,) + data:
                    access(pid, a, tables, used, owners, free, stats)
            pos[pid] = end

            if end == len(trace):
                end_process(pid, tables, owners, free)
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


def access(pid, address, tables, used, owners, free, stats):
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
        if not owners:
            return
        # replace the oldest page (FIFO)
        ppn, (old_pid, old_vpn) = owners.popitem(last=False)
        del tables[old_pid][old_vpn]

    table[vpn] = ppn
    owners[ppn] = (pid, vpn)
    used[pid].add(vpn)


def end_process(pid, tables, owners, free):
    for ppn in tables[pid].values():
        del owners[ppn]
        free.append(ppn)
    tables[pid].clear()
