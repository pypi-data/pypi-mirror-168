from __future__ import annotations

import argparse
import datetime
import typing

import global_entry_notifier.constants
from global_entry_notifier.notifier import notify_if_available


class MissingCountryCodeError(Exception):
    """The supplied phone number is missing a country code"""


def _get_args(argv: typing.Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='global-entry-notifier')

    parser.add_argument(
        '-V', '--version',
        action='version',
        version=f'%(prog)s {global_entry_notifier.constants.VERSION}',
    )

    parser.add_argument(
        '-l', '--locations',
        type=str,
        nargs='+',
        required=True,
        help='Interview location code(s) to check for availability',
    )

    parser.add_argument(
        '-p', '--phone-number',
        type=str,
        required=True,
        help='Your phone number',
    )

    parser.add_argument(
        '-c', '--current-appointment',
        type=lambda appointment_datetime: datetime.datetime.strptime(
            appointment_datetime,
            global_entry_notifier.constants.DATETIME_FORMAT_COMMAND_LINE_ARG,
        ),
        default=datetime.datetime.strptime(
            '9999-12-31T23:59',
            global_entry_notifier.constants.DATETIME_FORMAT_COMMAND_LINE_ARG,
        ),
        help=(
            'Your current interview appointment date and time '
            f'({global_entry_notifier.constants.DATETIME_FORMAT_COMMAND_LINE_ARG_HELP})'  # noqa: E501
        ),
    )

    _add_twilio_arguments(parser)

    parsed_args = parser.parse_args(argv)

    return parsed_args


def _add_twilio_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '--twilio-sid',
        type=str,
        required=True,
        help='Twilio account SID',
    )

    parser.add_argument(
        '--twilio-token',
        type=str,
        required=True,
        help='Twilio authentication token',
    )

    parser.add_argument(
        '--twilio-number',
        type=str,
        required=True,
        help='Twilio phone number',
    )


def _ensure_country_codes(*phone_numbers: str) -> None:
    for phone_number in phone_numbers:
        if not phone_number.startswith('+'):
            raise MissingCountryCodeError(phone_number)


def main(argv: typing.Sequence[str] | None = None) -> int:
    args = _get_args(argv)

    _ensure_country_codes(args.phone_number, args.twilio_number)

    notify_if_available(
        args.locations,
        args.phone_number,
        args.current_appointment,
        args.twilio_sid,
        args.twilio_token,
        args.twilio_number,
    )

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
