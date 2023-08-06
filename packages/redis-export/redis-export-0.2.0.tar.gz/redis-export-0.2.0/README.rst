redis-export
============================

Export redis keys with a given prefix or pattern, which later can be imported
to another redis server. To export all keys, use '*' as pattern.

Installation
------------

To install redis-export, simply:

.. code-block:: bash

   $ pip install redis-export

You should add ~/.local/bin/ to your PATH.

Quick Start
-----------

.. code-block:: bash

   redis-export PREFIX_OR_PATTERN OUTPUT_FILE
   redis-import INPUT_FILE

For example,

.. code-block:: bash

   # prefix based export
   redis-export 'phonebook:' ~/d/t1.json
   # pattern based export
   # redis-export 'phonebook:*:name:*' ~/d/t1.json
   redis-import --host redis.example.com ~/d/t1.json

For more usage help, run the command with --help option.

Documentation
-------------

redis-export will export keys with given pattern to a json file (keys and
values both base64 encoded).

redis-import will import those keys and values back to redis.

Implementation Detail
-------------------------

- SCAN is used to iterate over keys with given pattern.
- DUMP is used to dump the key.
- RESTORE is used to restore a key. force-replace param is set to TRUE.

Exported file is a json list, each list item is of form (key, dump_value).
The redis key and dump value is encoded in base64 in order to fit in regular
json.

License
----------

Copyright (C) 2022 Yuanle Song <sylecn@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

ChangeLog
---------

* v0.2.0 2022-09-24

  - update README.rst, applied license, distributed on PyPI.

* v0.1.2 2022-09-18

  - bugfix: when pattern contains '*' should not error

* v0.1.0 2021-11-21

  - initial release
