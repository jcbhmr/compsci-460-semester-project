bytes_suffixes = ['B', 'kB', 'MB', 'GB', 'TB', 'PB']
def pretty_bytes(nbytes):
    i = 0
    while nbytes >= 1000 and i < len(bytes_suffixes)-1:
        nbytes /= 1000.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, bytes_suffixes[i])

bits_suffixes = ['b', 'kb', 'Mb', 'Gb', 'Tb', 'Pb']
def pretty_bits(nbits):
    i = 0
    while nbits >= 1000 and i < len(bits_suffixes)-1:
        nbits /= 1000.
        i += 1
    f = ('%.2f' % nbits).rstrip('0').rstrip('.')
    return '%s %s' % (f, bits_suffixes[i])
