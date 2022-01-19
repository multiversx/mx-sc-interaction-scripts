#!/usr/bin/env python3

import argparse
from erdpy.accounts import Address
import json
from pathlib import Path
from typing import Any, List, Union

def pad_even(arg: str) -> str:
    '''
    Pads the argument with a zero, if needed, so that the number of hex-digits is even.

>>> pad_even('4d2b3')
'04d2b3'
>>> pad_even('c0ffee')
'c0ffee'
    '''
    new_length = len(arg) + len(arg) % 2
    return arg.rjust(new_length, '0')


def hex_encode_int(arg: int) -> str:
    '''
    Hex-encodes an int.

>>> hex_encode_int(1234)
'04d2'
    '''
    return pad_even(f'{arg:x}')

def hex_encode_string(arg: str) -> str:
    '''
    Hex-encodes a string.

>>> hex_encode_string('\\ntest')
'0a74657374'
    '''
    return ''.join(f'{ord(c):02x}' for c in arg)

def join_arguments(args: List[str]) -> str:
    return '@'.join(args)


def hex_encode(arg: Union[str, int, Address, List[Any]]) -> str:
    '''
    Hex-encodes an argument or a list of arguments.

>>> hex_encode('\\ntest')
'0a74657374'
>>> hex_encode(1234)
'04d2'
>>> hex_encode([1234, 'test'])
'04d2@74657374'
>>> hex_encode([10, 11, [12, 13]])
'0a@0b@0c@0d'
    '''
    if isinstance(arg, int):
        return hex_encode_int(arg)
    elif isinstance(arg, str):
        return hex_encode_string(arg)
    elif isinstance(arg, Address):
        return arg.hex()
    elif isinstance(arg, list):
        return join_arguments([hex_encode(nested_arg) for nested_arg in arg])
    else:
        raise Exception(f'Invalid argument: {arg}')
    
def prepare_call_data(function: str, args: Any) -> str:
    return join_arguments([function, hex_encode(args)])

def prepare_nft_issue(args: Any) -> str:
    return prepare_call_data('issueNonFungible', [
        args['token_name'],
        args['token_ticker']
    ])

def prepare_set_special_role(args: Any) -> str:
    return prepare_call_data('setSpecialRole', [
        args['token_identifier'],
        Address(args['address']),
        args['roles']
    ])

def prepare_nft_create_call(args: Any) -> str:
    return prepare_call_data('ESDTNFTCreate', [
        args['token_identifier'],
        args['initial_quantity'],
        args['nft_name'],
        args['royalties'],
        args['hash'],
        args['attributes'],
        args['uri']
    ])

def prepare_args(command: str, args: Any) -> str:
    if command == 'nft-issue':
        return prepare_nft_issue(args)
    if command == 'nft-create':
        return prepare_nft_create_call(args)
    if command == 'set-special-roles':
        return prepare_set_special_role(args)

parser = argparse.ArgumentParser(description='Prepare the data field for a given command from a JSON.')
parser.add_argument('command', help='Command to prepare', nargs='?', choices=('nft-issue', 'nft-create', 'set-special-roles'))
parser.add_argument('tx_arguments_json', type=Path, help='Path to the arguments json file')
cli_args = parser.parse_args()

with open(cli_args.tx_arguments_json, 'r') as file:
    tx_args = json.load(file)

tx_data = prepare_args(cli_args.command, tx_args)
print(tx_data)
