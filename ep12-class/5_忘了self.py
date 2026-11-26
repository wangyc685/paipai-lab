# 第五版：方法忘了写 self，会报 TypeError。
# 调用 小红.跳() 时，Python 会把「这一张」自己塞进去，方法得留个 self 接住。
class 鲤鱼:
    def __init__(self, 名字, 颜色):
        self.名字 = 名字          # 这一张自己的名字
        self.颜色 = 颜色          # 这一张自己的颜色

    def 游(self):
        print(self.名字, "游走了")

    def 跳():
        print("跳！")

小红 = 鲤鱼("小红", "红")
小红.跳()
