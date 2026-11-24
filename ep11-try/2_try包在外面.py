# 第二版：把整个循环包进 try。不崩了，但只算到第 233 行，因为循环早就断了。
总数 = 0
try:
    for 行 in open("账单.txt", encoding="utf-8"):
        钱 = 行.split()[1]
        总数 += int(钱)
except ValueError:             # 出了这种错，我来接
    print("有一行看不懂")
print("今年花了", 总数, "元")
