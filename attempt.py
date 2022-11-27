# def shout(fn):
#     def internal(*args):
#         return fn(*args).upper()
#     return internal
#
# @shout
# def greet(name):
#     return f"hi , I'm {name}."
# @shout
# def order(main,side):
#     return f"hi, I'd like the {main}, with a side of {side}, please."
#
#
# #print(greet('sara'))
# print(order('Coke','fries'))


# from functools import wraps
#
# def ensure_authorized(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         if any(key for key in kwargs.keys() if key == 'role'):
#             if kwargs['role'] == 'admin':
#                 return fn(*args, **kwargs)
#             else:
#                 return("Unauthorized")
#         else:
#         return("Unauthorized")
#     return wrapper


