# 1. write fibonacci function
# 2. write a decorator function that calculates time of function
# 3. use this decorator on fibonacci function
import datetime

def add_time(function):
    def wrapper(*args, **kwargs):
        t1 = datetime.datetime.now()
        output = function(*args, **kwargs)
        t2 = datetime.datetime.now()
        print(t2 - t1)

        return output

    return wrapper

# add_time(fibonacci)()
@add_time
def fibonacci(n):
    if n < 2:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(10))