def fib(n: int) -> int:
    sqrt5 = 5**0.5
    fibN = ((1 + sqrt5) / 2) ** n - ((1 - sqrt5) / 2) ** n
    return round(fibN / sqrt5)


def qs(l: list[int], i: int = 0, j: int = 0) -> None:
    def pt(l: list[int], i: int, j: int) -> int:
        i = i - 1
        p = l[j]

        for j in range(i, j):
            if l[j] <= p:

                i = i + 1
                l[i], l[j] = l[j], l[i]

        l[i + 1], l[j] = l[j], l[i + 1]
        return i + 1

    j = len(l) - 1
    if i < j:

        p = pt(l, i, j)

        qs(l, i, p - 1)
        qs(l, p + 1, j)


def bs(ids: list[int], values: list[int]) -> list[int]:
    lov: int = len(values)
    for i in range(lov):
        for j in range(lov - i):
            if values[i] < values[j]:
                ids[i], ids[j] = ids[j], ids[i]
    return ids
