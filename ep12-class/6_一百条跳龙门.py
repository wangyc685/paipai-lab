# 第六版：一块版，印一百张，一条条跳龙门（random.seed(2027)：红 23、金 22、黑 29、白 26）。
import random
random.seed(2027)

class 鲤鱼:
    def __init__(self, 名字, 颜色):
        self.名字 = 名字
        self.颜色 = 颜色

    def 跳龙门(self):
        print(self.颜色 + "鲤鱼", self.名字, "跳过去了！")

鱼塘 = []
for i in range(100):
    鱼塘.append(鲤鱼("鱼" + str(i + 1), random.choice(["红", "金", "黑", "白"])))

for 鱼 in 鱼塘:
    鱼.跳龙门()
print("一共", len(鱼塘), "条")
