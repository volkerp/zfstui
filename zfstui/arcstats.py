

def format_bytes(byte_string):
    """Return human-readable representation of a byte value in
    powers of 2 (eg "KiB" for "kibibytes", etc) to two decimal
    points. Values smaller than one KiB are returned without
    decimal points. Note "bytes" is a reserved keyword.
    """

    prefixes = [(2**80, "YiB"),   # yobibytes (yotta)
                (2**70, "ZiB"),   # zebibytes (zetta)
                (2**60, "EiB"),   # exbibytes (exa)
                (2**50, "PiB"),   # pebibytes (peta)
                (2**40, "TiB"),   # tebibytes (tera)
                (2**30, "GiB"),   # gibibytes (giga)
                (2**20, "MiB"),   # mebibytes (mega)
                (2**10, "KiB")]   # kibibytes (kilo)

    bites = int(byte_string)

    if bites >= 2**10:
        for limit, unit in prefixes:

            if bites >= limit:
                value = bites / limit
                break

        result = '{0:.1f} {1}'.format(value, unit)
    else:
        result = '{0} Bytes'.format(bites)

    return result


def read_kstat():
    with open('/proc/spl/kstat/zfs/arcstats') as p:
        lines = [line.strip() for line in p]

    del lines[0:2]
    kstat = {}

    for s in lines:
        if not s:
            continue

        name, _, value = s.split()
        kstat[name] = int(value)

    return kstat


