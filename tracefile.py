"""Trace file reader."""

NO_DATA = "--------"


def read_trace(path):
    """Yield (address, length, data addresses) for each instruction."""
    fetch = None
    with open(path, errors="replace") as f:
        for line in f:
            if line.startswith("EIP"):
                if fetch is not None:
                    yield fetch + ((),)
                fetch = parse_fetch(line)
            elif line.startswith("dstM:") and fetch is not None:
                yield fetch + (parse_data(line),)
                fetch = None
    if fetch is not None:
        yield fetch + ((),)


def parse_fetch(line):
    # EIP (04): 7c809767 ...  (length is decimal, address is hex)
    try:
        return int(line[10:18], 16), int(line[5:7])
    except ValueError:
        return None


def parse_data(line):
    # dstM: 7ffdf034 00000000    srcM: 7ffdfe2c 901e8b00
    fields = line.split()
    addresses = []
    for i in (1, 4):
        try:
            address = int(fields[i], 16)
            if address and fields[i + 1] != NO_DATA:
                addresses.append(address)
        except (IndexError, ValueError):
            pass
    return tuple(addresses)
