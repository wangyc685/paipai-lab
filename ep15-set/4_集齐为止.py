import random
random.seed(15)

卡册 = set()
次数 = 0
while len(卡册) < 100:
    卡 = random.randint(1, 100)
    次数 += 1
    if 卡 not in 卡册:
        print("新", 次数, 卡)
    卡册.add(卡)

print("集齐了！一共抽了", 次数, "次")
print("重复的有", 次数 - 100, "张")
