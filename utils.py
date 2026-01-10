digits = set("0123456789")

def input_unsigned_int(prompt: str, lb = None, ub = None, err = None) -> int:
    num = None
    check = lambda x: (x >= lb if type(lb) == int else True) and (x < ub if type(ub) == int else True)
    while num == None:
        user_input = input(prompt)
        if set(user_input).issubset(digits):
            num = int(user_input)
        if num == None or not check(num):
            if err != None:
                print(err)
            num = None
    return num

