from daner import dong, run


@dong()
async def say(name):
    print(f"say {name}")


@dong(alias={"u": "username"})
async def superuser(username: str):
    print(username)


@dong(sync=True)
def create(name: str, age: int, email: str = None):
    print(f"create {name} {age} {email}")


if __name__ == "__main__":
    run()
