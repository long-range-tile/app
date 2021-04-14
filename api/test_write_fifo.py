import time
import sys

if __name__ == '__main__':
    i = int(sys.argv[1])
    while True:
        print('{"MAC":"test_mac' + str(i) + '","other_data":5}')
        sys.stdout.flush()
        i += 1
        time.sleep(0.5)
