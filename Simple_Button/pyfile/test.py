import sys

def method1 (a,b,c):
	a = int(a)
	b = int(b)
	c = int(c)
	return a+b+c

a = sys.argv[1]
b = sys.argv[2]
c = sys.argv[3]
print(method1(a,b,c))

