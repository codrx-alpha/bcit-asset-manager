import pipeline as pipe
from pipeline import AssetMetadata
import os


# Create root path
root = os.getcwd()
# Create new Storage at root path
storage = pipe.Storage(root)

# Creating shows, shots and assets
# show_flash = storage.create_show("The Flash")
# shot_opening = show_flash.create_shot("Opening Titles")
# asset_car = shot_opening.create_asset("car")

# Loading shows, shots and assets
show_flash = storage.load_show("The Flash")
shot_opening = show_flash.load_shot("Opening Titles")
asset_car = shot_opening.load_asset("car")

# Asset functionality

# Get all assets in a shot
shot_opening_asset_list = shot_opening.assets()
print(shot_opening_asset_list)

# Read information for a single asset
loaded_asset = shot_opening.load_asset("car")
asset_data = loaded_asset.metadata()
print(asset_data)

# Update asset data
loaded_asset = shot_opening.load_asset("car")
loaded_asset.update_metadata(AssetMetadata(name="mercedes", category="vehicle", description="A silver Mercedes G-Wagon"))

# Delete asset
loaded_asset = shot_opening.load_asset("mercedes")
loaded_asset.delete()

# Find shots by asset
loaded_asset = shot_opening.load_asset("mercedes")
related_shots = loaded_asset.shots()

# Archiving functionality

loaded_show = storage.load_show("The Flash")
loaded_shot = loaded_show.load_shot("Opening Titles")
loaded_asset = loaded_shot.load_asset("mercedes")

loaded_show.archive(delete_original_folder=False)
loaded_shot.archive(delete_original_folder=True)
loaded_asset.archive(delete_original_folder=True)
