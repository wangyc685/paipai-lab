"""
派派整活实验室 · 第 11 集：训练贪吃蛇 AI 死了 1891 次，它竟然学会了……

一条小 AI 蛇，在 10×10 的棋盘上玩贪吃蛇。它一开始什么都不会，全靠"得分"一点点学。
它的脑子就是一个字典：账本[情况] = [直走值几分, 左转值几分, 右转值几分]。

怎么跑（需要 Python 3.8 以上，不用装任何别的东西）：
    python snake_ai.py          三条规则都训练一遍，打印成绩（和视频里的数字一样）
    python snake_ai.py 1        只跑规则一
    python snake_ai.py 1 看     训练完，在终端里放一局给你看（规则一能看到它"躺平"）

想自己训？去改下面的 算得分() 函数，改完再跑一遍，看看你的 AI 学成了什么样。
变量名是中文的，Python 3 完全支持，放心跑。
"""
import random
import sys
import time
from collections import deque

棋盘大小 = 10
方向表 = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # 上、右、下、左
动作名 = ["直走", "左转", "右转"]
最多步数 = 1000  # 一局最多走这么多步
饿死步数 = 200  # 规则二、三：这么多步没吃到苹果，这局就算结束
训练局数 = 2000


# ── 规则：每走一步给多少分（你来训，就改这里）────────────────────────────────────
def 算得分(规则, 吃到苹果, 撞死了):
    if 规则 == 1:
        得分 = 1                 # 活着，每走一步给 1 分
        if 撞死了: 得分 = -10     # 撞死，扣 10 分
    else:
        得分 = 0
        if 吃到苹果: 得分 = 10     # 吃到苹果，加 10 分
        if 撞死了: 得分 = -10      # 撞死，扣 10 分
    return 得分


# ── 贪吃蛇游戏 ──────────────────────────────────────────────────────────────────
class 游戏:
    def __init__(self, 随机):
        self.随机 = 随机
        中 = 棋盘大小 // 2
        self.身体 = deque([(中, 中), (中 - 1, 中), (中 - 2, 中)])  # 第一个是头
        self.朝向 = 1  # 一开始朝右
        self.苹果 = self.放苹果()
        self.步数 = 0
        self.没吃到 = 0
        self.吃了 = 0

    def 放苹果(self):
        空格 = [(x, y) for x in range(棋盘大小) for y in range(棋盘大小) if (x, y) not in self.身体]
        return self.随机.choice(空格) if 空格 else None

    def 挡住了(self, 格):
        x, y = 格
        if not (0 <= x < 棋盘大小 and 0 <= y < 棋盘大小):
            return True
        return 格 in list(self.身体)[:-1]  # 尾巴下一步会挪走，不算挡

    def 转向(self, 动作):
        return self.朝向 if 动作 == 0 else (self.朝向 - 1) % 4 if 动作 == 1 else (self.朝向 + 1) % 4

    def 前方(self, 朝向):
        x, y = self.身体[0]
        dx, dy = 方向表[朝向]
        return (x + dx, y + dy)

    def 数空地(self, 格):
        """往这格走的话，还剩多大地方能活动（数一数连成一片的空格）。"""
        if self.挡住了(格):
            return 0
        身子 = set(list(self.身体)[:-1])
        看过 = {格}
        要看 = [格]
        while 要看:
            x, y = 要看.pop()
            for dx, dy in 方向表:
                邻 = (x + dx, y + dy)
                if 0 <= 邻[0] < 棋盘大小 and 0 <= 邻[1] < 棋盘大小 and 邻 not in 看过 and 邻 not in 身子:
                    看过.add(邻)
                    要看.append(邻)
        return len(看过)

    def 看到的情况(self, 戴眼镜):
        """AI 能看到的全部信息。它只认这些，别的一概不知道。"""
        头x, 头y = self.身体[0]
        果x, 果y = self.苹果
        危险 = tuple(int(self.挡住了(self.前方(self.转向(a)))) for a in range(3))  # 直走/左转/右转会不会撞
        苹果方位 = (int(果y < 头y), int(果x > 头x), int(果y > 头y), int(果x < 头x))  # 苹果在上/右/下/左
        情况 = 危险 + (self.朝向,) + 苹果方位
        if 戴眼镜:  # 规则三：配了眼镜，能数空地
            够转身 = len(self.身体) + 1
            情况 += tuple(int(self.数空地(self.前方(self.转向(a))) >= 够转身) for a in range(3))
        return 情况

    def 走一步(self, 动作, 规则):
        self.朝向 = self.转向(动作)
        下一格 = self.前方(self.朝向)
        self.步数 += 1
        self.没吃到 += 1
        撞死了 = self.挡住了(下一格)
        吃到苹果 = not 撞死了 and 下一格 == self.苹果
        得分 = 算得分(规则, 吃到苹果, 撞死了)
        if 撞死了:
            撞墙 = not (0 <= 下一格[0] < 棋盘大小 and 0 <= 下一格[1] < 棋盘大小)
            return 得分, True, "撞墙" if 撞墙 else "咬到自己"
        self.身体.appendleft(下一格)
        if 吃到苹果:
            self.吃了 += 1
            self.没吃到 = 0
            self.苹果 = self.放苹果()
            if self.苹果 is None:
                return 得分, True, "占满全屏"
        else:
            self.身体.pop()
        if self.步数 >= 最多步数:
            return 得分, True, "活到时间上限"
        if 规则 != 1 and self.没吃到 >= 饿死步数:
            return 得分, True, "饿到时间上限"
        return 得分, False, None


