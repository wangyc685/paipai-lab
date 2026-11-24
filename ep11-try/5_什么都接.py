# 第五版：光秃秃的 except，什么错都接，还手滑把「总数」打成了「总树」。
# 打错字的 NameError 也被它接住了，一声不吭：结果是 0 元。别这么写。
总数 = 0
坏行 = 0
for 行 in open("账单.txt", encoding="utf-8"):
    try:
        钱 = 行.split()[1]
        总树 += int(钱)
    except:
        坏行 += 1
print("今年花了", 总数, "元，看不懂的有", 坏行, "行")
