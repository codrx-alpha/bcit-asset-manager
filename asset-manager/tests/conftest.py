import pytest
import pipeline


@pytest.fixture
def storage(tmpdir) -> pipeline.Storage:
    return pipeline.Storage(tmpdir.strpath)


@pytest.fixture
def show(tmpdir) -> pipeline.Show:
    storage = pipeline.Storage(tmpdir.strpath)
    return storage.create_show("test-show")
