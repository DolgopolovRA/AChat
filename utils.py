import traceback


def get_func_name():
    stack = traceback.extract_stack()
    return stack[-2][2]
