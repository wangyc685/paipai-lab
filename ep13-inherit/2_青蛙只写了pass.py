class 发条玩具:
    def __init__(self, 名字):
        self.名字 = 名字

    def 上发条(self):
        print(self.名字, "咔哒咔哒")

    def 走(self):
        print(self.名字, "往前走了一步")

class 青蛙(发条玩具):     # 括号里写谁，就继承谁
    pass

小绿 = 青蛙("小绿")
小绿.上发条()
小绿.走()
