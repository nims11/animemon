#!/usr/bin/python
"""animemon.

Usage:
  animemon [ --auth=user:pass ] PATH
  animemon [ -m | -n | -g | -y | -r | -M | -N ]
  animemon -h | --help
  animemon --version

Options:
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

"""

from __future__ import print_function
import os
import textwrap
import requests
import json
import sys
from guessit import guess_file_info
from terminaltables import AsciiTable
try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode
from docopt import docopt
from tqdm import tqdm
from colorama import init, Fore
import xml.etree.ElementTree

init()

MAL_API_URL = 'http://myanimelist.net/api/anime/search.xml?'
HUMMINGBIRD_URL = 'http://hummingbird.me/api/v1/search/anime?'
MAL_USER = None
MAL_PASS = None

EXT = (".3g2 .3gp .3gp2 .3gpp .60d .ajp .asf .asx .avchd .avi .bik .bix"
       ".box .cam .dat .divx .dmf .dv .dvr-ms .evo .flc .fli .flic .flv"
       ".flx .gvi .gvp .h264 .m1v .m2p .m2ts .m2v .m4e .m4v .mjp .mjpeg"
       ".mjpg .mkv .moov .mov .movhd .movie .movx .mp4 .mpe .mpeg .mpg"
       ".mpv .mpv2 .mxf .nsv .nut .ogg .ogm .omf .ps .qt .ram .rm .rmvb"
       ".swf .ts .vfw .vid .video .viv .vivo .vob .vro .wm .wmv .wmx"
       ".wrap .wvx .wx .x264 .xvid")

EXT = tuple(EXT.split())

CONFIG_PATH = os.path.expanduser("~/.animemon")


def main():
    global MAL_USER, MAL_PASS
    args = docopt(__doc__, version='animemon 0.1.1')
    if args['PATH']:
        if args['--auth']:
            if ':' in args['--auth']:
                user, passwd = args['--auth'].split(':', 1)
                if len(user) > 0 or len(passwd) > 0:
                    MAL_USER, MAL_PASS = user, passwd
            if MAL_USER == None or MAL_PASS == None:
                print(Fore.RED + 'BAD format for --mal-auth, see help (--help) for proper format')
                sys.exit(1)
        if MAL_USER == None or MAL_PASS == None:
            print(Fore.RED + 'MyAnimeList Username and Password not specified, MAL Rating won\'t be computed' + Fore.RESET)
    util(args)


