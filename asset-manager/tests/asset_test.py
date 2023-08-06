import pytest
from pipeline import Shot, ShotMetadata


def test_asset_metadata(shot: Shot):
    asset = shot.create_asset("my-asset")
    assert asset.metadata().name == "my-asset"


def test_asset_load_metadata(shot: Shot):
    shot.create_asset("my-asset")
    asset = shot.load_asset("my-asset")
    assert asset.metadata().name == "my-asset"


def test_asset_copy_metadata(shot: Shot):
    asset = shot.create_asset("my-asset")
    meta = asset.metadata()
    meta.description = "new description"

    assert (
        asset.metadata().description != meta.description
    ), "changing metadata should not update asset automatically"


def test_asset_update_metadata(shot: Shot):
    asset = shot.create_asset("my-asset")
    meta = asset.metadata()
    meta.description = "new description"
    asset.update_metadata(meta)

    loaded = shot.load_asset("my-shot").metadata()
    assert loaded.description == meta.description


def test_asset_update_metadata_is_copy(shot: Shot):
    asset = shot.create_asset("my-asset")
    meta = asset.metadata()
    meta.description = "new description"
    asset.update_metadata(meta)

    meta.description = "something else"

    assert (
        asset.metadata().description != meta.description
    ), "updating metadata does not link the passed metadata instance"