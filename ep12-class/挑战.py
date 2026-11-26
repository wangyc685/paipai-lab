# 编程挑战：现在 print(小红) 打出来是一串地址。
# 改 class 鲤鱼，让它打印出：一张红色的鲤鱼：小红
# 改完运行 python 检查挑战.py 看看对不对。
class 鲤鱼:
    def __init__(self, 名字, 颜色):
        self.名字 = 名字
        self.颜色 = 颜色

小红 = 鲤鱼("小红", "红")
print(小红)
