import random
random.seed(51)

卡包 = []
for i in range(10):
    卡包.append(random.randint(1, 100))   # 拆一包，抽到第几号卡

print(卡包)
print(len(卡包), "张")
