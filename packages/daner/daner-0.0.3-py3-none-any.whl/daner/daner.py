import asyncio
import inspect
import re
import sys
from functools import wraps


args = sys.argv
commands = []


def echo_red(text: str):
    red = "\033[31m"
    print(red + text)


def _get_key(arg: str) -> str:
    """
    :arg str: -u or --user
    """
    if arg.count("-") == 2:
        key = arg[2:]
    elif arg.count("-") == 1:
        key = arg[1:]
    return key


def _set_alias(alias: dict, obj_in: dict) -> dict:
    """
    :alias dict: {"u": "username"}
    :obj_in dict: {"u": "milisp"}
    :return dict: {"username": "milisp"}
    """
    if isinstance(alias, dict):
        for old, new in alias.items():
            obj_in[new] = obj_in[old]
            del obj_in[old]
        return obj_in


def _parse_args(args: list, alias: dict = {}) -> dict:
    """
    :args list: ["--name", "milisp"]
    :return dict: {"name": "milisp"}
    """
    if not alias and any([arg.count("-") == 1 for arg in args]):
        echo_red("no alias")
        exit(1)
    obj_in = {}
    for i, arg in enumerate(args):
        if i % 2 == 0:
            key = _get_key(arg)
            obj_in[key] = None
        else:
            key = _get_key(args[i - 1])
            obj_in[key] = arg
    return obj_in


def check_email(obj_in: dict, k: str) -> bool | None:
    """
    :obj_in dict: {"email": "milisp@pm.me"}
    :k str: "email"
    :return True | None:
    """

    if k == "email":
        if not re.search("(\w+@\w+.\w+)", obj_in[k]) or not re.match(  # noqa
            "[a-z]", obj_in[k]
        ):
            echo_red("error email")
            exit(1)
        return True


def dong(alias: dict = {}, help: str = "", sync: bool = False):
    """
    example:
    @dong()
    async def hello(name, age):
        print(name, age)

    """

    def arun(func):
        @wraps(func)
        def wrapper():
            if len(args) > 1:
                sub_cmd = args[1]
            else:
                sub_cmd = ""
            if len(args) > 2:
                new_args = args[2:]
            else:
                new_args = []

            # add command for help
            sig = inspect.signature(func)
            commands.append({func.__name__: str(sig)})

            if sub_cmd == func.__name__:
                obj_in = _parse_args(new_args, alias)
                if alias:
                    obj_in = _set_alias(alias, obj_in)
                annotations = inspect.get_annotations(func)
                if annotations:
                    for k, v in annotations.items():
                        if k in obj_in:
                            if v == int:
                                if not obj_in[k].isdigit():
                                    echo_red(k + " shou be int.")
                                    exit(1)
                            check_email(obj_in, k)

                if sync:
                    func(**obj_in)
                else:
                    asyncio.run(func(**obj_in))

        return wrapper()

    return arun


def run():
    """show help detail"""
    args = sys.argv
    if len(args) < 2 or (len(args) < 3 and args[1] in ["-h", "--help"]):
        for cmd in commands:
            print(cmd)
