# denodo/__init__.py
#
# Copyright (C) 2005-2021 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
#
# This software is part of the DenodoConnect component collection and
# is based on the PostgreSQL dialect of SQLAlchemy.
# Copyright (c) 2022, denodo technologies (http://www.denodo.com)
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from . import base
from . import pg8000  # noqa
from . import psycopg2  # noqa
from . import psycopg2cffi  # noqa
from . import pygresql  # noqa
from . import pypostgresql  # noqa
from .array import All
from .array import Any
from .array import ARRAY
from .array import array
from .base import BIGINT
from .base import BIT
from .base import BOOLEAN
from .base import BYTEA
from .base import CHAR
from .base import CIDR
from .base import CreateEnumType
from .base import DATE
from .base import DOUBLE_PRECISION
from .base import DropEnumType
from .base import ENUM
from .base import FLOAT
from .base import INET
from .base import INTEGER
from .base import INTERVAL
from .base import MACADDR
from .base import MONEY
from .base import NUMERIC
from .base import OID
from .base import REAL
from .base import SMALLINT
from .base import TEXT
from .base import TIME
from .base import TIMESTAMP
from .base import TSVECTOR
from .base import UUID
from .base import VARCHAR
from .dml import Insert
from .dml import insert
from .ext import aggregate_order_by
from .ext import array_agg
from .ext import ExcludeConstraint
from .jsond import JSON
from .jsond import JSONB
from .ranges import DATERANGE
from .ranges import INT4RANGE
from .ranges import INT8RANGE
from .ranges import NUMRANGE
from .ranges import TSRANGE
from .ranges import TSTZRANGE
from sqlalchemy.util import compat

if compat.py3k:
    from . import asyncpg  # noqa

base.dialect = dialect = psycopg2.dialect


__all__ = (
    "INTEGER",
    "BIGINT",
    "SMALLINT",
    "VARCHAR",
    "CHAR",
    "TEXT",
    "NUMERIC",
    "FLOAT",
    "REAL",
    "INET",
    "CIDR",
    "UUID",
    "BIT",
    "MACADDR",
    "MONEY",
    "OID",
    "DOUBLE_PRECISION",
    "TIMESTAMP",
    "TIME",
    "DATE",
    "BYTEA",
    "BOOLEAN",
    "INTERVAL",
    "ARRAY",
    "ENUM",
    "dialect",
    "array",
    "INT4RANGE",
    "INT8RANGE",
    "NUMRANGE",
    "DATERANGE",
    "TSVECTOR",
    "TSRANGE",
    "TSTZRANGE",
    "JSON",
    "JSONB",
    "Any",
    "All",
    "DropEnumType",
    "CreateEnumType",
    "ExcludeConstraint",
    "aggregate_order_by",
    "array_agg",
    "insert",
    "Insert",
)
