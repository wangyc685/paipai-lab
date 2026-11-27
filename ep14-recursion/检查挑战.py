"""检查 挑战.py：两关。第一关用 搬家记录.txt，第二关换一份你没见过的记录。"""
import ast
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RECORDS2 = '2\nA B\nA C\nB C\n\n3\nB C\n\n4\nA B\nA C\nC A\nB C\nA B\nC B\nA C\nB C\n\n3\nA C\nA B\nC B\nA C\nB A\nB C\nA C\nC B\nB C\n\n1\nA C\nC\n'
EXPECT2 = '第 1 份：搬完了，用了 3 步，最少要 3 步\n第 2 份：第 1 步出错，B 塔是空的\n第 3 份：还没搬完，C 塔上只有 2 个盘子\n第 4 份：搬完了，用了 9 步，最少要 7 步\n第 5 份：第 2 步看不懂：C\n'


def run(folder, records):
    shutil.copy(HERE / "挑战.py", folder / "挑战.py")
    (folder / "搬家记录.txt").write_text(records, encoding="utf-8")
    return subprocess.run([sys.executable, "-X", "utf8", "挑战.py"], cwd=folder, capture_output=True, text=True, encoding="utf-8", timeout=20)


def hint_for_error(err):
    last = err.strip().splitlines()[-1] if err.strip() else ""
    print("挑战.py 运行出错了：", last)
    if "RecursionError" in last:
        print("提示：递归停不下来了——你的递归函数有没有「出口」？（第 14 集 1:02 的竞猜）")
    elif "IndexError" in last:
        print("提示：有的行少了东西，或者从空列表里 pop 了。先检查这一步能不能搬，不能就 raise。")
    elif "KeyError" in last:
        print("提示：有的柱子名不是 A/B/C。这种行算「看不懂」。")
    elif "ValueError" in last:
        print("提示：int() 转不了的东西？看看你是怎么把一份记录切开的。")
    elif "FileNotFoundError" in last:
        print("提示：要在 ep14-recursion 文件夹里运行。")


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
    exc = [c for c in ast.walk(tree) if isinstance(c, ast.ClassDef) and any(isinstance(b, ast.Name) and b.id == "Exception" for b in c.bases)]
    if not exc:
        print("✗ 没找到继承 Exception 的异常类。要求 2：自己写一个 class 某某(Exception)。")
        return False
    if not any(isinstance(n, ast.Raise) for n in ast.walk(tree)):
        print("✗ 没找到 raise。要求 2：出错的时候 raise 你自己的异常类。")
        return False
    if not any(isinstance(n, ast.Try) for n in ast.walk(tree)):
        print("✗ 没找到 try/except。要求 2：在外面用 try/except 接住。")
        return False
    rec = False
    for f in ast.walk(tree):
        if isinstance(f, ast.FunctionDef):
            if any(isinstance(c, ast.Call) and isinstance(c.func, ast.Name) and c.func.id == f.name for c in ast.walk(f)):
                rec = True
    if not rec:
        print("✗ 没找到递归函数（在函数里调用它自己）。要求 1：「最少要几步」用递归算。")
        return False
    if any(isinstance(n, ast.BinOp) and isinstance(n.op, ast.Pow) for n in ast.walk(tree)):
        print("✗ 用了 **。要求 1：「最少要几步」用递归算，不许用 **。")
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
    for 关, (rec, expect) in enumerate([((HERE / "搬家记录.txt").read_text(encoding="utf-8"), expect1), (RECORDS2, EXPECT2)], 1):
        with tempfile.TemporaryDirectory() as t:
            p = run(Path(t), rec)
        名 = "搬家记录.txt" if 关 == 1 else "一份你没见过的记录"
        if p.returncode != 0:
            print(f"✗ 第 {关} 关（{名}）：")
            hint_for_error(p.stderr)
            sys.exit(1)
        if compare(p.stdout, expect):
            print(f"✓ 第 {关} 关（{名}）通过")
        else:
            print(f"✗ 第 {关} 关（{名}）没通过")
            if 关 == 2:
                print("提示：第一关过了第二关没过，是不是把第一份记录的答案写死在程序里了？")
            sys.exit(1)
    print("全部通过！挑战完成 🎉 来视频评论区报个到，先别贴代码，给别人留点思考的机会。")


if __name__ == "__main__":
    main()