def util(docopt_args):
    if docopt_args["PATH"]:
        if os.path.isdir(docopt_args["PATH"]):

            print("\n\nIndexing all anime inside ",
                  docopt_args["PATH"] + "\n\n")

            dir_json = docopt_args["PATH"] + ".json"

            # Save path to config file so we can read it later
            with open(CONFIG_PATH, "w") as inpath:
                inpath.write(docopt_args["PATH"])

            scan_dir(docopt_args["PATH"], dir_json)

            if anime_name:
                if anime_not_found:
                    print(Fore.RED + "\n\nData for the following anime(s)"
                          " could not be fetched -\n")
                    for val in anime_not_found:
                        print(Fore.RED + val)
                if not_a_anime:
                    print(Fore.RED + "\n\nThe following media in the"
                          " folder is not anime type -\n")
                    for val in not_a_anime:
                        print(Fore.RED + val)
                print(Fore.GREEN + "\n\nRun $animemon\n\n")
            else:
                print(Fore.RED + "\n\nGiven directory does not contain anime."
                      " Pass a directory containing anime\n\n")
        else:
            print(Fore.RED + "\n\nDirectory does not exists."
                  " Please pass a valid directory containing anime.\n\n")

    elif docopt_args["--mal"]:
        table_data = [["TITLE", "MAL RATING"]]
        data, table = butler(table_data)
        for item in data:
            item["Title"] = clean_table(item["Title"], None, item,
                                        table)
            table_data.append([item["Title"], item["malRating"]])
        sort_table(table_data, 1, True)

    elif docopt_args["--humming"]:
        table_data = [["TITLE", "HUMMINGBIRD RATING"]]
        data, table = butler(table_data)
        for item in data:
            item["Title"] = clean_table(item["Title"], None, item,
                                        table)
            table_data.append([item["Title"], item["hummingRating"]])
        sort_table(table_data, 1, True)

    elif docopt_args["--genre"]:
        table_data = [["TITLE", "GENRE"]]
        data, table = butler(table_data)
        for item in data:
            item["Title"] = clean_table(item["Title"], None,
                                        item, table)
            table_data.append([item["Title"], item["Genre"]])
        sort_table(table_data, 0, False)

    elif docopt_args["--year"]:
        table_data = [["TITLE", "RELEASED"]]
        data, table = butler(table_data)
        for item in data:
            item["Title"] = clean_table(item["Title"], None, item,
                                        table)
            table_data.append([item["Title"], item["Released"]])
        sort_table(table_data, 0, False)

    elif docopt_args["--runtime"]:  # Sort result by handling numeric sort
        table_data = [["TITLE", "RUNTIME"]]
        data, table = butler(table_data)
        for item in data:
            item["Title"] = clean_table(item["Title"], None, item,
                                        table)
            table_data.append([item["Title"], item["Runtime"]])
        print_table(table_data)

    elif docopt_args["--mal-rev"]:
        table_data = [["TITLE", "MAL RATING"]]
        data, table = butler(table_data)
        for item in data:
            item["Title"] = clean_table(item["Title"], None, item,
                                        table)
            table_data.append([item["Title"], item["malRating"]])
        sort_table(table_data, 1, False)

    elif docopt_args["--humming-rev"]:
        table_data = [["TITLE", "HUMMINGBIRD RATING"]]
        data, table = butler(table_data)
        for item in data:
            item["Title"] = clean_table(item["Title"], None, item,
                                        table)
            table_data.append([item["Title"], item["hummingRating"]])
        sort_table(table_data, 1, False)

    else:
        table_data = [
            ["TITLE", "GENRE", "MAL", "RUNTIME", "HUMMINGBIRD",
             "YEAR"]]
        data, table = butler(table_data)
        for item in data:
            item["Title"], item["Genre"] = clean_table(item["Title"],
                                                       item["Genre"], item,
                                                       table)
            table_data.append([item["Title"], item["Genre"],
                               item["malRating"], item["Runtime"],
                               item["hummingRating"], item["Year"]])
        sort_table(table_data, 0, False)


def sort_table(table_data, index, reverse):
    table_data = (table_data[:1] + sorted(table_data[1:],
                                          key=lambda i: i[index],
                                          reverse=reverse))
    print_table(table_data)


def clean_table(tag1, tag2, item, table):
    if tag1 and tag2:
        if len(tag1) > table.column_max_width(0):
            tag1 = textwrap.fill(
                tag1, table.column_max_width(0))
            if len(tag2) > table.column_max_width(1):
                tag2 = textwrap.fill(
                    tag2, table.column_max_width(1))
        elif len(tag2) > table.column_max_width(1):
            tag2 = textwrap.fill(
                tag2, table.column_max_width(1))
        return tag1, tag2
    elif tag1:
        if len(tag1) > table.column_max_width(0):
            tag1 = textwrap.fill(
                tag1, table.column_max_width(0))
        return tag1


def butler(table_data):
    try:
        with open(CONFIG_PATH) as config:
            anime_path = config.read()
    except IOError:
        print(Fore.RED, "\n\nRun `$animemon PATH` to "
              "index your anime directory.\n\n")
        quit()
    else:
        table = AsciiTable(table_data)
        try:
            with open(anime_path + ".json") as inp:
                data = json.load(inp)
            return data, table
        except IOError:
            print(Fore.YELLOW, "\n\nRun `$animemon PATH` to "
                  "index your anime directory.\n\n")
            quit()


