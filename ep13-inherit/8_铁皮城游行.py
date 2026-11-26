import random
random.seed(1313)
class 发条玩具:
    def __init__(self, 名字):
        self.名字 = 名字

    def 上发条(self):
        print(self.名字, "咔哒咔哒")

    def 走(self):
        print(self.名字, "往前走了一步")

class 青蛙(发条玩具):
    def 走(self):            # 同名方法：用自己的
        print(self.名字, "蹦了一下")

class 小鸟(发条玩具):
    def 飞(self):            # 新本事：爸爸没有的
        print(self.名字, "飞了起来")

class 小车(发条玩具):
    def __init__(self, 名字, 颜色):
        super().__init__(名字)    # 先请爸爸把名字装上
        self.颜色 = 颜色

    def 走(self):
        print(self.颜色 + "色的" + self.名字, "冲了出去")

叫法 = {发条玩具: "铁人", 青蛙: "青蛙", 小鸟: "小鸟", 小车: "小车"}
游行队 = []
for i in range(24):
    挑 = random.choice([发条玩具, 青蛙, 小鸟, 小车])
    名字 = 叫法[挑] + str(i + 1)
    if 挑 == 小车:
        游行队.append(小车(名字, random.choice(["红", "黄", "蓝"])))
    else:
        游行队.append(挑(名字))

for 玩具 in 游行队:
    玩具.走()
