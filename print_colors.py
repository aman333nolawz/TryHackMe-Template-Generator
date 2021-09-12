import colorama

colorama.init()


def red(*args, **kwargs):
    print(colorama.Fore.RED, end="")
    print(*args, **kwargs)


def green(*args, **kwargs):
    print(colorama.Fore.GREEN, end="")
    print(*args, **kwargs)
