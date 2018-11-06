# test for dictionnary

from collections import OrderedDict

data = OrderedDict()

a = 1 
data['1'] = format(a)
b = 2
data['2'] = format(b)
c = 3
data['3'] = format(c)
d = 4
data['4'] = format(d)

for k, v in data.items():
    print('Test : {0}, Description : {0}'.format(k,v))



