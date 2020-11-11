#2-1題
'''
請撰寫一程式，讓使用者輸入十個整數，計算並輸出偶數和奇數的個數。
'''
'''
I = 1
J = 0
K = 0
print('輸入10個正整數')
while I <= 10:
    A = eval(input(''))
    if A % 2 == 0:
        J += 1
    else:
        K += 1
    I += 1
print('偶數有''{}''個'.format(J))
print('奇數有''{}''個'.format(K))
'''

#2-2題
'''
請撰寫一程式，以不定數迴圈的方式讓使用者輸入西元年份，
然後判斷它是否為閏年（leap year）或平年。
其判斷規則如下：每四年一閏，每百年不閏，但每四百年也一閏。
(假設此不定數迴圈輸入-9999則會結束此迴圈。)
'''
'''
while True:
    A = eval(input('西元年分'))
    if A == -9999:
        break
    # if A % 4 == 0 and A % 100 != 0 and A % 400 == 0:
    if A % 4 == 0 and A % 100 != 0:
        print('leap year')
    elif A % 400 == 0:
        print('leap year')
    else:
        print('not leap year')
'''

#2-3題
'''
a = [[int(input('st{},score{}:'.format(i,o))) for o in range(1,6)]  for i in range(1,4)]

for i in range(len(a)):
    print('st{}-總分:{},平均:{:.2f}'.format(i+1,sum(a[i]), sum(a[i]) / 5))
'''

#2-4題
'''
請撰寫一程式，輸入X組和Y組各自的科目至集合中，
以字串"end"作為結束點（集合中不包含字串"end"）。
請依序分行顯示
(1) X組和Y組的所有科目、
(2)X組和Y組的共同科目、
(3)Y組有但X組沒有的科目，
以及(4) X組和Y組彼此沒有的科目（不包含相同科目）
'''
'''
a = str(input('字元'))
x = eval(input('個數'))
y = eval(input('列數'))

def compute(a,x,y):
    for i in range(y):
        for p in range(x):
            print('{} '.format(a),end='')
        print()

def main():
    compute(a,x,y)

if __name__ == '__main__':
    main()
'''

#2-5題
'''
請撰寫一程式，讓使用者輸入兩個整數，接著呼叫函式compute()，
此函式接收兩個參數a、b，並回傳從 a 連加到 b的和。
'''
'''
def compute(a,b):
    c = 0
    for i in range(a,b+1):
        c += i
    print(c)

c =eval(input())
d =eval(input())
compute(c,d)
'''

#2-6題
'''
請撰寫一程式，為一詞典輸入資料（以輸入鍵值"end"作為輸入結束點，詞典中將不包含鍵值"end"），
再輸入一鍵值並檢視此鍵值是否存在於該詞典中。
'''
'''
A = {}
while True:
    B = (input('key:'))
    if B == 'end':
        break
    A[B] = (input('valueL'))

C = input()
print(C in A.keys())
'''

#2-7題
'''
請撰寫一程式，輸入X組和Y組各自的科目至集合中，
以字串"end"作為結束點（集合中不包含字串"end"）。
請依序分行顯示
(1) X組和Y組的所有科目、
(2)X組和Y組的共同科目、
(3)Y組有但X組沒有的科目，
以及(4) X組和Y組彼此沒有的科目（不包含相同科目）
'''
'''
A = set()
B = set()
while True:
    C = input('A值')
    if C == 'end':
        break
    A.add(C)

while True:
    D = input('B值')
    if D == 'end':
        break
    B.add(D)
print(sorted(A | B))
print(sorted(A & B))
print(sorted(B - A))
print(sorted(A ^ B))
'''


#2-10題
'''
請撰寫一程式，要求使用者輸入一個長度為6的字串，
將此字串分別置於10個欄位的寬度的左邊、
中間和右邊，並顯示這三個結果，左右皆以直線 |（Vertical bar）作為邊界。
'''
'''
A = str(input())
print('|{:<10}||{:^10}||{:>10}|'.format(A,A,A))
'''

#2-11題
'''
請撰寫一程式，輸入四個整數，然後將這四個整數以欄寬為5、欄與欄間隔一個空白字元，
再以每列印兩個的方式，先列印向右靠齊，再列印向左靠齊，左右皆以直線 |（Vertical bar）作為邊界。
'''
'''
for I in range(0,1):
    A = eval(input())
    B = eval(input())
    C = eval(input())
    D = eval(input())
print('|{:>5}{:>5}|'.format(A,B))
print('|{:>5}{:>5}|'.format(C,D))
print('|{:<5}{:<5}|'.format(A,B))
print('|{:<5}{:<5}|'.format(C,D))
#print('{:5} {:5} {:5} {:5}'.format(A,B,C,D))
#print('|{:>5}||{:<5}||{:>5}||{:<5}||{:>5}||{:<5}||{:>5}||{:<5}|'.format(A,A,B,B,C,C,D,D))
'''

#2-12題
'''
請使用迴圈敘述撰寫一程式，要求使用者輸入一個正整數 n（n<10），顯示 n*n 乘法表。
(每項運算式需進行格式化排列整齊，每個運算子及運算元輸出的欄寬為2，而每項乘積輸出的欄寬為4，皆靠左對齊不跳行。)
'''
'''
C = eval(input())
for B in range(1,C+1):
    for A in range(2,C+1):
        print('{:<2}{:<2}{:<2}{:<2}{:<4}  '.format(A,'x',B,'=',A*B),end='')
    print()
'''
#2-13
'''
def compute(x):
    if x == 0:
        return 0
    elif x ==1:
        return 1
    else:
        return compute(x-1) +compute(x-2)

a = eval(input())
if a >= 2:
    for i in range(a):
        print(compute(i), end='')
'''