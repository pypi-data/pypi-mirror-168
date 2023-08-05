from daner import daner


def test_get_key():
    assert daner._get_key("-u") == "u"
    assert daner._get_key("--user") == "user"


def test_parse_args():
    assert daner._parse_args(["--name", "milisp"]) == {"name": "milisp"}


def test_parse_mixin_args():
    assert daner._parse_args(
        ["--name", "milisp", "-p", "8000"], alias={"p": "port"}
    ) == {"name": "milisp", "p": "8000"}


def test_set_alias():
    assert daner._set_alias(alias={"u": "username"}, obj_in={"u": "milisp"}) == {
        "username": "milisp"
    }


def test_check_email():
    assert daner.check_email({"email": "milisp@pm.me"}, "email")
