# animemon

**A Python Application that displays all the information about all your anime in the command line.**

### Dependencies

* [guessit](https://github.com/guessit-io/guessit)
* [terminaltables](https://github.com/Robpol86/terminaltables)
* [docopt](https://github.com/docopt/docopt)
* [tqdm](https://github.com/tqdm/tqdm)
* [colorama](https://github.com/tartley/colorama)


### Usage:
```sh
  animemon.py PATH
  animemon [-i | -t | -g | -a | -c | -d | -y | -r | -I | -T ]
  animemon -h | --help
  animemon --version
```

### Options:
```sh
  -h, --help            Show this screen.
  --version             Show version.
  PATH                  Path to anime dir. to index/reindex all anime.
  -m, --mal             Sort acc. to MyAnimeList rating.(dec)
  -u, --humming         Sort acc. to Hummingbird rating.(dec)
  -g, --genre           Show anime name with its genre.
  -y, --year            Show anime name with its release date.
  -r, --runtime         Show anime name with its runtime.
  -M, --mal-rev         Sort acc. to MyAnimeList rating.(inc)
  -U, --humming-rev     Sort acc. to Hummingbird rating.(inc)
```
