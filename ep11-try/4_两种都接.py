# 第四版：两种错都点名。终于跑完了。
总数 = 0
坏行 = 0
for 行 in open("账单.txt", encoding="utf-8"):
    try:
        钱 = 行.split()[1]
        总数 += int(钱)
    except (ValueError, IndexError):
        坏行 += 1
print("今年花了", 总数, "元，看不懂的有", 坏行, "行")
