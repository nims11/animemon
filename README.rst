animemon
========

**A Python Application that displays all the information about all your
anime in the command line. An anime ripoff of
[@iCHAIT](https://github.com/iCHAIT)'s
`moviemon <https://github.com/iCHAIT/moviemon>`__**

Installation
------------

Using pip
~~~~~~~~~

.. code:: sh

    $ pip install animemon

Get the latest build from the Source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: sh

    $ git clone https://github.com/nims11/animemon
    $ cd animemon
    $ python setup.py install

Dependencies
~~~~~~~~~~~~

-  `guessit <https://github.com/guessit-io/guessit>`__
-  `terminaltables <https://github.com/Robpol86/terminaltables>`__
-  `docopt <https://github.com/docopt/docopt>`__
-  `tqdm <https://github.com/tqdm/tqdm>`__
-  `colorama <https://github.com/tartley/colorama>`__

Usage:
~~~~~~

.. code:: sh

      animemon [ --auth=user:pass ] PATH
      animemon [ -m | -n | -g | -y | -r | -M | -N ]
      animemon -h | --help
      animemon --version

Examples:
~~~~~~~~~

Display basic info about all your anime
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: sh

    $ animemon

Display all movies sorted according to their MyAnimeList ratings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: sh

    $ animemon -m

Index your anime collection with MAL Ratings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: sh

    $ animemon ~/anime --auth=viceversa:password123

Options:
~~~~~~~~

.. code:: sh

      -h, --help            Show this screen.
      --version             Show version.
      PATH                  Path to anime dir. to index/reindex all anime.
      --auth=user:pass      Your MyAnimeList username (eg. --auth=coolguy123:password12)
      -m, --mal             Sort acc. to MyAnimeList rating.(dec)
      -n, --humming         Sort acc. to Hummingbird rating.(dec)
      -g, --genre           Show anime name with its genre.
      -y, --year            Show anime name with its release date.
      -r, --runtime         Show anime name with its runtime.
      -M, --mal-rev         Sort acc. to MyAnimeList rating.(inc)
      -N, --humming-rev     Sort acc. to Hummingbird rating.(inc)
