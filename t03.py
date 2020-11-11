#610
'''
A = []
print('week1')
for i in range(3):
    B = eval(input())
    A.append(B)
print('week2')
for i in range(3):
    B = eval(input())
    A.append(B)
print('week3')
for i in range(3):
    B = eval(input())
    A.append(B)
print('week4')
for i in range(3):
    B = eval(input())
    A.append(B)
print('{:.2f}'.format(sum(A)/len(A)))
print(max(A))
print(min(A))
'''

#609
'''
L1 = [[0 for t in range(2)]for y in range(2)]
L2 = [[0 for t in range(2)]for y in range(2)]

print('1',':')
for t in range(2):
    for y in range(2):
        print([t+1,y+1],':',end='')
        L1[t][y] = eval(input())
print('2',':')
for t in range(2):
    for y in range(2):
        print([t+1,y+1],':',end='')
        L2[t][y] = eval(input())

print(1,':')
for i in range(2):
    for o in range(2):
        print('{:^4}'.format(L1[i][o]),end='')
        if o % 2 == 1:
            print()
print(2,':')
for i in range(2):
    for o in range(2):
        print('{:^4}'.format(L2[i][o]),end='')
        if o % 2 == 1:
            print()
print('sum')
for i in range(2):
    for o in range(2):
        print('{:^4}'.format(L1[i][o]+L2[i][o]), end='')
        if o % 2 == 1:
            print()
'''

#607
'''
Q = []
W = []
E = []
print(1,'student')
for o in range(5):
    B = eval(input())
    Q.append(B)
print(2,'student')
for i in range(5):
    C = eval(input())
    W.append(C)
print(3,'student')
for P in range(5):
    D = eval(input())
    E.append(D)
print(1,'student')
print(sum(Q))
print(sum(Q)/5)
print(2,'student')
print(sum(W))
print(sum(W)/5)
print(3,'student')
print(sum(E))
print(sum(E)/5)
'''

#606
'''
def computr(a,b):
    for i in range(a):
        for o in range(b):
            print('{:4}'.format(o-i),end='')
        print()

def main():
    x = eval(input())
    y = eval(input())
    computr(x,y)

if __name__ == '__main__':
    main()
'''

#605
'''
A = []
for i in range(10):
    B = eval(input())
    A.append(B)
C = sum(A)-max(A)-min(A)
print(C)
print('{:.2f}'.format(C/8))
'''

#604
'''
A = []
C = 0
D = 0
for i in range(10):
    B = input()
    A.append(B)
for o in range(10):
    if A.count(A[o]) > C:
        D = A[o]
        C += 1
print(D)
print(C)
'''

#603
'''
A = []
for i in range(10):
    B = eval(input())
    A.append(B)

#B = sorted(A,reverse=True)
#print(B[0],B[1],B[2])
A.sort(reverse=True)
print(A[0],A[1],A[2])
'''

#602
'''
A = []
C = 0
for i in range(5):
    B = input()
    if B == 'J':
        B = 11
    if B == 'Q':
        B = 12
    if B == 'K':
        B = 13
    if B == 'A':
        B = 1
    A.append(int(B))
print(sum(A))
#for o in range(5):
#    C += A[o]
#print(C)
'''

#601
'''
A = []
D = 0
C = 0
for i in range(12):
    B = eval(input())
    A.append(B)
for o in range(len(A)):
    D += 1
    print('{:>3}'.format(A[o]),end='')

    if D % 3 == 0:
        print()
    if D % 2 != 0:
        C += A[o]
print()
print(C)
'''

#710
'''
A = {}
while True:
    B = str(input('keys:'))
    if B == 'end':
        break
    A[B] = str(input('value:'))
C = str(input())
print(C in A.keys())
'''

#709
'''
A = {}
while True:
    print('key')
    C = str(input())
    if C == 'end':
        break
    A[C] = str(input())
for i in sorted(A.keys()):
    print(i,':',A[i])
'''

#708
'''
A = {}
while True:
    B = (input('keys:'))
    if B == 'end':
        break
    A[B] = (input('value:'))

C = {}
while True:
    D = (input('keys:'))
    if D == 'end':
        break
    C[D] = (input('value:'))
A.update(C)
for i in sorted(A.keys()):
    print(i,':',A[i])
'''

#707
'''
A = set()
while True:
    B = input()
    if B == 'end':
        break
    A.add(B)

C = set()
while True:
    D = input()
    if D == 'end':
        break
    C.add(D)

print(sorted(A | C))
print(sorted(A & C))
print(sorted(C - A))
print(sorted(A ^ C))
'''

#705
'''
A = set()
print('set1:')
for i in range(5):
    B = input()
    A.add(B)

C = set()
print('set2:')
for o in range(3):
    D = input()
    C.add(D)

E = set()
print('set3:')
for p in range(9):
    F = input()
    E.add(F)

if C.issubset(A):
    print('true')
else:
    print('false')

if E.issuperset(A):
    print('true')
else:
    print('false')
'''

#704
'''
A = set()
while True:
    B = int(input())
    if B == -9999:
        break
    A.add(B)
print('length:',len(A))
print('max:',max(A))
print('min:',min(A))
print('sum:',sum(A))
'''

#703
'''
A =[]
while True:
    B = input()
    if B == 'end':
        break
    A.append(B)
    C =tuple(A)
print(C)
print(C[0:3])
print(C[-3:])
'''

#702
'''
A =[]
while True:
    B = eval(input())
    if B == -9999:
        break
    A.append(B)


C =[]
while True:
    D = eval(input())
    if D == -9999:
        break
    C.append(D)

E =tuple(A)
F =tuple(C)
print(E+F)
print(sorted(E+F))

#A.extend(C)
#E = tuple(A)
#print(E)
#A.sort()
#print(A)
'''

#701
'''
A = []
while True:
    B =eval(input())
    if B == -9999:
        break
    A.append(B)

C = tuple(A)

print(C)
print('length:',len(C))
print('max:',max(C))
print('min:',min(C))
print('sum:',sum(C))
'''

#807
'''
A = input().split(' ')
B = []
for i in range(len(A)):
    B.append(int(A[i]))
print(sum(B))
print(sum(B)/5)
'''

#806
'''
def compute(x,y):
    print(x.count(y))

def main():
    A = input()
    B = input()
    compute(A,B)

if __name__ == '__main__':
    main()
'''

#805
'''
A = input()
print('|{:<10}|'.format(A))
print('|{:^10}|'.format(A))
print('|{:>10}|'.format(A))
'''

#804
'''
A = input()
print(A.upper())
print(A.title())
'''

#803
'''
A = input().split(' ')
print(A[-3],A[-2],A[-1])
'''

#801
'''
A = input()
for i in range(len(A)):
    #print('index of',A[i],':',i)
    print("index of '{}' : ".format(A[i]),i)
'''

#poker
'''
import random

people = int(input('people:'))
number = []
for i in range(1,14):
    number.append(str(i))
#print(number)
flower = ['Diamond','Club','Heart','Spade']
poker = []
for i in range(len(flower)):
    for o in range(len(number)):
        poker.append(flower[i]+number[o])
#print(poker)


def play(x):
    for i in range(1,x+1):
        #print('player{}'.format(i),random.sample(poker,13))
        a = random.sample(poker,int((52/x)))
        print('player{}:'.format(i),a)
        for o in range(len(a)):
            #print(a[o])
            poker.remove(a[o])
play(people)

#a = random.sample(poker,13)
#print(a)

'''

