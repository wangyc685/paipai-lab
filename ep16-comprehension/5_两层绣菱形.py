图 = ["".join(["#" if abs(x - 7) + abs(y - 7) <= 7 else "."
               for x in range(15)])          # 里层：每一格
      for y in range(15)]                    # 外层：15 行
for 行 in 图:
    print(行)
