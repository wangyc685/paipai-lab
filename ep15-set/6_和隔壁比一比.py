import random
random.seed(808)

我的 = set()
你的 = set()
for i in range(80):
    我的.add(random.randint(1, 100))
    你的.add(random.randint(1, 100))

print("我有", len(我的), "张，你有", len(你的), "张")
print("都有的：", len(我的 & 你的))
print("我有你没有：", len(我的 - 你的))
print("你有我没有：", len(你的 - 我的))
print("合起来：", len(我的 | 你的))
print("还差：", 100 - len(我的 | 你的))
