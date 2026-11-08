"""Download public Pokémon Showdown replays into data/replays/.

    python download_replays.py                          # 100 recent Gen 1 random battles
    python download_replays.py --count 1000 --min-rating 1300
    python download_replays.py --format gen1ou

Each replay is saved as data/replays/<id>.json; the battle itself is the "log" field.
Re-running skips replays you already have. Needs Python 3.10+ and nothing else.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://replay.pokemonshowdown.com"
HEADERS = {"User-Agent": "carletonai-pokemon-battle-trainer replay downloader"}


def get_json(url: str):
    time.sleep(0.25)  # be polite to Showdown's servers
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--format", default="gen1randombattle", help="Showdown format id")
    parser.add_argument("--count", type=int, default=100, help="how many replays to end up with")
    parser.add_argument("--min-rating", type=int, default=0, help="skip replays rated below this")
    parser.add_argument("--out", type=Path, default=Path("data/replays"), help="output folder")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    have = new = 0
    before = None
    while have < args.count:
        query = {"format": args.format}
        if before is not None:
            query["before"] = before
        page = get_json(f"{API}/search.json?{urllib.parse.urlencode(query)}")
        if not page or page[-1]["uploadtime"] == before:
            break  # no older replays
        for entry in page:
            if have >= args.count:
                break
            if entry.get("private") or entry.get("password"):
                continue
            if (entry.get("rating") or 0) < args.min_rating:
                continue
            path = args.out / f"{entry['id']}.json"
            if not path.exists():
                try:
                    replay = get_json(f"{API}/{entry['id']}.json")
                except urllib.error.HTTPError as error:
                    print(f"\nskipping {entry['id']}: {error}")
                    continue
                part = path.with_suffix(".part")
                part.write_text(json.dumps(replay), encoding="utf-8")
                part.replace(path)
                new += 1
            have += 1
            print(f"\r{have}/{args.count} replays", end="", flush=True)
        before = page[-1]["uploadtime"]

    print(f"\ndone: {have} replays in {args.out} ({new} new)")


if __name__ == "__main__":
    main()
