#1-1題
'''
請撰寫一程式，讓使用者輸入五個數字，計算並輸出這五個數字之數值、總和及平均數。
提示：總和與平均數皆輸出到小數點後第1位。
'''
'''
A = float(input('請輸入數字1'))
B = float(input('請輸入數字2'))
C = float(input('請輸入數字3'))
D = float(input('請輸入數字4'))
E = float(input('請輸入數字5'))

print('{:<2.1f} {:<2.1f} {:<2.1f} {:<2.1f} {:<2.1f} '.format(A,B,C,D,E))
print('總和' , '{:<2.1f}'.format(A+B+C+D+E))
print('平均數' , '{:<2.1f}'.format((A+B+C+D+E)/5))
'''

#1-2題
'''
假設一賽跑選手在x分y秒的時間跑完z公里，請撰寫一程式，輸入x、y、z數值，
最後顯示此選手每小時的平均英哩速度（1英哩等於1.6公里）。
提示：輸出浮點數到小數點後第一位。
'''
'''
X =eval(input('幾分'))
Y =eval(input('幾秒'))
Z =eval(input('幾公里'))
Y =60 * X + Y
W = Z / 1.6
print('平均英里','{:.1f}'.format(W/Y*3600))
'''

#1-3題
'''
請撰寫一程式，輸入兩個正數，代表一矩形之寬和高，計算並輸出此矩形之高（Height）、寬（Width）、周長（Perimeter）及面積（Area）。
提示：輸出浮點數到小數點後第二位。
'''
'''
A = eval(input('寬:'))
B = eval(input('高:'))
print('Height' , '{:.2f}'.format(A))
print('Width' , '{:.2f}'.format(B))
print('Perimeter' ,'{:.2f}'.format(2*(A+B)))
print('Area','{:.2f}'.format(A*B))
'''

#1-4題
'''
請使用選擇敘述撰寫一程式，讓使用者輸入三個邊長，檢查這三個邊長是否可以組成一個三角形。
若可以，則輸出該三角形之周長；否則顯示【Invalid】。
提示：檢查方法 = 任意兩個邊長之總和大於第三邊長。
'''
'''
A =eval(input('周長1'))
B =eval(input('周長2'))
C =eval(input('周長3'))
if A + B > C and A + C > B and B + C > A:
    print('周長','{}'.format(A+B+C))
else:
    print('{}'.format('Invalid'))
'''

#1-5題
'''
請使用選擇敘述撰寫一程式，讓使用者輸入一個十進位整數num(0 ≤ num ≤ 15)，將num轉換成十六進位值。
提示：轉換規則 = 十進位0~9的十六進位值為其本身，十進位10~15的十六進位值為A~F。
'''
'''
A = eval(input('輸入0~15'))
if A >= 0 and A <= 15:
    print('{:X}'.format(A))
'''

#1-6題
'''
請使用選擇敘述撰寫一程式，要求使用者輸入購物金額，購物金額需大於8,000（含）以上，
並顯示折扣優惠後的實付金額。購物金額折扣方案如下表所示：
金額	折扣
8,000（含）以上	9.5折
18,000（含）以上	9折
28,000（含）以上	8折
38,000（含）以上	7折
'''
'''
A = eval(input('購物金額'))
if A >= 38000:
        print('折扣後金額','{}'.format(A*0.7))
elif A >= 28000:
        print('折扣後金額', '{}'.format(A * 0.8))
elif A >= 18000:
        print('折扣後金額', '{}'.format(A * 0.9))
elif A >= 8000:
        print('折扣後金額', '{}'.format(A * 0.95))
'''

#1-7題
'''
請使用選擇敘述撰寫一程式，根據使用者輸入的分數顯示對應的等級。標準如下表所示：
分數	等級
80 ~ 100	A
70 ~ 79	B
60 ~ 69	C
<= 59	F
'''
'''
A = eval(input('成績'))
if A >=80 and A <=100:
    print('A')
elif A >= 70 and A <80:
    print('B')
elif A >=60 and A <70:
    print('C')
elif A <= 59:
    print('F')
'''

#1-8題
'''
請使用選擇敘述撰寫一程式，讓使用者輸入一個正整數，然後判斷它是3或5的倍數，
顯示【x is a multiple of 3.】或【x is a multiple of 5.】；
若此數值同時為3與5的倍數，顯示【x is a multiple of 3 and 5.】；
如此數值皆不屬於3或5的倍數，顯示【x is not a multiple of 3 or 5.】，
將使用者輸入的數值代入x。
'''
'''
X =eval(input('正整數'))
if X % 3 == 0 and X % 5 == 0:
    print('x is a multiple of 3 and 5.')
elif X % 3 == 0:
    print('x is a multiple of 3.')
elif X % 5 == 0:
    print('x is a multiple of 5.')
else:
    print('x is not a multiple of 3 or 5.')
'''

#1-9題
'''
請使用迴圈敘述撰寫一程式，提示使用者輸入金額（如10,000）、年收益率（如5.75），
以及經過的月份數（如5），接著顯示每個月的存款總額。
提示：四捨五入，輸出浮點數到小數點後第二位。

舉例：
假設您存款$10,000，年收益為5.75%。
過了一個月，存款會是：10000 + 10000 * 5.75 / 1200 = 10047.92
過了兩個月，存款會是：10047.92 + 10047.92 * 5.75 / 1200 = 10096.06
過了三個月，存款將是：10096.06 + 10096.06 * 5.75 / 1200 = 10144.44
以此類推。
'''
'''
A = eval(input('金額'))
B = eval(input('年收益率'))
C = eval(input('月份'))
I = 1

print('{}  {}'.format('月份','存款總額'))
while I <= C:
    #X =A + A * ((B * I) / 1200)
    A += (A * B /1200)
    #print('{:.2f}'.format(X))
    #print('{:.2f}'.format(A))
    print('{:>2}   {:>3.2f}'.format(I,A))
    I += 1
print()
'''

#1-10題
'''
請使用迴圈敘述撰寫一程式，讓使用者輸入一個正整數a，
利用迴圈計算從1到a之間，所有5之倍數數字總和。
'''
'''
A =eval(input('正整數'))
C = 0
for B in range(1,A+1):
    if B % 5 == 0:
        C += B
print(C)
'''

#1-11題
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