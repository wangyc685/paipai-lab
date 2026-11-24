"""运行你改好的 挑战.py，看它算出来的总数对不对（应该是 15947.5，看不懂的只剩空行那 1 行）。"""
import re
import subprocess
import sys

p = subprocess.run([sys.executable, "-X", "utf8", "挑战.py"], capture_output=True, text=True, encoding="utf-8")
if p.returncode != 0:
    print("挑战.py 运行出错了：")
    print(p.stderr)
    sys.exit(1)
print("你的程序输出：", p.stdout.strip())
数 = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", p.stdout)]
if 数 and abs(数[0] - 15947.5) < 1e-6:
    print("✓ 总数对了：15947.5")
    if len(数) > 1 and 数[1] == 1:
        print("✓ 看不懂的只剩 1 行（空行）。挑战完成！把代码贴到视频评论区吧。")
    else:
        print("总数对了，再看看「看不懂的」是不是只剩空行那 1 行？")
else:
    print("✗ 总数还不是 15947.5，再想想：十五、23元、3.5、加蛋 8 这几行分别差在哪？")
