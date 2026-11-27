import time

def 搬(n, 从, 到, 借):            # 这次不打印，只数一共搬了几次
    if n == 1:
        return 1
    return 搬(n - 1, 从, 借, 到) + 1 + 搬(n - 1, 借, 到, 从)

开始 = time.time()
次数 = 搬(20, "A", "C", "B")
用时 = time.time() - 开始
print("搬了", 次数, "次，用了", round(用时, 2), "秒")
print("一秒能搬", round(次数 / 用时), "次")
