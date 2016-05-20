# netta
A file-packaging application for making data sets, books with ordered
tables of contents written in Python 3, using the Flask framework.

This is experimental, Alpha quality software only, with some test
coverage and a very basic UI. 

This some similarities with [cr8it](https://github.com/IntersectAustralia/owncloud) which is a plugin for ownCloud. Netta is designed to run as a desktop app and can thus run on any files that the user can mount. The obvious downside is that it will have to be distributed as a stand-alone application rather than running on the web. The upside is that it can do a lot more with file-conversion and thumbnail creation running locally without creating a lot of extra files in a user's ownCloud share.

The primary application for this software is to compile  data-sets for
deposit into an institutional repository:

*  Runs as a web application on a user's computer (i.e. a little web server)

*  Allows users to browse directories mounted on their computer and
add files and directories to a data package

*  Exports to the BagIt format and packages (Zip now, more formats
   such as tar and disk images coming soon)

*  Allows users to order files in the package and give them meaningful
   labels rather than just filenames (coming soon: add arbitrary
   metadata to packages and files)

*  Extracts metadata from files using Apache Tika (also considering
using Siegfried)

* (Coming soon: Generates a README file for each package with
thumbnails)

*  Generates thumbnails and PDF versions of files using an extensible
plugin system.

Other applications (coming soon):

* Generate EPUB books from collections of documents and other bits and
pieces, using Calibre to do the heavy lifting

*  Use my other project, [chordprobook] to make song-books from text
   files (and maybe also PDF)

# Audience

At this stage Netta is only for Python developers, but if the experiment succeeds then it will be packaged as a stand-alone executable for Windows and OS X for general use.

# Install

*  Install dependencies (TODO: check this):

  ```pip3 install bagit pillow flask tika PyPDF2```

*   Install an Open Office derivative such as Libre Office and make sure
the executable ```soffice``` is in your path.


# Run it

To run:

```python3 netta.py```

Then visit  http://localhost:5000 in your browser

[chordprobook]: https://github.com/ptsefton/chordprobook

