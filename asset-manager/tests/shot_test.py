import pytest

from pipeline import Show, Storage, ShowMetadata


def test_shot_metadata(show: Show):
    shot = show.create_shot("my-shot")
    assert shot.metadata().name == "my-shot"


def test_shot_load_metadata(show: Show):
    show.create_shot("my-shot")
    shot = show.load_shot("my-shot")
    assert shot.metadata().name == "my-shot"


def test_shot_copy_metadata(show: Show):
    shot = show.create_shot("my-shot")
    meta = shot.metadata()
    meta.description = "new description"

    assert (
        shot.metadata().description != meta.description
    ), "changing metadata should not update shot automatically"


def test_shot_update_metadata(show: Show):
    shot = show.create_shot("my-shot")
    meta = shot.metadata()
    meta.description = "new description"
    shot.update_metadata(meta)

    loaded = show.load_shot("my-shot").metadata()
    assert loaded.description == meta.description


def test_shot_update_metadata_is_copy(show: Show):
    shot = show.create_shot("my-shot")
    meta = shot.metadata()
    meta.description = "new description"
    shot.update_metadata(meta)

    meta.description = "something else"

    assert (
        shot.metadata().description != meta.description
    ), "updating metadata does not link the passed metadata instance"


def test_shot_delete_removes_shots(show: Show):
    shot = show.create_shot("my-shot")
    shot.delete()

    with pytest.raises(FileNotFoundError):
        show.load_shot("my-shot")

    with pytest.raises(FileNotFoundError):
        shot.update_metadata(ShowMetadata("my-shot"))
