app.fuse
========

Fuse support for app.net files. Or app.net support for fuse...


## Usage

Currently this needs a `.app.fuse.conf` in the current directory like so:

``
[Auth]
access_token = \<an app.net access token\>
``

Then in your checkout of this you do:

``
virtualenv env
. env/bin/activate
pip install -r requirements.txt
``

to get all the needed stuff. Then run it in the same shell with:

``
python src/fs.py \<path_where_you_want_it_mounted\>
``

Then look into the dir with `ls` or any file-browser to see your files. Well,
their metadata and as content their url...

End it all with

``
fusermount -f <mountpoint_from_above>
``

## Current state

**This is pre-alpha!**

Currently it lists all your files stored on app.net. It reads the list of files
once upon startup and then uses this.


## Ideas for the future

 - Learn how to make it a usable app.net application without manual giving it
   an app.net access\_token

 - Retrieve actual file contents.

 - Cache files locally, maybe in a hidden subdir or in `~/.app.fuse` or in
   a database...

 - Update files from the net dynamically.

 - Support for writing files.
