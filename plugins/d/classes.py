from .amath import fib, bs


class thing:
    def __init__(self, name: str, __score: int, docs: str) -> None:
        self.__sco: int = __score
        self.name: str = name
        self.doc: str = docs

    def __repr__(self) -> str:
        return self.name

    def aget_cost(self, num: int, have: int) -> int:
        return -sum([fib(i + have + 2) * self.__sco for i in range(num)])


class user:
    def __init__(self, id: int) -> None:
        self.id: int = id
        self.__limit: int = 0
        self.__score: int = 0
        self.things: dict[thing, int] = {}

    def __repr__(self) -> str:
        return f"{self.id}"

    def aset_score(self, num: int) -> str:
        self.__score: int = num
        return "修改成功！"

    def aget_score(self) -> int:
        return self.__score

    def achange_score(self, num: int) -> tuple[int, bool]:
        if num > 0:
            self.__score += num
            return (
                self.__score,
                True,
            )
        elif -num > self.__score:
            return (
                -num - self.__score,
                False,
            )
        self.__score += num
        return (
            self.__score,
            True,
        )

    def aset_thing(self, thing: thing, num: int) -> str:
        self.things[thing] = num
        return "修改成功！"

    def aget_thing(self, thing: thing) -> int:
        return self.things.get(thing, 0)

    def achange_thing(self, thing: thing, num: int) -> tuple[int, bool]:
        if num > 0:
            self.things[thing] += num
            return (
                self.things[thing],
                True,
            )
        elif -num > self.things[thing]:
            return (
                -num - self.things[thing],
                False,
            )
        self.things[thing] += num
        return self.things[thing], True

    def abuy(self, thing: thing, num: int) -> str:
        cost: int = thing.aget_cost(num, self.things[thing])
        return_tuple: tuple[int, bool] = self.achange_score(cost)
        if return_tuple[1]:
            self.things[thing] += num
            return f"够买成功！\n当前剩余 {self.things[thing]}个 {thing}\n剩余积分：{return_tuple[0]}"
        return f"你只有 {return_tuple[0]} 积分，无法购买 {num} 个 {thing} ！\n所需积分：{cost}"

    def auplevel(self) -> str:
        cost: int = fib(self.__limit) * 100
        if cost > self.__score:
            return f"你只有 {self.__score} 积分，无法增加上限！\n所需积分：{-cost}\n当前上限：{self.__limit} 个"
        self.__score -= cost
        self.__limit += 1
        return f"使用积分增加上限成功！\n 当前上限：{self.__limit} 个\n剩余积分：{self.__score}"


class users:
    def __init__(self, users: list[user]) -> None:
        self.data: dict[int, user] = {i.id: i for i in users}
        self.__index: int = -1
    def get_users(self)->list[user]:
        return [i for i in self.data.values()]

    def __repr__(self) -> str:
        return str([i.id for i in self.data.values()])

    def __getitem__(self, item: int) -> user:
        try:
            return self.data[item]
        except KeyError:
            self.data.update({item:user(item)})
            return self.data[item]

    def __iter__(self):
        return self

    def __next__(self) -> user:
        try:
            self.__index += 1
            return self.get_users()[self.__index]
        except IndexError:
            raise StopIteration

    def add_user(self,us: list[user]):
        self.data.update({i.id: i for i in us})

    def aget_uids(self) -> list[int]:
        return [i.id for i in self.data.values()]

    def aget_scores_list(self) -> list[int]:
        return [i.aget_score() for i in self.data.values()]

    def aget_things_list(self, thing: thing) -> list[int]:
        return [i.aget_thing(thing) for i in self.data.values()]

    def aget_scores_top(self) -> list[int]:
        return bs(self.aget_uids(), self.aget_scores_list())

    def aget_things_top(self, thing: thing) -> list[int]:
        return bs(
            self.aget_uids(),
            [i.aget_thing(thing) for i in self.data.values()],
        )


class operations:
    def __init__(self, us: users) -> None:
        self.users: users = us


if __name__ == "__main__":
    from asyncio import run

    def main():
        su: user = user(2963221776)
        su1: user = user(296322176)
        su2: user = user(296322177)
        kiss: thing = thing("亲亲", 10, "")

        su.things = {kiss: 10}
        a: users = users([su, su1, su2])
        su.achange_score(8)
        su1.achange_score(0)
        su2.achange_score(2)
        print(su.abuy(kiss, 1))
        print(a.aget_scores_list())
        print(a.aget_things_top(kiss))
        print(a.aget_things_list(kiss))
        print(a.aget_scores_top())
        print(a)
        for i in a:
            print(i)
