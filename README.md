# Asset Manager API
An API to create and manage shows, shots and assets in a VFX pipeline.

### See documentation [here](asset-manager/docs.md)

# Usage

## Creating Shows, Shots and Assets
- To create shows, shots or assets, the `pipeline` module must be imported

```py
import pipeline
```

- After importing `pipeline`, a new `Storage` must be instantiated.
- The `Storage` class requires a path where it can create the root of the pipeline.

```py
import pipeline as pipe
import os

root = os.getcwd() + f"\pipeline"

storage = pipe.Storage(root)
```

- Now, using the instance of `Storage` that we have created, we can create a new show, which we will store in a variable.

```py
import pipeline as pipe
import os

root = os.getcwd() + f"\pipeline"

storage = pipe.Storage(root)

show_flash = storage.create_show("The Flash")
```

- Similarly, we can create shots and assets.

```py
import pipeline as pipe
import os


# Create root path
root = os.getcwd() + f"\pipeline"
# Create new Storage at root path
storage = pipe.Storage(root)

# Creating shows, shots and assets
show_flash = storage.create_show("The Flash")
shot_opening = show_flash.create_shot("Opening Titles")
asset_car = shot_opening.create_asset("car")
```

## Using Assets

### Get List of all Assets

```py
# Get all assets in a shot
shot_opening_asset_list = shot_opening.assets()
print(shot_opening_asset_list)
```

### Read information for an asset

```py
# Read information for a single asset
loaded_asset = shot_opening.load_asset("car")
asset_data = loaded_asset.metadata()
print(asset_data)
```

### Update information for an asset

```py
from pipeline import AssetMetadata

# Update asset data
loaded_asset = shot_opening.load_asset("car")
loaded_asset.update_metadata(AssetMetadata(name="mercedes", category="vehicle", description="A silver Mercedes G-Wagon"))
```

### Delete an asset

```py
# Delete asset
loaded_asset = shot_opening.load_asset("mercedes")
loaded_asset.delete()
```

### Find shots by asset used in shot

```py
# Find shots by asset
loaded_asset = shot_opening.load_asset("mercedes")
related_shots = loaded_asset.shots()
```

## Archiving Shows, Shots and Assets

- With this addition to the API shows, shots and assets can be conveniently archived into .zip files.
- A choice can be made regarding whether or not the original directory should be deleted.

```py
# Archiving functionality
import pipeline as pipe
import os

root = os.getcwd() + f"\pipeline"

storage = pipe.Storage(root)

loaded_show = storage.load_show("The Flash")
loaded_shot = loaded_show.load_shot("Opening Titles")
loaded_asset = loaded_shot.load_asset("mercedes")

loaded_show.archive(delete_original_folder=False)
loaded_shot.archive(delete_original_folder=True)
loaded_asset.archive(delete_original_folder=True)
```