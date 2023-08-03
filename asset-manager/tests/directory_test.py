from pipeline import Directory


def test_get_name(tmpdir):
    path = tmpdir.join("my-name").ensure(dir=True)
    dir = Directory(path.strpath)
    assert dir.name() == "my-name"
