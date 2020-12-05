import os


def load(filename: str, separator: str = ',', index: list = None):
    assert os.path.isfile(filename), 'file not found'
    col_num = -1
    table = []
    with open(filename, 'r') as fi:
        while True:
            line = fi.readline().strip()
            if not bool(line):
                break
            elems = tuple(float(elem) for elem in line.split(separator))
            if col_num < 0:
                col_num = len(elems)
            assert col_num > 0 and col_num == len(elems), f'wrong line {line}'
            table.append(elems)
    assert bool(table), 'reading failed'
    if bool(index):
        table = select(table, index)
    return table


def select(table: list, index: list):
    assert len(table) > 0 and len(table[0]) > 0, 'table empty'
    assert all(i < len(table[0]) for i in index), 'out of range'
    assert len(set(len(row)
                   for row in table)) == 1, 'rows have different lengths'
    return tuple(
        tuple(row[i] if i >= 0 else ir for i in index)
        for ir, row in enumerate(table))


if __name__ == '__main__':
    print(load(filename='./test/cos_sin.csv', index=[1, 2]))
    print(load(filename='./test/cos_sin.csv', index=[-1, 2]))
