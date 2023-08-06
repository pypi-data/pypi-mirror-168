def read_file(filename):
    di = dict()
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            res = line.strip().split("\t")
            di[res[0]] = float(res[1])
    return di