def yes_or_no():
    choice =
    for answer in choice:
        yield answer


gen = yes_or_no()

next(gen)
next(gen)
next(gen)
next(gen)
