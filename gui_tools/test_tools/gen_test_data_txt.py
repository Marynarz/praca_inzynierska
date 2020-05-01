import random
import sys


def gen_data(min_val=-10, max_val=10, lines_number=10, file_name='test_data.txt'):
    with open(file_name, 'w')as f:
        for i in range(0, lines_number):
            x = i
            y = random.randrange(min_val, max_val*1000, 1)
            f.write('%f %f\n' % (x, y/1000))
    print('OK!')


if __name__ == '__main__':
    try:
        gen_data(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
    except Exception as e:
        print(e)