# ── 训练：一边玩，一边记账 ─────────────────────────────────────────────────────────
def 训练(规则, 种子, 局数=None):
    局数 = 局数 or 训练局数
    随机 = random.Random(种子)
    账本 = {}  # AI 的脑子：一个字典
    戴眼镜 = 规则 == 3
    撞死次数 = 0
    for 第几局 in range(局数):
        乱试概率 = max(0.01, 1.0 * (0.995 ** 第几局))  # 一开始多乱试，越往后越照着账本走
        g = 游戏(random.Random(种子 * 100003 + 第几局))
        情况 = g.看到的情况(戴眼镜)
        while True:
            分数 = 账本.setdefault(情况, [0.0, 0.0, 0.0])  # 查一下：这种情况下，直走、左转、右转各值几分
            动作 = 随机.randrange(3) if 随机.random() < 乱试概率 else max(range(3), key=lambda a: 分数[a])
            得分, 结束, 原因 = g.走一步(动作, 规则)
            新情况 = None if 结束 else g.看到的情况(戴眼镜)
            以后最多能拿的分 = 0 if 结束 else max(账本.setdefault(新情况, [0.0, 0.0, 0.0]))
            目标 = 得分 + 0.9 * 以后最多能拿的分  # 以后的分打九折，眼前的更实在
            账本[情况][动作] += 0.1 * (目标 - 账本[情况][动作])  # 往目标挪一小步
            if 结束:
                break
            情况 = 新情况
        if 原因 in ("撞墙", "咬到自己"):
            撞死次数 += 1
    return 账本, 撞死次数


# ── 测试：关掉"乱试"，让它光照着账本走 ─────────────────────────────────────────────
def 测试(账本, 规则, 局数=200, 种子=999):
    戴眼镜 = 规则 == 3
    成绩 = []
    for k in range(局数):
        g = 游戏(random.Random(种子 + k))
        while True:
            分数 = 账本.get(g.看到的情况(戴眼镜), [0.0, 0.0, 0.0])
            动作 = max(range(3), key=lambda a: 分数[a])
            _, 结束, 原因 = g.走一步(动作, 规则)
            if 结束:
                break
        成绩.append((g.步数, g.吃了, 原因))
    return 成绩


def 放一局(账本, 规则, 种子=999, 帧间隔=0.05):
    """在终端里放一局（按 Ctrl+C 停）。"""
    戴眼镜 = 规则 == 3
    g = 游戏(random.Random(种子))
    while True:
        分数 = 账本.get(g.看到的情况(戴眼镜), [0.0, 0.0, 0.0])
        动作 = max(range(3), key=lambda a: 分数[a])
        _, 结束, 原因 = g.走一步(动作, 规则)
        画面 = [["·"] * 棋盘大小 for _ in range(棋盘大小)]
        if g.苹果:
            画面[g.苹果[1]][g.苹果[0]] = "●"
        for i, (x, y) in enumerate(g.身体):
            if 0 <= x < 棋盘大小 and 0 <= y < 棋盘大小:
                画面[y][x] = "◆" if i == 0 else "■"
        print("\033[H\033[J", end="")
        print("\n".join(" ".join(行) for 行 in 画面))
        print(f"第 {g.步数} 步  吃了 {g.吃了} 个苹果")
        if 结束:
            print(f"结束：{原因}")
            return
        time.sleep(帧间隔)


# 视频里三条规则用的随机种子（换种子，数字会变，但结论不变）
视频种子 = {1: 12, 2: 13, 3: 14}
规则名 = {1: "规则一：活着就加分", 2: "规则二：吃到苹果才加分", 3: "规则三：吃到苹果加分 + 配眼镜（能数空地）"}

if __name__ == "__main__":
    要跑 = [int(a) for a in sys.argv[1:] if a in ("1", "2", "3")] or [1, 2, 3]
    for 规则 in 要跑:
        print(f"\n== {规则名[规则]}（训练 {训练局数} 局……）")
        账本, 撞死次数 = 训练(规则, 视频种子[规则])
        成绩 = 测试(账本, 规则)
        原因统计 = {}
        for _, _, 原因 in 成绩:
            原因统计[原因] = 原因统计.get(原因, 0) + 1
        print(f"训练时撞死：{撞死次数} 次")
        print(f"测试 {len(成绩)} 局：平均吃 {sum(c[1] for c in 成绩) / len(成绩):.2f} 个苹果，最多 {max(c[1] for c in 成绩)} 个，平均活 {sum(c[0] for c in 成绩) / len(成绩):.1f} 步")
        print(f"每局怎么结束的：{原因统计}")
        print(f"账本里一共记了 {len(账本)} 种情况")
        if "看" in sys.argv[1:]:
            input("按回车，放一局给你看……")
            放一局(账本, 规则)
