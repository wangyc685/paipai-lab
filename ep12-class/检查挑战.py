"""运行你改好的 挑战.py，看它打印的是不是：一张红色的鲤鱼：小红"""
import subprocess
import sys

p = subprocess.run([sys.executable, "-X", "utf8", "挑战.py"], capture_output=True, text=True, encoding="utf-8")
if p.returncode != 0:
    print("挑战.py 运行出错了：")
    print(p.stderr)
    sys.exit(1)
got = p.stdout.strip()
print("你的程序输出：", got)
if got == "一张红色的鲤鱼：小红":
    print("✓ 对了！挑战完成，把代码贴到视频评论区吧。")
else:
    print("✗ 还不对。提示：Python 有一个特殊方法，名字前后各有两个下划线，print 一个对象时会去调用它。")
