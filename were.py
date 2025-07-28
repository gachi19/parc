#4
def number(*args):
    num_sum = 0
    for f in args:
        num_sum += f
    avgs = num_sum / len(args)
    num_list = list(args)
    for f in args:
        if f < avgs:
            num_list.remove(f)
    return num_list
print(number(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))