import random
random.seed(51)

卡册 = set()                  # 一本空卡册
for i in range(10):
    卡册.add(random.randint(1, 100))   # 已经有的，再放也不会多

print(卡册)
print(len(卡册), "张")
