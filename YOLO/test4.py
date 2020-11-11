import random

aaa = []
for i in range(380,400):
    aaa.append('/content/yolo/{}.jpg'.format(i))

print(aaa)
xxx = []
zzz = random.sample(aaa,20)
for o in zzz:
    with open('./cfg_test/train.txt','a',encoding='utf-8') as f:
        f.write(o +'\n' )
    xxx.append(o)
print(sorted(xxx))