def 步数(n):
    if n == 1:
        return 1
    return 步数(n - 1) * 2 + 1   # 搬开 + 搬最大的 + 搬回来

for n in range(1, 11):
    print(n, "层：", 步数(n), "步")
