"""检查 挑战.py：两关。第一关用 玩具清单.txt，第二关换一张你没见过的清单。"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = 'class 发条玩具:\n    def __init__(self, 名字):\n        self.名字 = 名字\n\n    def 上发条(self):\n        print(self.名字, "咔哒咔哒")\n\n    def 走(self):\n        print(self.名字, "往前走了一步")\n'
LIST2 = '小鸟 小黄\n小车 旋风 蓝\n机器人 叮叮\n青蛙 呱呱\n小车 雷霆 黄\n青蛙\n小鸟 灰灰\n'
EXPECT2 = '小黄 往前走了一步\n蓝色的旋风 冲了出去\n呱呱 蹦了一下\n黄色的雷霆 冲了出去\n灰灰 往前走了一步\n游行队伍 5 个，看不懂 2 行\n'


def run(folder, lst):
    shutil.copy(HERE / "挑战.py", folder / "挑战.py")
    (folder / "玩具清单.txt").write_text(lst, encoding="utf-8")
    return subprocess.run([sys.executable, "-X", "utf8", "挑战.py"], cwd=folder, capture_output=True, text=True, encoding="utf-8", timeout=20)


def hint_for_error(err):
    last = err.strip().splitlines()[-1] if err.strip() else ""
    print("挑战.py 运行出错了：", last)
    if "KeyError" in last or "IndexError" in last:
        print("提示：有一行看不懂，程序就崩了。还记得第 11 集派派怎么接住报错的吗？")
    elif "AttributeError" in last and "名字" in last:
        print("提示：子类自己写了 __init__，爸爸的 __init__ 就不跑了（第 13 集 1:28）。")
    elif "TypeError" in last:
        print("提示：看看创建玩具时传了几个参数，和 __init__ 要的对不对得上。")
    elif "NameError" in last:
        print("提示：是不是哪个名字拼错了，或者用之前还没定义？")


def compare(got, expect):
    g, e = got.strip().splitlines(), expect.strip().splitlines()
    for i in range(max(len(g), len(e))):
        a = g[i] if i < len(g) else "（没有这一行）"
        b = e[i] if i < len(e) else "（不该有这一行）"
        if a.rstrip() != b.rstrip():
            print(f"  第 {i + 1} 行不一样")
            print(f"    你的：{a}")
            print(f"    应该：{b}")
            return False
    return True


def main():
    src = (HERE / "挑战.py").read_text(encoding="utf-8")
    if BASE.strip() not in src:
        print("✗ 发条玩具（爸爸）被改动了。爸爸一个字都不许改，只能写子类。")
        sys.exit(1)
    for 子类 in ("青蛙", "小鸟", "小车"):
        if not re.search(r"class\s+" + 子类 + r"\s*\(\s*发条玩具\s*\)", src):
            print(f"✗ 没找到 class {子类}(发条玩具)。三个子类都要继承 发条玩具。")
            sys.exit(1)
    代码 = "\n".join(行.split("#")[0] for 行 in src.splitlines())   # 注释不算
    if "期望输出" in 代码:
        print("✗ 不能偷看 期望输出.txt 哦。")
        sys.exit(1)
    expect1 = (HERE / "期望输出.txt").read_text(encoding="utf-8")
    ok = True
    for 关, (lst, expect) in enumerate([((HERE / "玩具清单.txt").read_text(encoding="utf-8"), expect1), (LIST2, EXPECT2)], 1):
        with tempfile.TemporaryDirectory() as t:
            p = run(Path(t), lst)
        名 = "玩具清单.txt" if 关 == 1 else "一张你没见过的清单"
        if p.returncode != 0:
            print(f"✗ 第 {关} 关（{名}）：")
            hint_for_error(p.stderr)
            ok = False
            break
        if compare(p.stdout, expect):
            print(f"✓ 第 {关} 关（{名}）通过")
        else:
            print(f"✗ 第 {关} 关（{名}）没通过")
            if 关 == 2:
                print("提示：第一关过了第二关没过，是不是把第一张清单的内容写死在程序里了？")
            ok = False
            break
    if ok:
        print("全部通过！挑战完成 🎉 来视频评论区报个到，先别贴代码，给别人留点思考的机会。")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
