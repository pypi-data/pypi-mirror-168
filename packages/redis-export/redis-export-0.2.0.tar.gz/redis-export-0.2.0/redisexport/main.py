#!/usr/bin/env python3
# coding=utf-8
#
# Copyright (C) 2022  Yuanle Song <sylecn@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""Export redis keys with a given prefix.

"""

import argparse
import logging
import codecs
import json

import redis

from redisexport import __version__


logger = logging.getLogger(__name__)


def tob64(bs):
    """encode bytes to base64 string.

    """
    return codecs.decode(codecs.encode(bs, 'base64'))


def fromb64(s):
    """decode base64 string to bytes.

    """
    return codecs.decode(codecs.encode(s), 'base64')


def get_redis(args):
    return redis.Redis(host=args.host, port=args.port, db=args.num)


def export_db(args):
    pattern = args.pattern
    if '*' not in pattern:
        pattern = pattern + '*'
    logger.info("export keys with pattern %s...", pattern)
    result = []
    red = get_redis(args)
    cur = 0
    while True:
        cur, key_list = red.scan(cur, match=pattern)
        for key in key_list:
            result.append((tob64(key), tob64(red.dump(key))))
        if cur == 0:
            break
    # Note: can't use 'wb' in json.dump()
    with open(args.output_filename, 'w', encoding='utf-8') as fo:
        json.dump(result, fo, ensure_ascii=True, indent=0)
    logger.info("dumped %s keys", len(result))


def import_db(args):
    logger.info("import keys...")
    with open(args.input_filename, 'r', encoding='utf-8') as fi:
        result = json.load(fi)
    red = get_redis(args)
    pipe = red.pipeline()
    for key, value in result:
        pipe.restore(fromb64(key), 0, fromb64(value), replace=True)
    pipe.execute()
    logger.info("restored %s keys", len(result))


def create_shared_parser():
    """create shared parser for both export and import cli tools.

    """
    parser = argparse.ArgumentParser(
        description='redis db selective export and import tool'
                    ' v%s' % (__version__, ))
    parser.add_argument('--host', default='localhost', help='redis host')
    parser.add_argument('-p', '--port', default=6379, help='redis port')
    parser.add_argument('-n', '--num', help='redis database number')
    return parser


def redis_export():
    logging.basicConfig(
        format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
        level=logging.INFO)
    parser = create_shared_parser()
    parser.add_argument('pattern', help='key prefix to export')
    parser.add_argument('output_filename')
    args = parser.parse_args()
    export_db(args)


def redis_import():
    logging.basicConfig(
        format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
        level=logging.INFO)
    parser = create_shared_parser()
    parser.add_argument('input_filename')
    args = parser.parse_args()
    import_db(args)
