from pprint import pprint as print
from typing import Any

import redis
from models import Author, Quote
from redis_lru import RedisLRU

# docker run --name redis-cache -d -p 6379:6379 redis

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str) -> list[str | None]:
    print(f"Find by tag: {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_author(author: str) -> list[list[Any]]:
    print(f"Find by author: {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


def main():
    while True:
        print(
            """Введіть команду дляпошуку цитат\n name: ім'я -> шукає за ім'ям автора\n tag: теги -> шукає за тегами, через кому без пробілу\n exit -> для виходу"""
        )
        user_input = input(">>> ")
        comand, *args = user_input.split()
        if comand.lower() == "name:":
            print(find_by_author(" ".join(args)))
        elif comand.lower() == "tag:":
            args = args[0].split(",")
            for tag in args:
                print(find_by_tag(tag))
        elif comand == "exit":
            print("Exiting...")
            break
        else:
            print("Нічого не знайдено, перевірте правильність написання")


if __name__ == "__main__":
    main()
