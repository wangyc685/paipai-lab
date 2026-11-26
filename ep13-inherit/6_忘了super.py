class 发条玩具:
    def __init__(self, 名字):
        self.名字 = 名字

    def 上发条(self):
        print(self.名字, "咔哒咔哒")

    def 走(self):
        print(self.名字, "往前走了一步")

class 小车(发条玩具):
    def __init__(self, 名字, 颜色):
        self.颜色 = 颜色

    def 走(self):
        print(self.颜色 + "色的" + self.名字, "冲了出去")

闪电 = 小车("闪电", "红")
闪电.走()
