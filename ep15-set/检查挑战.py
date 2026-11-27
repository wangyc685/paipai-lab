"""检查 挑战.py：两关。第一关用 收藏.txt，第二关换一份你没见过的收藏。"""
import ast
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEXT2 = '阿蓝: 10, 20, 30, 30\n阿红: 30, 40, 50\n坏数据\n阿黄: 10, 40, 60, 60, 60, 70\n阿紫: 七, 20\n阿绿: 20, 50, 80, 90, 10\n'
EXPECT2 = '阿蓝： 3 种，重复 1 张，还缺 97 种\n阿红： 3 种，重复 0 张，还缺 97 种\n阿黄： 4 种，重复 2 张，还缺 96 种\n阿绿： 5 种，重复 0 张，还缺 95 种\n最该换卡的：阿黄 和 阿绿，能互换 3 对\n大家合起来： 9 种\n看不懂的行： 2 行\n'


def run(folder, text):
    shutil.copy(HERE / "挑战.py", folder / "挑战.py")
    (folder / "收藏.txt").write_text(text, encoding="utf-8")
    return subprocess.run([sys.executable, "-X", "utf8", "挑战.py"], cwd=folder, capture_output=True, text=True, encoding="utf-8", timeout=20)


def hint_for_error(err):
    last = err.strip().splitlines()[-1] if err.strip() else ""
    print("挑战.py 运行出错了：", last)
    if "ValueError" in last:
        print("提示：有一行写坏了，程序就崩了。还记得第 11 集怎么接住报错吗？想想写坏的行会报哪一种错。")
    elif "IndexError" in last:
        print("提示：有的行拆出来的段数不对，先检查一下再取。")
    elif "AttributeError" in last:
        print("提示：对象身上没有这个属性——__init__ 里有没有用 self.xxx = … 装上？（第 12 集）")
    elif "FileNotFoundError" in last:
        print("提示：要在 ep15-set 文件夹里运行。")


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


def check_rules(src):
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        print("✗ 挑战.py 有语法错误：", e)
        return False
    if not any(isinstance(n, ast.ClassDef) for n in ast.walk(tree)):
        print("✗ 没找到 class。要求 1：写一个 class，每个人是它的一个对象。")
        return False
    if not any(isinstance(n, ast.Try) for n in ast.walk(tree)):
        print("✗ 没找到 try/except。要求 2：写坏的行用 try/except 接住。")
        return False
    code = "\n".join(l.split("#")[0] for l in src.splitlines())
    if "期望输出" in code:
        print("✗ 不能偷看 期望输出.txt 哦。")
        return False
    return True


def main():
    src = (HERE / "挑战.py").read_text(encoding="utf-8")
    if not check_rules(src):
        sys.exit(1)
    expect1 = (HERE / "期望输出.txt").read_text(encoding="utf-8")
    for 关, (text, expect) in enumerate([((HERE / "收藏.txt").read_text(encoding="utf-8"), expect1), (TEXT2, EXPECT2)], 1):
        with tempfile.TemporaryDirectory() as t:
            p = run(Path(t), text)
        名 = "收藏.txt" if 关 == 1 else "一份你没见过的收藏"
        if p.returncode != 0:
            print(f"✗ 第 {关} 关（{名}）：")
            hint_for_error(p.stderr)
            sys.exit(1)
        if compare(p.stdout, expect):
            print(f"✓ 第 {关} 关（{名}）通过")
        else:
            print(f"✗ 第 {关} 关（{名}）没通过")
            if 关 == 2:
                print("提示：第一关过了第二关没过，是不是把第一份收藏的答案写死在程序里了？")
            sys.exit(1)
    print("全部通过！挑战完成 🎉 来视频评论区报个到，先别贴代码，给别人留点思考的机会。")


if __name__ == "__main__":
    main()
