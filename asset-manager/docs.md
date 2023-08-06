# Asset Manager API Documentation

## Table of Contents

* [storage.py](#storage)
  * [Storage](#storage.Storage)
    * [\_\_init\_\_](#storage.Storage.__init__)
    * [shows](#storage.Storage.shows)
    * [load\_show](#storage.Storage.load_show)
    * [create\_show](#storage.Storage.create_show)
* [directory.py](#directory)
  * [Directory](#directory.Directory)
    * [create](#directory.Directory.create)
    * [name](#directory.Directory.name)
    * [load\_metadata](#directory.Directory.load_metadata)
    * [save\_metadata](#directory.Directory.save_metadata)
    * [delete](#directory.Directory.delete)
* [show.py](#show)
  * [ShowMetadata](#show.ShowMetadata)
  * [Show](#show.Show)
    * [\_\_init\_\_](#show.Show.__init__)
    * [metadata](#show.Show.metadata)
    * [update\_metadata](#show.Show.update_metadata)
    * [shots](#show.Show.shots)
    * [load\_shot](#show.Show.load_shot)
    * [create\_shot](#show.Show.create_shot)
    * [archive](#show.Show.archive)
    * [delete](#show.Show.delete)
* [shot.py](#shot)
  * [ShotMetadata](#shot.ShotMetadata)
  * [Shot](#shot.Shot)
    * [\_\_init\_\_](#shot.Shot.__init__)
    * [metadata](#shot.Shot.metadata)
    * [update\_metadata](#shot.Shot.update_metadata)
    * [assets\_by\_category](#shot.Shot.assets_by_category)
    * [assets](#shot.Shot.assets)
    * [load\_asset](#shot.Shot.load_asset)
    * [create\_asset](#shot.Shot.create_asset)
    * [archive](#shot.Shot.archive)
    * [delete](#shot.Shot.delete)
* [asset.py](#asset)
  * [AssetMetadata](#asset.AssetMetadata)
  * [Asset](#asset.Asset)
    * [\_\_init\_\_](#asset.Asset.__init__)
    * [metadata](#asset.Asset.metadata)
    * [update\_metadata](#asset.Asset.update_metadata)
    * [shots](#asset.Asset.shots)
    * [archive](#asset.Asset.archive)
    * [delete](#asset.Asset.delete)


<a id="storage"></a>

# storage.py

<a id="storage.Storage"></a>

## Storage Objects

```python
class Storage()
```

<a id="storage.Storage.__init__"></a>

#### \_\_init\_\_

```python
def __init__(root: str) -> None
```

Create a new pipeline storage.

**Arguments**:

- `root` - The path under which all pipeline data is stored

<a id="storage.Storage.shows"></a>

#### shows

```python
def shows() -> List[str]
```

Get the list of shows in the pipeline.

The order of the returned shows is undertermined.

<a id="storage.Storage.load_show"></a>

#### load\_show

```python
def load_show(name: str) -> Show
```

Load the data for a show in the storage.

**Arguments**:

- `name` - The name of the show to load
  

**Raises**:

- `FileNotFoundError` - if the show does not exist

<a id="storage.Storage.create_show"></a>

#### create\_show

```python
def create_show(name: str) -> Show
```

Create a new show inside the pipeline storage.

**Raises**:

- `FileExistsError` - If the show already exists

<a id="directory"></a>

# directory.py

<a id="directory.Directory"></a>

## Directory Objects

```python
class Directory(os.PathLike)
```

An existing directory where pipeline data is stored.

**Raises**:

- `FileNotFoundError` - the directory does not yet exist

<a id="directory.Directory.create"></a>

#### create

```python
@staticmethod
def create(path) -> "Directory"
```

Create a new pipeline directory for storing data.

<a id="directory.Directory.name"></a>

#### name

```python
def name() -> str
```

The name of this directory on disk

<a id="directory.Directory.load_metadata"></a>

#### load\_metadata

```python
def load_metadata() -> dict
```

Loads the current metadata from this directory.

<a id="directory.Directory.save_metadata"></a>

#### save\_metadata

```python
def save_metadata(metadata: dict) -> None
```

Saves the given metadata into the directory for later retrieval.

metadata: A data class holding the metadata to save

<a id="directory.Directory.delete"></a>

#### delete

```python
def delete() -> None
```

Delete this directory and everything within it.

<a id="show"></a>

# show.py

<a id="show.ShowMetadata"></a>

## ShowMetadata Objects

```python
@dataclass(slots=True, eq=True)
class ShowMetadata()
```

A dataclass representing the metadata of a show.

**Attributes**:

- `name` _str_ - The name of the show.
- `description` _str_ - A description of the show. Defaults to an empty string.

<a id="show.Show"></a>

## Show Objects

```python
class Show()
```

A class representing a show in a given directory.

**Attributes**:

- `_directory` _Directory_ - The directory where the show is located.
- `_metadata` _ShowMetadata_ - The metadata of the show.

<a id="show.Show.__init__"></a>

#### \_\_init\_\_

```python
def __init__(directory: Directory) -> None
```

Open a show in the given directory.

This will load any existing metadata or save the default as needed.

<a id="show.Show.metadata"></a>

#### metadata

```python
def metadata() -> ShowMetadata
```

Returns the available metadata for this show.

<a id="show.Show.update_metadata"></a>

#### update\_metadata

```python
def update_metadata(metadata: ShowMetadata) -> None
```

Modify the metadata for this show.

<a id="show.Show.shots"></a>

#### shots

```python
def shots() -> List[str]
```

Get the list of shots in the pipeline.

The order of the returned shots is undetermined.

<a id="show.Show.load_shot"></a>

#### load\_shot

```python
def load_shot(name: str) -> Shot
```

Load the data for a shot in the storage.

**Arguments**:

- `name` - The name of the shot to load
  

**Raises**:

- `FileNotFoundError` - if the shot does not exist

<a id="show.Show.create_shot"></a>

#### create\_shot

```python
def create_shot(name: str) -> Shot
```

Create a new shot inside the pipeline storage.

**Raises**:

- `FileExistsError` - If the shot already exists

<a id="show.Show.archive"></a>

#### archive

```python
def archive(delete_original_folder: bool = False) -> None
```

Archive this show into a .zip file

**Arguments**:

- `delete_original_folder` - If set to True, the directory being zipped will be deleted.

<a id="show.Show.delete"></a>

#### delete

```python
def delete() -> None
```

Remove this show and all associated shots and data.

<a id="shot"></a>

# shot.py

<a id="shot.ShotMetadata"></a>

## ShotMetadata Objects

```python
@dataclass(frozen=True)
class ShotMetadata()
```

A dataclass representing the metadata of a shot.

**Attributes**:

- `name` _str_ - The name of the shot.
- `description` _str_ - A description of the shot. Defaults to an empty string.

<a id="shot.Shot"></a>

## Shot Objects

```python
class Shot()
```

A class representing a shot in a given directory.

**Attributes**:

- `_directory` _Directory_ - The directory where the shot is located.
- `_metadata` _ShotMetadata_ - The metadata of the shot.

<a id="shot.Shot.__init__"></a>

#### \_\_init\_\_

```python
def __init__(directory: Directory) -> None
```

Open a shot in the given directory.

This will load any existing metadata or save the default as needed.

<a id="shot.Shot.metadata"></a>

#### metadata

```python
def metadata() -> ShotMetadata
```

Returns the available metadata for this shot.

<a id="shot.Shot.update_metadata"></a>

#### update\_metadata

```python
def update_metadata(metadata: ShotMetadata) -> None
```

Modify the metadata for this shot.

<a id="shot.Shot.assets_by_category"></a>

#### assets\_by\_category

```python
def assets_by_category(category: str) -> List[str]
```

Get the list of assets of a given category in the pipeline.

The order of the returned assets is undetermined.

**Arguments**:

- `category` _str_ - The category of assets to be listed.

<a id="shot.Shot.assets"></a>

#### assets

```python
def assets() -> List[str]
```

Get the list of assets in the pipeline.

The order of the returned assets is undetermined.

<a id="shot.Shot.load_asset"></a>

#### load\_asset

```python
def load_asset(name: str) -> Asset
```

Load the data for an asset in the storage.

**Arguments**:

  name (str) : The name of the asset to load
  

**Raises**:

- `FileNotFoundError` - if the shot does not exist

<a id="shot.Shot.create_asset"></a>

#### create\_asset

```python
def create_asset(name: str, category: str = "") -> Asset
```

Create a new asset inside the pipeline storage.

**Arguments**:

- `name` - The name of the asset to create
- `category` - The category to assign the asset. If this is left empty, asset will have no category.
  

**Raises**:

- `FileExistsError` - If the asset already exists

<a id="shot.Shot.archive"></a>

#### archive

```python
def archive(delete_original_folder: bool = False) -> None
```

Archive this shot into a .zip file

**Arguments**:

- `delete_original_folder` - If set to True, the directory being zipped will be deleted.

<a id="shot.Shot.delete"></a>

#### delete

```python
def delete() -> None
```

Remove this shot and all associated data.

<a id="asset"></a>

# asset.py

<a id="asset.AssetMetadata"></a>

## AssetMetadata Objects

```python
@dataclass(frozen=True)
class AssetMetadata()
```

A dataclass for storing information about an asset.

**Attributes**:

* `name` _str_ - The name of the asset.
* `category` _str_ - The category of the asset.
* `description` _str_ - A description of the asset.

<a id="asset.Asset"></a>

## Asset Objects

```python
class Asset()
```

A class for representing an asset in a given directory.

**Attributes**:

* `_directory` _Directory_ - The directory where the asset is located.
* `_metadata` _AssetMetadata_ - The metadata associated with the asset.
  
**Methods**:

* `metadata` - Returns the available metadata for this shot.
* `update_metadata` - Modify the metadata for this shot.
* `shots` - Get the list of shots this asset is used in.
* `archive` - Archive this asset into a .zip file.
* `delete` - Remove this asset and all associated data.

<a id="asset.Asset.__init__"></a>

#### \_\_init\_\_

```python
def __init__(directory: Directory, category: str = "") -> None
```

Open an asset in the given directory.

This will load any existing metadata or save the default as needed.

<a id="asset.Asset.metadata"></a>

#### metadata

```python
def metadata() -> AssetMetadata
```

Returns the available metadata for this shot.

<a id="asset.Asset.update_metadata"></a>

#### update\_metadata

```python
def update_metadata(metadata: AssetMetadata) -> None
```

Modify the metadata for this shot.

<a id="asset.Asset.shots"></a>

#### shots

```python
def shots() -> List[str]
```

Get the list of shots this asset is used in.

Asset must have the same name in other shots.

The order of the returned shots is undetermined.

<a id="asset.Asset.archive"></a>

#### archive

```python
def archive(delete_original_folder: bool = False) -> None
```

Archive this asset into a .zip file

**Arguments**:

* `delete_original_folder` - If set to True, the directory being zipped will be deleted.

<a id="asset.Asset.delete"></a>

#### delete

```python
def delete() -> None
```

Remove this asset and all associated data.
