# 第三版：try 挪进循环里，每一行都有自己的网。可第 512 行是空行，报的是 IndexError，它不管。
总数 = 0
坏行 = 0
for 行 in open("账单.txt", encoding="utf-8"):
    try:
        钱 = 行.split()[1]
        总数 += int(钱)
    except ValueError:         # 坏一行，就扔一行
        坏行 += 1
print("今年花了", 总数, "元，看不懂的有", 坏行, "行")
