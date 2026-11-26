class 发条玩具:
    def __init__(self, 名字):
        self.名字 = 名字

    def 上发条(self):
        print(self.名字, "咔哒咔哒")

    def 走(self):
        print(self.名字, "往前走了一步")

老铁 = 发条玩具("老铁")
老铁.上发条()
老铁.走()
