import os
path = "./123456/"
# 獲取該目錄下所有檔案，存入列表中
f = os.listdir(path)
print(len(f))

print(f[0])

n = 0
i = 0
u = 240
for i in f:
    # 設定舊檔名（就是路徑+檔名）
    oldname = f[n]

    # 設定新檔名
    newname = str(u+1) + '.jpg'
    # 用os模組中的rename方法對檔案改名
    os.rename(path+oldname, path+newname)
    print(oldname, '======>', newname)

    n += 1
    u += 1