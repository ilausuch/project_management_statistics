import os
import sys
import argparse
import pytest
import yaml
from utils.config_parser import ConfigParser


def test_config_parser():
    parser = argparse.ArgumentParser()
    config_parser = ConfigParser(parser)
    parser.add_argument('--output_format', type=str, help='output_format')

    config_data = {'output_format': 'csv',
                   'start_date': '2020-01-01'}
    with open('/tmp/test_config.yml', 'w', encoding='utf8') as outfile:
        yaml.dump(config_data, outfile)

    sys.argv = ['test_script', '--config', '/tmp/test_config.yml', '--output_format', 'json']

    parsed_args = config_parser.parse_args()

    assert parsed_args['output_format'] == 'json'
    assert parsed_args['start_date'] == '2020-01-01'

    os.remove('/tmp/test_config.yml')


def test_config_parser_no_config():
    parser = argparse.ArgumentParser()
    config_parser = ConfigParser(parser)

    sys.argv = ['test_script']

    parsed_args = config_parser.parse_args()

    assert parsed_args.get('config') is None


def test_config_parser_invalid_yaml():
    parser = argparse.ArgumentParser()
    config_parser = ConfigParser(parser)

    with open('/tmp/test_config.yml', 'w', encoding='utf8') as outfile:
        outfile.write('invalid yaml')

    sys.argv = ['test_script', '--config', '/tmp/test_config.yml']

    with pytest.raises(ValueError):
        config_parser.parse_args()

    # Cleanup
    os.remove('/tmp/test_config.yml')
