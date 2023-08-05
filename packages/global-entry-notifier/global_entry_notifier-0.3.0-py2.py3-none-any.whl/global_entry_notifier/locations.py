from __future__ import annotations

import argparse
import typing

import requests

import global_entry_notifier.constants


def list_locations() -> None:
    args = _get_args()

    locations = _get_locations()

    for location in locations:
        if args.name and args.name.lower() not in location['name'].lower():
            continue

        if args.state and args.state.lower() not in location['state'].lower():
            continue

        print(f"{location['id']:>5} {location['state']:2} {location['name']}")


def _get_locations() -> list[dict[str, str]]:
    response = requests.get(
        global_entry_notifier.constants.GLOBAL_ENTRY_LOCATIONS_URL,
        params=global_entry_notifier.constants.GLOBAL_ENTRY_LOCATIONS_DEFAULT_PARAMETERS,  # noqa: E501
    )

    if not response.ok:
        raise SystemExit(
            'Could not obtain availability information. Exiting...',
        )

    return response.json()


def _get_args(argv: typing.Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='global-entry-locations')

    parser.add_argument(
        '-V', '--version',
        action='version',
        version=f'%(prog)s {global_entry_notifier.constants.VERSION}',
    )

    parser.add_argument(
        '-n', '--name',
        type=str,
        help='Filter for interview location name',
    )

    parser.add_argument(
        '-s', '--state',
        type=str,
        help='Filter for interview location state',
    )

    parsed_args = parser.parse_args(argv)

    return parsed_args
