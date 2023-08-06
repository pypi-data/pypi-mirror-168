# Pouty: a very silly library bringing weird C++ features to Python since 2022

Do you like Python? Wanna use std::cout in it? No? I didn't ask!

`pouty` is a Python package that will make you pout with it's ability to use C++ style IO in Python.

## FAQ:

- **Is it fast?**
  No.
- **Does C++ I/O even make sense in this context?**
  That's for you to judge.
- **Is it faster than Python's print()?**
  While it may *occasionally* avoid a string creation or contcatenation, it does so through multiple operator overloads and several function calls + type checks. Therefore, no.
- **Why is C++'s iostream fast?**
  C++ is a compiled language with static typing and function call inlining.
- **Why make this?** 
  Because I can.


## Example code (`examples/test.py`):

```python
from pouty.iostream import *;
import random;

std.cout << "Hello, world!" << std.endl

class CustomOutput: #custom operator<< and operator>> overload supported
    is_pouty_stream = True
    def __init__(self) -> None:
        self.x = ref(0)
        pass

    def __lshift__(self, other: any) -> None:
        other << self.x[...]
    
    def __rshift__(self, other: any) -> None:
        other >> self.x

# Python [unfortunately, perhaps fortunately!] does not have implicit reference parameters.
x = ref(0)
std.cin >> x
std.cout << x << std.endl # uses the __str__ method of ref
std.cout << x[...] << std.endl # dereferences the ref and prints the int

x = CustomOutput()
std.cin >> x
std.cout << x << std.endl

x = random.random() #precision is supported too!
std.cout << x << std.endl
std.cout << std.precision(3) 
std.cout << x << std.endl


using_namespace(globals(), "std")
cout << "Hello, world!" << endl # bringing namespace pollution into Python since 2022 :)

from pouty.stdlib.h import *;

printf("%s", "Hello, world!")
printf("%d", 123) #note that precision is not supported yet here (feel free to contrubute it)
puts("Hello, world!")
```

## Installation

`pip install pouty`

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss the change.
