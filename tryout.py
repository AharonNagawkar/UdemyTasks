
# calculate(make_float=False, operation='add', message='You just added', first=2, second=4) # "You just added 6"



def calculate(**kwargs):
    if "add" in kwargs.values():
        result = kwargs["first"] + kwargs["second"]
    elif "subtract" in kwargs.values():
        result = kwargs["first"] - kwargs["second"]
    elif "multiply" in kwargs.values():
        result = kwargs["first"] * kwargs["second"]
    else:
        result = kwargs["first"] / kwargs["second"]
    if kwargs["make_float"]:
        return "{} {}".format(kwargs.get("message"),float(result))
    else:
        return "{} {}".format(kwargs.get("message"),int(result))


print(calculate(make_float=False, operation='add', message='You just added', first=2, second=4))# "You just added 6"
print(calculate(make_float=True, operation='divide', first=3.5, second=5)) # "The result is 0.7"


# from keyword import iskeyword
#
# def contains_keyword(*args):
#     return any([iskeyword(word) for word in args])
#
#
# print(contains_keyword('hello','hi'))