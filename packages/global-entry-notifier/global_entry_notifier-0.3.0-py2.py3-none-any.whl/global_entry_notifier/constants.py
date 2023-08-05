from __future__ import annotations

import sys

if sys.version_info >= (3, 8):  # pragma: >=3.8 cover
    import importlib.metadata as importlib_metadata
else:  # pragma: <3.8 cover
    import importlib_metadata

VERSION = importlib_metadata.version('global_entry_notifier')

GLOBAL_ENTRY_BASE_URL = 'https://ttp.cbp.dhs.gov'

GLOBAL_ENTRY_SLOTS_ENDPOINT = '/schedulerapi/slots'
GLOBAL_ENTRY_SLOTS_URL = (
    f'{GLOBAL_ENTRY_BASE_URL}{GLOBAL_ENTRY_SLOTS_ENDPOINT}'
)
GLOBAL_ENTRY_SLOTS_DEFAULT_PARAMETERS = {
    'orderBy': 'soonest',
    'minimum': 1,
    'limit': 3,
}

GLOBAL_ENTRY_LOCATIONS_ENDPOINT = '/schedulerapi/locations/'
GLOBAL_ENTRY_LOCATIONS_URL = (
    f'{GLOBAL_ENTRY_BASE_URL}{GLOBAL_ENTRY_LOCATIONS_ENDPOINT}'
)
GLOBAL_ENTRY_LOCATIONS_DEFAULT_PARAMETERS = {
    'temporary': 'false',
    'inviteOnly': 'false',
    'operational': 'true',
    'serviceName': 'Global Entry',
}

DATETIME_FORMAT_COMMAND_LINE_ARG = '%Y-%m-%dT%H:%M'
DATETIME_FORMAT_COMMAND_LINE_ARG_HELP = 'YYYY-MM-DDTHH:MM'
DATETIME_FORMAT_API = '%Y-%m-%dT%H:%M'
DATETIME_FORMAT_SMS = '%a, %b %d @ %I:%M%p'
