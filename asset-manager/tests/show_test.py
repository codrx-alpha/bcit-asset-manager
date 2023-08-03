import pytest

from pipeline import Show, Storage, ShowMetadata


def test_show_metadata(storage: Storage):
    show = storage.create_show("my-show")
    assert show.metadata().name == "my-show"


def test_show_load_metadata(storage: Storage):
    storage.create_show("my-show")
    show = storage.load_show("my-show")
    assert show.metadata().name == "my-show"


def test_show_copy_metadata(storage: Storage):
    show = storage.create_show("my-show")
    meta = show.metadata()
    meta.description = "new description"

    assert (
        show.metadata().description != meta.description
    ), "changing metadata should not update show automatically"


def test_show_update_metadata(storage: Storage):
    show = storage.create_show("my-show")
    meta = show.metadata()
    meta.description = "new description"
    show.update_metadata(meta)

    loaded = storage.load_show("my-show").metadata()
    assert loaded.description == meta.description


def test_show_update_metadata_is_copy(storage: Storage):
    show = storage.create_show("my-show")
    meta = show.metadata()
    meta.description = "new description"
    show.update_metadata(meta)

    meta.description = "something else"

    assert (
        show.metadata().description != meta.description
    ), "updating metadata does not link the passed metadata instance"


def test_show_delete_removes_shots(storage: Storage):
    show = storage.create_show("my-show")
    shot = show.create_shot("shot1")

    show.delete()

    with pytest.raises(FileNotFoundError):
        storage.load_show("my-show")

    with pytest.raises(FileNotFoundError):
        show.update_metadata(ShowMetadata("my-show"))


def test_list_shots(show: Show):
    show.create_shot("my-shot1")
    show.create_shot("my-shot2")
    show.create_shot("my-shot3")
    show.create_shot("my-shot4")

    expected = {
        "my-shot4",
        "my-shot1",
        "my-shot3",
        "my-shot2",
    }

    # use a set because we can't rely on the order of the list
    assert expected == set(show.shots())


def test_list_shots_is_list(show: Show):
    assert isinstance(show.shots(), list)
