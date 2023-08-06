from argparse import ArgumentParser
import argparse
from pathlib import Path
from typing import Any

import pydwanimes.application.sites.anime_fenix as anime_fenix
from pydwanimes.application.loading.tqdm_loading import TqdmLoading
from pydwanimes.application.config import config


def config_command(args: Any)-> None:
    key = args.key
    value = args.value

    if not value:
        value = config.get(key)
        print(f"Config {key} -> {value}")
    else:
        value = config.update(key,value)
        print(f"Config updated {key} -> {value}")

def download_command(args: Any):
    anime_slug = args.name
    chapter = args.chapter
    path = Path(args.directory).joinpath(anime_slug)
    d = path.resolve()

    ld = TqdmLoading()

    s = anime_fenix.AnimeFenix({
        "directory": d,
        "loading": ld
    })
    s.download_multimedia(anime_slug, chapter)


def main():
    parser = ArgumentParser(description="Anime downloader",
                            formatter_class=argparse.HelpFormatter)

    subparser = parser.add_subparsers(help="actions")

    # Download commands
    download_parser = subparser.add_parser('dw', help="downloader")

    download_parser.add_argument('name', type=str, help="Anime name")
    download_parser.add_argument('chapter', type=int, help="Anime chapter")
    download_parser.add_argument("--directory", dest="directory",
                        type=str,
                        default=config.get("directory"),
                        help="Directory to save animes")

    # Configuration commands
    config_parser = subparser.add_parser('config', help="configuration")

    config_parser.add_argument('key', type=str, help="Key setting")
    config_parser.add_argument('--value', type=str, help="Value of setting", default=None)

    args = parser.parse_args()

    if getattr(args,"name",None) :
        download_command(args)
    elif getattr(args,"key",None):
        config_command(args)
    

if __name__ == '__main__':
    main()
