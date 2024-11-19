def format_left(string, length):
    return string + " "*(length - len(string))
def format_center(string, length):
    return ' '*((n := length - len(string))//2) + string + ' '*((n+n%2)//2)
