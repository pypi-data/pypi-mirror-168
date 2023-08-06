import logging
import sys

_log = logging.getLogger(__name__)


def validate_input(arg_number: int, input_name: str):
    try:
        return sys.argv[arg_number]
    except IndexError as ie:
        _log.error(f'ERROR: {input_name} not provided. One or more required path inputs were not provided')
        raise ie