def print_table(table_data):
    table = AsciiTable(table_data)
    table.inner_row_border = True
    if table_data[:1] in ([['TITLE', 'MAL RATING']],
                          [['TITLE', 'HUMMINGBIRD RATING']]):
        table.justify_columns[1] = 'center'
    print("\n")
    print(table.table)


anime = []
anime_name = []
not_a_anime = []
anime_not_found = []


def scan_dir(path, dir_json):
    # Preprocess the total files count
    for root, dirs, files in tqdm(os.walk(path)):
        for name in files:
            path = os.path.join(root, name)
            if os.path.getsize(path) > (9*1024*1024):
                ext = os.path.splitext(name)[1]
                if ext in EXT:
                    anime_name.append(name)

    with tqdm(total=len(anime_name), leave=True, unit='B',
              unit_scale=True) as pbar:
        for name in anime_name:
            data = get_anime_info(name)
            pbar.update()
            if data is not None and data.get('Response', 'False') == 'True':
                for key, val in data.items():
                    if val == "N/A":
                        data[key] = "-"  # Should N/A be replaced with `-`?
                anime.append(data)
            elif data is not None and data['Cached'] == True:
                pass
            else:
                if data is not None:
                    anime_not_found.append(name)
        with open(dir_json, "w") as out:
            json.dump(anime, out, indent=2)

titleCache = {}

def get_anime_info(name):
    global titleCache
    """Find anime information"""
    anime_info = guess_file_info(name, type="episode")
    anime_title = anime_info.get('title', anime_info.get('series', None))
    if anime_title != None:
        if anime_title.lower() in titleCache:
            return {'Cached': True}
        response = None
        if 'year' in anime_info:
            response = hummingbird(anime_title, anime_info['year'])
        else:
            response = hummingbird(anime_title, None)
        if response['Title'].lower() in titleCache:
            return {'Cached': True}
        titleCache[response['Title'].lower()] = True
        titleCache[anime_title.lower()] = True
        return response
    else:
        not_a_anime.append(name)

def getMALRating(title):
    if MAL_USER == None or MAL_PASS == None:
        return -1
    try:
        xmlresponse = requests.get(MAL_API_URL+'q='+title, auth=(MAL_USER, MAL_PASS))
        status = xmlresponse.status_code
        if status//100 == 4:
            print(Fore.RED + 'MAL Auth failed, correct the credentials or remove the auth parameter' + Fore.RESET)
            sys.exit(1)
        et = xml.etree.ElementTree.fromstring(xmlresponse.content.strip())
        if len(list(et)) == 0:
            return -1
        return list(et)[0].find('score').text
    except SystemExit:
        sys.exit(1)
    except:
        return -1

def convertResponse(entry):
    return {
        'Title': entry['title'],
        'Year': (entry['started_airing'].split('-', 1)[0] if entry['started_airing'] != None else "N/A"),
        'Genre': ','.join([x['name'] for x in entry['genres']]),
        'malRating': str(getMALRating(entry['title'])),
        'hummingRating': str(entry['community_rating']),
        'Runtime': 'Ep: %s, Length: %s min' % (str(entry['episode_count']) if entry['episode_count'] != None else "N/A",
                                               str(entry['episode_length']) if entry['episode_length'] != None else "N/A"),
        'Response': "True"
    }

def hummingbird(title, year):
    """ Fetch data from HUMMINGBIRD API. """
    params = {'query': title}
    url = HUMMINGBIRD_URL + urlencode(params)
    response = requests.get(url).json()

    if year:
        filteredResponse = []
        for animeEntry in response:
            if year in (animeEntry['started_airing'].split('-', 1)[0] if animeEntry['started_airing'] != None else None,
                        animeEntry['finished_airing'].split('-', 1)[0] if animeEntry['finished_airing'] != None else None):
                filteredResponse.append(animeEntry)
            if len(filteredResponse) > 0:
                response = filteredResponse

    if len(response) == 0:
        return None
    return convertResponse(response[0])

if __name__ == '__main__':
    main()
