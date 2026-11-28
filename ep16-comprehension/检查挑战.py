"""检查 挑战.py：两关。第一关用 图纸.txt，第二关换一张你没见过的图纸。"""
import ast
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEXT2 = '#..\n.#.\n..##\n###\n'
EXPECT2 = '左右翻过来：\n...#\n..#.\n##..\n.###\n放大两倍：\n##......\n##......\n..##....\n..##....\n....####\n....####\n######..\n######..\n要绣 7 针，空着 9 格\n左右对称的行： []\n'


def run(folder, text):
    shutil.copy(HERE / "挑战.py", folder / "挑战.py")
    (folder / "图纸.txt").write_text(text, encoding="utf-8")
    return subprocess.run([sys.executable, "-X", "utf8", "挑战.py"], cwd=folder, capture_output=True, text=True, encoding="utf-8", timeout=20)


def hint_for_error(err):
    last = err.strip().splitlines()[-1] if err.strip() else ""
    print("挑战.py 运行出错了：", last)
    if "IndexError" in last:
        print("提示：是不是有的行比别的行短？先补齐再干别的。")
    elif "KeyError" in last:
        print("提示：字典里没有这个键——数针数的时候，你的字典里都有哪几个键？")
    elif "FileNotFoundError" in last:
        print("提示：要在 ep16-comprehension 文件夹里运行。")
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


def check_rules(src):
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        print("✗ 挑战.py 有语法错误：", e)
        return False
    funcs = {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    for f in ("翻转", "放大"):
        if f not in funcs:
            print(f"✗ 没找到函数 {f}。要求 1：写两个函数 翻转(图) 和 放大(图)。")
            return False
    lc = sum(isinstance(n, ast.ListComp) for n in ast.walk(tree))
    dc = sum(isinstance(n, ast.DictComp) for n in ast.walk(tree))
    if lc < 3:
        print(f"✗ 只找到 {lc} 个列表推导式。要求 2：至少 3 个 [... for ...]。")
        return False
    if dc < 1:
        print("✗ 没找到字典推导式。要求 2：至少 1 个 {...: ... for ...}。")
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
    for 关, (text, expect) in enumerate([((HERE / "图纸.txt").read_text(encoding="utf-8"), expect1), (TEXT2, EXPECT2)], 1):
        with tempfile.TemporaryDirectory() as t:
            p = run(Path(t), text)
        名 = "图纸.txt" if 关 == 1 else "一张你没见过的图纸"
        if p.returncode != 0:
            print(f"✗ 第 {关} 关（{名}）：")
            hint_for_error(p.stderr)
            sys.exit(1)
        if compare(p.stdout, expect):
            print(f"✓ 第 {关} 关（{名}）通过")
        else:
            print(f"✗ 第 {关} 关（{名}）没通过")
            if 关 == 2:
                print("提示：第一关过了第二关没过？这张图纸的行长短不一样，有没有先补齐？是不是把答案写死了？")
            sys.exit(1)
    print("全部通过！挑战完成 🎉 来视频评论区报个到，先别贴代码，给别人留点思考的机会。")


if __name__ == "__main__":
    main()
