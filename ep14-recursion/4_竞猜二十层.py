def 步数(n):
    if n == 1:
        return 1
    return 步数(n - 1) * 2 + 1

print(步数(20))
