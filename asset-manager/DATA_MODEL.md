## NOTES

> This is just a brain dump from our dicussion in class, but I would expect these to be turned into something _a little bit_ more legible before submission. If you are using this as a base for your project 02, you can leave this as-is for the submission and only write a new `DATA_MODEL_02.md` file


## Initial Thoughts

- We need to represent two objects: Shows and Shots
- Each one has an associated directory
- We need to save data for each into the directory
  - we could save these all to a single file, but I'd like to keep the json files separated so that my classes can also be separated
  - if I save all the data to one file, then I can only save the file if I have all the data, which might make some of the code more complex

```txt
Show
    metadata
    directory
    shots (is this instances of Shots or just a way to load/create them?)
        because of wanting to keep the json separate, I am going to say that the show can load/create shots but doesn't keep them in memory
        so this is not a has-a relationship... just a starting point to access shots 
Shot
    metadata
    directory
```

- It seems like there is a requirement here: Metadata needs to be saved to a file.
    - because of this, it might be easier to have a dataclass for this information that can easily be serialized/deserialized from a dictionary
    - this means that the metadata class cannot have methods (break encapsulation) so the shot and shot and shot metadata will be separate types

```txt
Shot
   -> ShotMetadata
   -> Directory
```

- is the directory just a directory string or more complex data structure?
    - it will definitely have a path associated with it on disk
    - this could be a place to handle the json data loading/saving
        - if it handles json save/load then the show/shot can reuse it, which is goo
        - but if they use the same filename could there be collisions?     
        - an error in this case seems appropriate
        - we could say that the filename is a parameter so that the show/shot can have different file names
            - then you could have a folder that is both a show and a shot - which is probably a bad idea...

```txt
class Shot
    -> ShotMetadata
    -> PipelineDirectory

class Show
    -> ShowMetadata
    -> PipelineDirectory
```

## Adding Behaviour

- How do you create a show?
    - does it get created when I create an instance of the show class?
    - do we allow show classes to exist when there is no directory on disk yet?
    - it feels like if I have an isntance of the Show class, that I expect that the show exists on disk
    - this means that our __init__ function needs to either create the show or ensure that it exists
        - it feels a little unsafe to create the directory in the __init__ because then there is no great way to check if a show exists or not
        - more likely you are only creating shows rarely but more likely you want to load an existing one
        - because of that, we'll have a separate, non __init__ function for creating shows and shots
    - this probably applies to shots as well

```py
class Show:
  def __init__(show_name: str) -> None: # (only for loading) 
  def create() -> Show: # (static method for new shows) 
  def metadata(self) -> ShowMetadata: # (returns the current metadata)
  def update_metadata(self, metadata) -> None:
  def shots() -> List[str]:
```

- do we allow updating individual fields or need the whole metadata back
    - since we have a data type for the metadata, seems easier to take the whole thing.
    - we could also ensure that the metadata from metadata() function is a copy so that you can't modify the metadata that the class has without it being saved to diks
    - because we don't want to ever have a Show/Shot instance that is NOT the same as what was on disk (mostly)
    - we can't stop someone else from modifying the files on disk... we could mitigate this by saving the load time and checking the last time the file was saved, but that seems to much for this project so we'll jsut make note of it...

- what do we need to load shows/shots
    - probably a string name is enough, which can be the directory name on disk
    - we will also need the root directory of the pipeline in order to load a show
    - this could be a global variable, but I might rather have another class to hold this jsut to make testing easier

- because each level requires access to the one above for the directory, you will only really be able to load a shot from the full path or via the show
- for consistency, we will do the same for the pipeline

- the delete functionality will break our invarant that says that an instance of the class always exists on disk - unfortunately with python there's not much we can do about this, so will add a note

```py
from dataclasses import dataclass
from typing import List

class Pipeline:
    def __init__(self, root: str) -> None:
        ...

    def shows(self) -> List[str]:
        ...

    def load_show(self, name: str) -> 'Show':
        ...

    def create_show(name: str) -> 'Show':
        ...

@dataclass(freeze=True) 
class ShowMetadata:
    name: str
    description: str

class Show:
    def __init__(self, root: str) -> None:
        ...

    def metadata(self) -> ShowMetadata:
        ...

    def update_metadata(self, metadata: ShowMetadata) -> None:
        ...

    def shots() -> List[str]:
        ...

    def load_shot(name: str) -> 'Shot':
        ...

    def create_shot(name: str) -> 'Shot':
        ...

    def delete(self) -> None:
        ...


@dataclass(freeze=True) 
class ShotMetadata:
    name: str
    description: str

class Shot:
    def __init__(self, name: str) -> None:
        ...

    def metadata(self) -> ShotMetadata:
        ...

    def update_metadata(self, metadata: ShotMetadata) -> None:
        ...

    def delete(self) -> None:
        ...

```

- I decided to rename `Pipeline` to `Storage` because
    1. it created import stuttering since the module is also callled pipeline
    2. more importantly it was not representing an entire pipeline, just the root of it which is kind of more just representing the storage dir for the data


- the directory type saves the metadata instance directly but only loads a dict. We could possible pass the class type around and use that but it would complicate in functions and directory class a little more that I want. Instead returning the dict seems okay.

- I also ended up needing to inherit from os.PathLike in the directory class so that it could be used in functions like `os.path.join`