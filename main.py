from random import randint
from typing import List
from sys import argv
from subprocess import Popen, PIPE
from io import TextIOWrapper
from os import path

# テストケース数
TESTCASE_NUM = 100
# n ** m の upper_bound
POW_N_M_UPPERBOUND = 10 ** 5
# k の upper_bound
K_UPPERBOUND = 5


def TEN(n): return [1, 10, 100, 1000, 10000, 100000][n]


def naive(n: int, k: int, m: int, t: int, a: List[int]):
    """naive solution

    与えらえた入力に対して愚直解を計算して返す関数.
    n ** m が POW_N_M_UPPERBOUND 以下である必要がある.

    Args:
        n (int): 入力の n .
        k (int): 入力の k .
        m (int): 入力の m .
        t (int): 入力の t .
        a (List[int]): 入力の a .

    Raises:
        ValueError: n ** m が POW_N_M_UPPERBOUND より大きいときに返す.

    Returns:
        List[int]: 答えを格納した配列.
    """

    if n ** m > POW_N_M_UPPERBOUND:
        raise ValueError

    def add(i, j):
        res = 0
        for d in range(k):
            if d < t and i % 10 + j % 10 >= 10:
                return -1
            res += (i + j) % 10 * TEN(d)
            i //= 10
            j //= 10
        return res

    ans = [0] * TEN(k)

    def dfs(depth, s):
        if s == -1:
            return
        if depth == m:
            ans[s] += 1
            return
        for x in a:
            dfs(depth + 1, add(s, x))
    dfs(0, 0)
    return [x % 120586241 for x in ans]


def gen():
    """generator

    ランダムなテストケースを生成する関数.

    Returns:
        int: N 
        int: K
        int: M
        int: T
        List[int] : A
    """
    while True:
        N = randint(1, 20)
        M = randint(2, 20)
        if N**M < POW_N_M_UPPERBOUND:
            break
    while True:
        K = randint(1, K_UPPERBOUND)
        T = randint(0, K_UPPERBOUND)
        if T <= K:
            break
    A_MIN = 0
    A_MAX = TEN(K) - 1
    A = []

    while len(A) < N:
        # 雑に作ると 0 だらけになってしまうので
        # 0 が多いものを優先する
        if len(A) == 0 and randint(1, 2) == 1:
            A.append(0)
        else:
            while True:
                x = randint(A_MIN, A_MAX)
                s = "0" * (K - len(str(x))) + str(x)
                if s.count('0') >= K - 1:
                    A.append(x)
                    break
                elif s.count('0') >= K - 2 and randint(1, 100) == 1:
                    A.append(x)
                    break

    assert 1 <= N <= TEN(5)
    assert 1 <= K <= 5
    assert 2 <= M <= 10 ** 18
    assert 0 <= T <= K
    assert len(A) == N
    for x in A:
        assert 0 <= x < TEN(K)

    return N, K, M, T, A


def main():
    """main

    プログラムが小さいケースで適切に動いているかをテストする関数.

    """
    if len(argv) < 2:
        filename = "a.exe"
    else:
        filename = argv[1]

    assert path.exists(filename)

    for testcase in range(1, TESTCASE_NUM + 1):
        p = Popen(filename, stdin=PIPE, stdout=PIPE)
        wrapper = TextIOWrapper(p.stdin)
        print("testcase :", testcase, " : ", end='', flush=True)
        n, k, m, t, a = gen()
        expected = naive(n, k, m, t, a)

        def dump():
            print("hack.in, hack.out を生成中…")
            with open("hack.in", mode='w') as f:
                print(n, k, m, t, file=f)
                print(*a, file=f)
            with open("hack.out", mode='w') as f:
                print(*expected, sep='\n', file=f)
            print("生成完了. プログラムを終了します.")

        print("プログラムを実行中…")
        print(n, k, m, t, file=wrapper, flush=True)
        print(*a, file=wrapper, flush=True)
        output = list(map(int, p.stdout.read().decode().split()))

        if len(output) != len(expected):
            print("答えの要素数が一致しません.", flush=True)
            print("output :", len(output))
            print("expected :", len(expected))
            dump()
            exit(1)
        for i in range(len(expected)):
            if output[i] != expected[i]:
                print(i, "番目の要素が一致しません.")
                print("output :", output[i])
                print("expected :", expected[i])
                dump()
                exit(1)

    print(TESTCASE_NUM, " ケース終了. 全ケース OK です.")


if __name__ == '__main__':
    main()
