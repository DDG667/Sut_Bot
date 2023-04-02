import wikipedia

wikipedia.set_lang("zh")


class wiki:
    def __init__(self, word: str) -> None:
        self.word = word

    def search(self) -> list:
        return wikipedia.search(self.word)

    def page(self, name: str) -> wikipedia.WikipediaPage:
        return wikipedia.page(name)

    def summary(self, name: str) -> str:
        return wikipedia.summary(name)


if __name__ == "__main__":
    print(wikipedia.search("ATRI my dear"))
    print(wikipedia.summary("ATRI -My Dear Moments-"))
    print(wikipedia.page("ATRI -My Dear Moments-").content)
