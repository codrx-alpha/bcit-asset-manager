import os
import pipeline as pipe

root = os.getcwd() + f"\show-directory"

storage = pipe.Storage(root)

custom_dir = pipe.Directory()
custom_show = pipe.Show()

show_flash = storage.create_show("The Flash")

shot_opening = show_flash.create_shot("Opening")

asset_suit = shot_opening.create_asset("suit")






