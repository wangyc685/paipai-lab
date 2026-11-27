import random
random.seed(2026)

def 集齐要抽几次():
    卡册 = set()
    次数 = 0
    while len(卡册) < 100:
        卡册.add(random.randint(1, 100))
        次数 += 1
    return 次数

结果 = []
for i in range(10000):
    结果.append(集齐要抽几次())

print("平均", sum(结果) / len(结果), "次")
print("最快", min(结果), "次，最慢", max(结果), "次")

for 起点 in range(200, 1400, 100):     # 每 100 次一格，数一数落在这一格的有几本
    本数 = 0
    for x in 结果:
        if 起点 <= x < 起点 + 100:
            本数 += 1
    print(起点, "到", 起点 + 99, "次：", 本数, "本")
