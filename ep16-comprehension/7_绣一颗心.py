横 = [i / 10 for i in range(-14, 15)]           # 从左到右 29 格
竖 = [i / 10 for i in range(13, -12, -1)]        # 从上到下 25 行
心 = ["".join(["#" if (x * x + y * y - 1) ** 3 - x * x * y ** 3 <= 0 else "."
               for x in 横])
      for y in 竖]

for 行 in 心:
    print(行)
print("一共绣了", sum([行.count("#") for 行 in 心]), "针")
