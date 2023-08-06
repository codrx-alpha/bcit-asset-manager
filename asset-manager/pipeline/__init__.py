"""
The pipeline library is used to create, load and manage the shows
and shots within the pipeline storage. 
"""

# the __init__.py file is the main entrypoint to the pipeline
# module/library so I can curate what is accessible in the api
# by importing things here directly
#
# Eg: I want other developer to be able to run the code like:
# import pipeline
# my_show = pipeline.Show("path/to/show")

from .storage import Storage
from .directory import Directory
from .show import Show, ShowMetadata
from .shot import Shot, ShotMetadata
from .asset import Asset, AssetMetadata
