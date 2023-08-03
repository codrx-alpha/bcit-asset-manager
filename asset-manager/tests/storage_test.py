import os
import pytest

from pipeline import Storage, Show


def test_path_is_always_absolute():
    current_dir = os.getcwd()
    storage = Storage("relative")
    assert os.path.isabs(storage._root)
    assert storage._root.startswith(current_dir)


def test_create_show(tmpdir):
    storage = Storage(tmpdir.strpath)
    show = storage.create_show("my-show")
    assert isinstance(show, Show)


def test_create_show_makes_dir(tmpdir):
    storage = Storage(tmpdir.strpath)
    show = storage.create_show("my-show")
    assert os.path.exists(show._directory._root)


def test_create_show_already_exists(tmpdir):
    storage = Storage(tmpdir.strpath)
    tmpdir.join("my-show").ensure(dir=True)
    with pytest.raises(FileExistsError):
        storage.create_show("my-show")


def test_load_show(storage: Storage):
    show1 = storage.create_show("my-show")
    show2 = storage.load_show("my-show")
    assert show1.metadata() == show2.metadata()


def test_load_show_doesnt_exist(storage: Storage):
    with pytest.raises(FileNotFoundError):
        storage.load_show("my-other-show")


def test_list_shows(storage: Storage):
    storage.create_show("my-show1")
    storage.create_show("my-show2")
    storage.create_show("my-show3")
    storage.create_show("my-show4")

    expected = {
        "my-show4",
        "my-show1",
        "my-show3",
        "my-show2",
    }

    # use a set because we can't rely on the order of the list
    assert expected == set(storage.shows())


def test_list_shows_is_list(storage: Storage):
    assert isinstance(storage.shows(), list)
