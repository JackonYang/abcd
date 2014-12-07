
def read_data(file_name):
    data = dict()
    with open(file_name) as f:
        for line in f.readlines():
            year, cloze, read_a, read_b = line.strip().split(' ')
            item = list(cloze)
            item.extend(read_a)
            item.extend(read_b)
            data[year] = item
    return data

def run():
    data = read_data('data/data.txt')
    for k, v in data.items():
        print k, len(v)

if __name__ == "__main__":
    run()

