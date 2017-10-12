from pybloom import BloomFilter

f = BloomFilter(capacity=10000, error_rate=0.01)

error_num = 0
success_num = 0

for i in xrange(10000):
    f.add('kk'+str(i))

for i in xrange(10000):
    string = 'kk'+str(i)
    if string in f:
        success_num = success_num + 1
    else:
        error_num = error_num + 1

print error_num
print success_num
