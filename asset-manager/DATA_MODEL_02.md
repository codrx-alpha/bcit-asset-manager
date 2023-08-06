## NOTES

> This project is based on the Project01 file provided on GitHub. After testing the existing data model, I decided to use the provided project as I thought it was a good way of implementing the required functionality. As a result, the additional features I have comply with the design of that project.

# Asset Manager API


## Basic Structure

The following additions have been made to the base API:

- A new class "Asset" has been added, which provides functionality to manage individual assets.
  - Assets can be created through instances of the Shot class.
  - Each asset has a metadata file which contains information relative to the asset, as follows:

    ```txt
    Asset
        metadata
            name -> str
            category -> str (optional) 
            description -> str (optional) 
    ```

  - The reason for this is so that each asset's data can be individually accessed, which can then be used for things like finding asset by name or by category.
  - Functionality to find shots associated with assets has also been added. This is done by recursively searching all shot directories for any assets with the same name. For example:  

  ```txt
  Asset Manager
    Shows
      The Flash
        Opening Shot
          building_01
            metadata.json

        Reverse Shot
          building_01
            metadata.json
        
        Running Shot
          car_01
            metadata.json
  ```
  - In the above structure, listing all the shots from the building_01 asset would return the following list:

  ```txt
  ['Opening Shot', 'Reverse Shot']
  ```

  - The disadvantage of this is that for the list to be accurate, the concerned asset needs to be named identically in all shots, or that shot won't show up in the list. Since the metadata file of the asset is not read, only the name of the directory matters. The advantage is that the code becomes less complex.

---

- The existing "Shot" class has been modified

  - Functionality for creating, loading and listing assets, as well as listing assets by category.
  - Creating, loading and listing assets works similarly to doing the same for shots.
  - Listing assets by category is done by iterating over all the assets and getting their respective categories from their metadata. This gives the user the freedom to create any categories they may want to, as opposed to picking from a preset.

---

- Archiving has been added to the Asset, Shot and Show classes.
  - Archiving shots, assets and shows will simply enclose their contents in a .zip file.
  - The user can choose to delete the original directory.
