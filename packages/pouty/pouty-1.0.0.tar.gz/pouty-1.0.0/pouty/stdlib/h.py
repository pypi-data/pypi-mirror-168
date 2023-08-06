import re
# decimal precision not supported yet
def printf(format, value):
    format = re.sub(r'(%[0-9]*[a-zA-Z])', "{}", format)
    print(format.format(value))
def puts(value):
    print(value)