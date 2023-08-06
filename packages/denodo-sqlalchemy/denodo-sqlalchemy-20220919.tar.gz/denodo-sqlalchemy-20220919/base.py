# denodo/base.py
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

from collections import defaultdict
import datetime as dt
import re
from uuid import UUID as _python_UUID

from . import array as _array
from . import jsond as _json
from . import ranges as _ranges
from sqlalchemy import exc
from sqlalchemy import schema
from sqlalchemy import sql
from sqlalchemy import util
from sqlalchemy.engine import characteristics
from sqlalchemy.engine import default
from sqlalchemy.engine import reflection
from sqlalchemy.sql import coercions
from sqlalchemy.sql import compiler
from sqlalchemy.sql import elements
from sqlalchemy.sql import expression
from sqlalchemy.sql import roles
from sqlalchemy.sql import sqltypes
from sqlalchemy.sql import util as sql_util
from sqlalchemy.sql.ddl import DDLBase
from sqlalchemy.types import BIGINT
from sqlalchemy.types import BINARY
from sqlalchemy.types import BOOLEAN
from sqlalchemy.types import CHAR
from sqlalchemy.types import DATE
from sqlalchemy.types import DECIMAL
from sqlalchemy.types import FLOAT
from sqlalchemy.types import INTEGER
from sqlalchemy.types import NUMERIC
from sqlalchemy.types import NVARCHAR
from sqlalchemy.types import REAL
from sqlalchemy.types import SMALLINT
from sqlalchemy.types import TEXT
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.types import VARCHAR


IDX_USING = re.compile(r"^(?:btree|hash|gist|gin|[\w_]+)$", re.I)

AUTOCOMMIT_REGEXP = re.compile(
    r"\s*(?:UPDATE|INSERT|CREATE|DELETE|DROP|ALTER|GRANT|REVOKE|"
    "IMPORT FOREIGN SCHEMA|REFRESH MATERIALIZED VIEW|TRUNCATE)",
    re.I | re.UNICODE,
)

RESERVED_WORDS = set(
    [
        "all",
        "analyse",
        "analyze",
        "and",
        "any",
        "array",
        "as",
        "asc",
        "asymmetric",
        "both",
        "case",
        "cast",
        "check",
        "collate",
        "column",
        "constraint",
        "create",
        "current_catalog",
        "current_date",
        "current_role",
        "current_time",
        "current_timestamp",
        "current_user",
        "default",
        "deferrable",
        "desc",
        "distinct",
        "do",
        "else",
        "end",
        "except",
        "false",
        "fetch",
        "for",
        "foreign",
        "from",
        "grant",
        "group",
        "having",
        "in",
        "initially",
        "intersect",
        "into",
        "leading",
        "limit",
        "localtime",
        "localtimestamp",
        "new",
        "not",
        "null",
        "of",
        "off",
        "offset",
        "old",
        "on",
        "only",
        "or",
        "order",
        "placing",
        "primary",
        "references",
        "returning",
        "select",
        "session_user",
        "some",
        "symmetric",
        "table",
        "then",
        "to",
        "trailing",
        "true",
        "union",
        "unique",
        "user",
        "using",
        "variadic",
        "when",
        "where",
        "window",
        "with",
        "authorization",
        "between",
        "binary",
        "cross",
        "current_schema",
        "freeze",
        "full",
        "ilike",
        "inner",
        "is",
        "isnull",
        "join",
        "left",
        "like",
        "natural",
        "notnull",
        "outer",
        "over",
        "overlaps",
        "right",
        "similar",
        "verbose",
    ]
)

_DECIMAL_TYPES = (1231, 1700)
_FLOAT_TYPES = (700, 701, 1021, 1022)
_INT_TYPES = (20, 21, 23, 26, 1005, 1007, 1016)


class BYTEA(sqltypes.LargeBinary):
    __visit_name__ = "BYTEA"


class DOUBLE_PRECISION(sqltypes.Float):
    __visit_name__ = "DOUBLE_PRECISION"


class INET(sqltypes.TypeEngine):
    __visit_name__ = "INET"


PGInet = INET


class CIDR(sqltypes.TypeEngine):
    __visit_name__ = "CIDR"


PGCidr = CIDR


class MACADDR(sqltypes.TypeEngine):
    __visit_name__ = "MACADDR"


PGMacAddr = MACADDR


class MONEY(sqltypes.TypeEngine):

    r"""Provide the PostgreSQL MONEY type.

    Depending on driver, result rows using this type may return a
    string value which includes currency symbols.

    For this reason, it may be preferable to provide conversion to a
    numerically-based currency datatype using :class:`_types.TypeDecorator`::

        import re
        import decimal
        from sqlalchemy import TypeDecorator

        class NumericMoney(TypeDecorator):
            impl = MONEY

            def process_result_value(self, value: Any, dialect: Any) -> None:
                if value is not None:
                    # adjust this for the currency and numeric
                    m = re.match(r"\$([\d.]+)", value)
                    if m:
                        value = decimal.Decimal(m.group(1))
                return value

    Alternatively, the conversion may be applied as a CAST using
    the :meth:`_types.TypeDecorator.column_expression` method as follows::

        import decimal
        from sqlalchemy import cast
        from sqlalchemy import TypeDecorator

        class NumericMoney(TypeDecorator):
            impl = MONEY

            def column_expression(self, column: Any):
                return cast(column, Numeric())

    .. versionadded:: 1.2

    """

    __visit_name__ = "MONEY"


class OID(sqltypes.TypeEngine):

    """Provide the PostgreSQL OID type.

    .. versionadded:: 0.9.5

    """

    __visit_name__ = "OID"


class REGCLASS(sqltypes.TypeEngine):

    """Provide the PostgreSQL REGCLASS type.

    .. versionadded:: 1.2.7

    """

    __visit_name__ = "REGCLASS"


class TIMESTAMP(sqltypes.TIMESTAMP):
    def __init__(self, timezone=False, precision=None):
        super(TIMESTAMP, self).__init__(timezone=timezone)
        self.precision = precision


class TIME(sqltypes.TIME):
    def __init__(self, timezone=False, precision=None):
        super(TIME, self).__init__(timezone=timezone)
        self.precision = precision


class INTERVAL(sqltypes.NativeForEmulated, sqltypes._AbstractInterval):

    """PostgreSQL INTERVAL type."""

    __visit_name__ = "INTERVAL"
    native = True

    def __init__(self, precision=None, fields=None):
        """Construct an INTERVAL.

        :param precision: optional integer precision value
        :param fields: string fields specifier.  allows storage of fields
         to be limited, such as ``"YEAR"``, ``"MONTH"``, ``"DAY TO HOUR"``,
         etc.

         .. versionadded:: 1.2

        """
        self.precision = precision
        self.fields = fields

    @classmethod
    def adapt_emulated_to_native(cls, interval, **kw):
        return INTERVAL(precision=interval.second_precision)

    @property
    def _type_affinity(self):
        return sqltypes.Interval

    def as_generic(self, allow_nulltype=False):
        return sqltypes.Interval(native=True, second_precision=self.precision)

    @property
    def python_type(self):
        return dt.timedelta

    def coerce_compared_value(self, op, value):
        return self


PGInterval = INTERVAL


class BIT(sqltypes.TypeEngine):
    __visit_name__ = "BIT"

    def __init__(self, length=None, varying=False):
        if not varying:
            # BIT without VARYING defaults to length 1
            self.length = length or 1
        else:
            # but BIT VARYING can be unlimited-length, so no default
            self.length = length
        self.varying = varying


PGBit = BIT


class UUID(sqltypes.TypeEngine):

    """PostgreSQL UUID type.

    Represents the UUID column type, interpreting
    data either as natively returned by the DBAPI
    or as Python uuid objects.

    The UUID type is currently known to work within the prominent DBAPI
    drivers supported by SQLAlchemy including psycopg2, pg8000 and
    asyncpg. Support for other DBAPI drivers may be incomplete or non-present.

    """

    __visit_name__ = "UUID"

    def __init__(self, as_uuid=False):
        """Construct a UUID type.


        :param as_uuid=False: if True, values will be interpreted
         as Python uuid objects, converting to/from string via the
         DBAPI.

        """
        self.as_uuid = as_uuid

    def coerce_compared_value(self, op, value):
        """See :meth:`.TypeEngine.coerce_compared_value` for a description."""

        if isinstance(value, util.string_types):
            return self
        else:
            return super(UUID, self).coerce_compared_value(op, value)

    def bind_processor(self, dialect):
        if self.as_uuid:

            def process(value):
                if value is not None:
                    value = util.text_type(value)
                return value

            return process
        else:
            return None

    def result_processor(self, dialect, coltype):
        if self.as_uuid:

            def process(value):
                if value is not None:
                    value = _python_UUID(value)
                return value

            return process
        else:
            return None


PGUuid = UUID


class TSVECTOR(sqltypes.TypeEngine):

    """The :class:`_postgresql.TSVECTOR` type implements the PostgreSQL
    text search type TSVECTOR.

    It can be used to do full text queries on natural language
    documents.

    .. versionadded:: 0.9.0

    .. seealso::

        :ref:`postgresql_match`

    """

    __visit_name__ = "TSVECTOR"


class ENUM(sqltypes.NativeForEmulated, sqltypes.Enum):

    """PostgreSQL ENUM type.

    This is a subclass of :class:`_types.Enum` which includes
    support for PG's ``CREATE TYPE`` and ``DROP TYPE``.

    When the builtin type :class:`_types.Enum` is used and the
    :paramref:`.Enum.native_enum` flag is left at its default of
    True, the PostgreSQL backend will use a :class:`_postgresql.ENUM`
    type as the implementation, so the special create/drop rules
    will be used.

    The create/drop behavior of ENUM is necessarily intricate, due to the
    awkward relationship the ENUM type has in relationship to the
    parent table, in that it may be "owned" by just a single table, or
    may be shared among many tables.

    When using :class:`_types.Enum` or :class:`_postgresql.ENUM`
    in an "inline" fashion, the ``CREATE TYPE`` and ``DROP TYPE`` is emitted
    corresponding to when the :meth:`_schema.Table.create` and
    :meth:`_schema.Table.drop`
    methods are called::

        table = Table('sometable', metadata,
            Column('some_enum', ENUM('a', 'b', 'c', name='myenum'))
        )

        table.create(engine)  # will emit CREATE ENUM and CREATE TABLE
        table.drop(engine)  # will emit DROP TABLE and DROP ENUM

    To use a common enumerated type between multiple tables, the best
    practice is to declare the :class:`_types.Enum` or
    :class:`_postgresql.ENUM` independently, and associate it with the
    :class:`_schema.MetaData` object itself::

        my_enum = ENUM('a', 'b', 'c', name='myenum', metadata=metadata)

        t1 = Table('sometable_one', metadata,
            Column('some_enum', myenum)
        )

        t2 = Table('sometable_two', metadata,
            Column('some_enum', myenum)
        )

    When this pattern is used, care must still be taken at the level
    of individual table creates.  Emitting CREATE TABLE without also
    specifying ``checkfirst=True`` will still cause issues::

        t1.create(engine) # will fail: no such type 'myenum'

    If we specify ``checkfirst=True``, the individual table-level create
    operation will check for the ``ENUM`` and create if not exists::

        # will check if enum exists, and emit CREATE TYPE if not
        t1.create(engine, checkfirst=True)

    When using a metadata-level ENUM type, the type will always be created
    and dropped if either the metadata-wide create/drop is called::

        metadata.create_all(engine)  # will emit CREATE TYPE
        metadata.drop_all(engine)  # will emit DROP TYPE

    The type can also be created and dropped directly::

        my_enum.create(engine)
        my_enum.drop(engine)

    .. versionchanged:: 1.0.0 The PostgreSQL :class:`_postgresql.ENUM` type
       now behaves more strictly with regards to CREATE/DROP.  A metadata-level
       ENUM type will only be created and dropped at the metadata level,
       not the table level, with the exception of
       ``table.create(checkfirst=True)``.
       The ``table.drop()`` call will now emit a DROP TYPE for a table-level
       enumerated type.

    """

    native_enum = True

    def __init__(self, *enums, **kw):
        """Construct an :class:`_postgresql.ENUM`.

        Arguments are the same as that of
        :class:`_types.Enum`, but also including
        the following parameters.

        :param create_type: Defaults to True.
         Indicates that ``CREATE TYPE`` should be
         emitted, after optionally checking for the
         presence of the type, when the parent
         table is being created; and additionally
         that ``DROP TYPE`` is called when the table
         is dropped.    When ``False``, no check
         will be performed and no ``CREATE TYPE``
         or ``DROP TYPE`` is emitted, unless
         :meth:`~.postgresql.ENUM.create`
         or :meth:`~.postgresql.ENUM.drop`
         are called directly.
         Setting to ``False`` is helpful
         when invoking a creation scheme to a SQL file
         without access to the actual database -
         the :meth:`~.postgresql.ENUM.create` and
         :meth:`~.postgresql.ENUM.drop` methods can
         be used to emit SQL to a target bind.

        """
        native_enum = kw.pop("native_enum", None)
        if native_enum is False:
            util.warn(
                "the native_enum flag does not apply to the "
                "sqlalchemy.dialects.postgresql.ENUM datatype; this type "
                "always refers to ENUM.   Use sqlalchemy.types.Enum for "
                "non-native enum."
            )
        self.create_type = kw.pop("create_type", True)
        super(ENUM, self).__init__(*enums, **kw)

    @classmethod
    def adapt_emulated_to_native(cls, impl, **kw):
        """Produce a PostgreSQL native :class:`_postgresql.ENUM` from plain
        :class:`.Enum`.

        """
        kw.setdefault("validate_strings", impl.validate_strings)
        kw.setdefault("name", impl.name)
        kw.setdefault("schema", impl.schema)
        kw.setdefault("inherit_schema", impl.inherit_schema)
        kw.setdefault("metadata", impl.metadata)
        kw.setdefault("_create_events", False)
        kw.setdefault("values_callable", impl.values_callable)
        kw.setdefault("omit_aliases", impl._omit_aliases)
        return cls(**kw)

    def create(self, bind=None, checkfirst=True):
        """Emit ``CREATE TYPE`` for this
        :class:`_postgresql.ENUM`.

        If the underlying dialect does not support
        PostgreSQL CREATE TYPE, no action is taken.

        :param bind: a connectable :class:`_engine.Engine`,
         :class:`_engine.Connection`, or similar object to emit
         SQL.
        :param checkfirst: if ``True``, a query against
         the PG catalog will be first performed to see
         if the type does not exist already before
         creating.

        """
        if not bind.dialect.supports_native_enum:
            return

        bind._run_ddl_visitor(self.EnumGenerator, self, checkfirst=checkfirst)

    def drop(self, bind=None, checkfirst=True):
        """Emit ``DROP TYPE`` for this
        :class:`_postgresql.ENUM`.

        If the underlying dialect does not support
        PostgreSQL DROP TYPE, no action is taken.

        :param bind: a connectable :class:`_engine.Engine`,
         :class:`_engine.Connection`, or similar object to emit
         SQL.
        :param checkfirst: if ``True``, a query against
         the PG catalog will be first performed to see
         if the type actually exists before dropping.

        """
        if not bind.dialect.supports_native_enum:
            return

        bind._run_ddl_visitor(self.EnumDropper, self, checkfirst=checkfirst)

    class EnumGenerator(DDLBase):
        def __init__(self, dialect, connection, checkfirst=False, **kwargs):
            super(ENUM.EnumGenerator, self).__init__(connection, **kwargs)
            self.checkfirst = checkfirst

        def _can_create_enum(self, enum):
            if not self.checkfirst:
                return True

            effective_schema = self.connection.schema_for_object(enum)

            return not self.connection.dialect.has_type(
                self.connection, enum.name, schema=effective_schema
            )

        def visit_enum(self, enum):
            if not self._can_create_enum(enum):
                return

            self.connection.execute(CreateEnumType(enum))

    class EnumDropper(DDLBase):
        def __init__(self, dialect, connection, checkfirst=False, **kwargs):
            super(ENUM.EnumDropper, self).__init__(connection, **kwargs)
            self.checkfirst = checkfirst

        def _can_drop_enum(self, enum):
            if not self.checkfirst:
                return True

            effective_schema = self.connection.schema_for_object(enum)

            return self.connection.dialect.has_type(
                self.connection, enum.name, schema=effective_schema
            )

        def visit_enum(self, enum):
            if not self._can_drop_enum(enum):
                return

            self.connection.execute(DropEnumType(enum))

    def _check_for_name_in_memos(self, checkfirst, kw):
        """Look in the 'ddl runner' for 'memos', then
        note our name in that collection.

        This to ensure a particular named enum is operated
        upon only once within any kind of create/drop
        sequence without relying upon "checkfirst".

        """
        if not self.create_type:
            return True
        if "_ddl_runner" in kw:
            ddl_runner = kw["_ddl_runner"]
            if "_pg_enums" in ddl_runner.memo:
                pg_enums = ddl_runner.memo["_pg_enums"]
            else:
                pg_enums = ddl_runner.memo["_pg_enums"] = set()
            present = (self.schema, self.name) in pg_enums
            pg_enums.add((self.schema, self.name))
            return present
        else:
            return False

    def _on_table_create(self, target, bind, checkfirst=False, **kw):
        if (
            checkfirst
            or (
                not self.metadata
                and not kw.get("_is_metadata_operation", False)
            )
        ) and not self._check_for_name_in_memos(checkfirst, kw):
            self.create(bind=bind, checkfirst=checkfirst)

    def _on_table_drop(self, target, bind, checkfirst=False, **kw):
        if (
            not self.metadata
            and not kw.get("_is_metadata_operation", False)
            and not self._check_for_name_in_memos(checkfirst, kw)
        ):
            self.drop(bind=bind, checkfirst=checkfirst)

    def _on_metadata_create(self, target, bind, checkfirst=False, **kw):
        if not self._check_for_name_in_memos(checkfirst, kw):
            self.create(bind=bind, checkfirst=checkfirst)

    def _on_metadata_drop(self, target, bind, checkfirst=False, **kw):
        if not self._check_for_name_in_memos(checkfirst, kw):
            self.drop(bind=bind, checkfirst=checkfirst)


class _ColonCast(elements.Cast):
    __visit_name__ = "colon_cast"

    def __init__(self, expression, type_):
        self.type = type_
        self.clause = expression
        self.typeclause = elements.TypeClause(type_)


colspecs = {
    sqltypes.ARRAY: _array.ARRAY,
    sqltypes.Interval: INTERVAL,
    sqltypes.Enum: ENUM,
    sqltypes.JSON.JSONPathType: _json.JSONPathType,
    sqltypes.JSON: _json.JSON,
}

ischema_names = {
    "_array": _array.ARRAY,
    "json": _json.JSON,
    "jsonb": _json.JSONB,
    "int4range": _ranges.INT4RANGE,
    "int8range": _ranges.INT8RANGE,
    "numrange": _ranges.NUMRANGE,
    "daterange": _ranges.DATERANGE,
    "tsrange": _ranges.TSRANGE,
    "tstzrange": _ranges.TSTZRANGE,
    "integer": INTEGER,
    "bigint": BIGINT,
    "smallint": SMALLINT,
    "character varying": VARCHAR,
    "character": CHAR,
    '"char"': sqltypes.String,
    "name": sqltypes.String,
    "text": TEXT,
    "numeric": NUMERIC,
    "float": FLOAT,
    "real": REAL,
    "inet": INET,
    "cidr": CIDR,
    "uuid": UUID,
    "bit": BIT,
    "bit varying": BIT,
    "macaddr": MACADDR,
    "money": MONEY,
    "oid": OID,
    "regclass": REGCLASS,
    "double precision": DOUBLE_PRECISION,
    "timestamp": TIMESTAMP,
    "timestamp with time zone": TIMESTAMP,
    "timestamp without time zone": TIMESTAMP,
    "time with time zone": TIME,
    "time without time zone": TIME,
    "TIMESTAMP_WITH_TIMEZONE": TIMESTAMP,
    "date": DATE,
    "time": TIME,
    "bytea": BYTEA,
    "boolean": BOOLEAN,
    "interval": INTERVAL,
    "tsvector": TSVECTOR,
    'BIGINT': BIGINT,
    'BINARY': BINARY,
    'BIT': BIT,
    'BOOLEAN': BOOLEAN,
    'CHAR': CHAR,
    'CHARACTER': CHAR,
    'DATE': DATE, 
    'NUMERIC': NUMERIC,
    'DEC': DECIMAL,
    'DECIMAL': DECIMAL,
    'DOUBLE': FLOAT,
    'FIXED': DECIMAL,
    'FLOAT': FLOAT,
    'INT': INTEGER,
    'INTEGER': INTEGER,
    'NUMBER': DECIMAL,
    # 'OBJECT': ?
    'REAL': REAL,
    'BYTEINT': SMALLINT,
    'SMALLINT': SMALLINT,
    'STRING': VARCHAR,
    'TEXT': VARCHAR,
    'TIME': TIME,
    'TIMESTAMP': TIMESTAMP,
    'TIMESTAMP_LTZ': TIMESTAMP,
    'TIMESTAMP_TZ': TIMESTAMP,
    'TIMESTAMP_NTZ': TIMESTAMP,
    'TINYINT': SMALLINT,
    'VARBINARY': BINARY,
    'VARCHAR': VARCHAR,
    'NVARCHAR': NVARCHAR,
}


class PGCompiler(compiler.SQLCompiler):
    def visit_colon_cast(self, element, **kw):
        return "%s::%s" % (
            element.clause._compiler_dispatch(self, **kw),
            element.typeclause._compiler_dispatch(self, **kw),
        )

    def visit_array(self, element, **kw):
        return "ARRAY[%s]" % self.visit_clauselist(element, **kw)

    def visit_slice(self, element, **kw):
        return "%s:%s" % (
            self.process(element.start, **kw),
            self.process(element.stop, **kw),
        )

    def visit_json_getitem_op_binary(
        self, binary, operator, _cast_applied=False, **kw
    ):
        if (
            not _cast_applied
            and binary.type._type_affinity is not sqltypes.JSON
        ):
            kw["_cast_applied"] = True
            return self.process(sql.cast(binary, binary.type), **kw)

        kw["eager_grouping"] = True

        return self._generate_generic_binary(
            binary, " -> " if not _cast_applied else " ->> ", **kw
        )

    def visit_json_path_getitem_op_binary(
        self, binary, operator, _cast_applied=False, **kw
    ):
        if (
            not _cast_applied
            and binary.type._type_affinity is not sqltypes.JSON
        ):
            kw["_cast_applied"] = True
            return self.process(sql.cast(binary, binary.type), **kw)

        kw["eager_grouping"] = True
        return self._generate_generic_binary(
            binary, " #> " if not _cast_applied else " #>> ", **kw
        )

    def visit_getitem_binary(self, binary, operator, **kw):
        return "%s[%s]" % (
            self.process(binary.left, **kw),
            self.process(binary.right, **kw),
        )

    def visit_aggregate_order_by(self, element, **kw):
        return "%s ORDER BY %s" % (
            self.process(element.target, **kw),
            self.process(element.order_by, **kw),
        )

    def visit_match_op_binary(self, binary, operator, **kw):
        if "postgresql_regconfig" in binary.modifiers:
            regconfig = self.render_literal_value(
                binary.modifiers["postgresql_regconfig"], sqltypes.STRINGTYPE
            )
            if regconfig:
                return "%s @@ to_tsquery(%s, %s)" % (
                    self.process(binary.left, **kw),
                    regconfig,
                    self.process(binary.right, **kw),
                )
        return "%s @@ to_tsquery(%s)" % (
            self.process(binary.left, **kw),
            self.process(binary.right, **kw),
        )

    def visit_ilike_op_binary(self, binary, operator, **kw):
        escape = binary.modifiers.get("escape", None)

        return "%s ILIKE %s" % (
            self.process(binary.left, **kw),
            self.process(binary.right, **kw),
        ) + (
            " ESCAPE " + self.render_literal_value(escape, sqltypes.STRINGTYPE)
            if escape
            else ""
        )

    def visit_not_ilike_op_binary(self, binary, operator, **kw):
        escape = binary.modifiers.get("escape", None)
        return "%s NOT ILIKE %s" % (
            self.process(binary.left, **kw),
            self.process(binary.right, **kw),
        ) + (
            " ESCAPE " + self.render_literal_value(escape, sqltypes.STRINGTYPE)
            if escape
            else ""
        )

    def _regexp_match(self, base_op, binary, operator, kw):
        flags = binary.modifiers["flags"]
        if flags is None:
            return self._generate_generic_binary(
                binary, " %s " % base_op, **kw
            )
        if isinstance(flags, elements.BindParameter) and flags.value == "i":
            return self._generate_generic_binary(
                binary, " %s* " % base_op, **kw
            )
        flags = self.process(flags, **kw)
        string = self.process(binary.left, **kw)
        pattern = self.process(binary.right, **kw)
        return "%s %s CONCAT('(?', %s, ')', %s)" % (
            string,
            base_op,
            flags,
            pattern,
        )

    def visit_regexp_match_op_binary(self, binary, operator, **kw):
        return self._regexp_match("~", binary, operator, kw)

    def visit_not_regexp_match_op_binary(self, binary, operator, **kw):
        return self._regexp_match("!~", binary, operator, kw)

    def visit_regexp_replace_op_binary(self, binary, operator, **kw):
        string = self.process(binary.left, **kw)
        pattern = self.process(binary.right, **kw)
        flags = binary.modifiers["flags"]
        if flags is not None:
            flags = self.process(flags, **kw)
        replacement = self.process(binary.modifiers["replacement"], **kw)
        if flags is None:
            return "REGEXP_REPLACE(%s, %s, %s)" % (
                string,
                pattern,
                replacement,
            )
        else:
            return "REGEXP_REPLACE(%s, %s, %s, %s)" % (
                string,
                pattern,
                replacement,
                flags,
            )

    def visit_empty_set_expr(self, element_types):
        # cast the empty set to the type we are comparing against.  if
        # we are comparing against the null type, pick an arbitrary
        # datatype for the empty set
        return "SELECT %s WHERE 1!=1" % (
            ", ".join(
                "CAST(NULL AS %s)"
                % self.dialect.type_compiler.process(
                    INTEGER() if type_._isnull else type_
                )
                for type_ in element_types or [INTEGER()]
            ),
        )

    def render_literal_value(self, value, type_):
        value = super(PGCompiler, self).render_literal_value(value, type_)

        if self.dialect._backslash_escapes:
            value = value.replace("\\", "\\\\")
        return value

    def visit_sequence(self, seq, **kw):
        return "nextval('%s')" % self.preparer.format_sequence(seq)

    def limit_clause(self, select, **kw):
        text = ""
        if select._limit_clause is not None:
            text += " \n LIMIT " + self.process(select._limit_clause, **kw)
        if select._offset_clause is not None:
            if select._limit_clause is None:
                text += "\n LIMIT ALL"
            text += " OFFSET " + self.process(select._offset_clause, **kw)
        return text

    def format_from_hint_text(self, sqltext, table, hint, iscrud):
        if hint.upper() != "ONLY":
            raise exc.CompileError("Unrecognized hint: %r" % hint)
        return "ONLY " + sqltext

    def get_select_precolumns(self, select, **kw):
        # Do not call super().get_select_precolumns because
        # it will warn/raise when distinct on is present
        if select._distinct or select._distinct_on:
            if select._distinct_on:
                return (
                    "DISTINCT ON ("
                    + ", ".join(
                        [
                            self.process(col, **kw)
                            for col in select._distinct_on
                        ]
                    )
                    + ") "
                )
            else:
                return "DISTINCT "
        else:
            return ""

    def for_update_clause(self, select, **kw):

        if select._for_update_arg.read:
            if select._for_update_arg.key_share:
                tmp = " FOR KEY SHARE"
            else:
                tmp = " FOR SHARE"
        elif select._for_update_arg.key_share:
            tmp = " FOR NO KEY UPDATE"
        else:
            tmp = " FOR UPDATE"

        if select._for_update_arg.of:

            tables = util.OrderedSet()
            for c in select._for_update_arg.of:
                tables.update(sql_util.surface_selectables_only(c))

            tmp += " OF " + ", ".join(
                self.process(table, ashint=True, use_schema=False, **kw)
                for table in tables
            )

        if select._for_update_arg.nowait:
            tmp += " NOWAIT"
        if select._for_update_arg.skip_locked:
            tmp += " SKIP LOCKED"

        return tmp

    def returning_clause(self, stmt, returning_cols):

        columns = [
            self._label_returning_column(stmt, c)
            for c in expression._select_iterables(returning_cols)
        ]

        return "RETURNING " + ", ".join(columns)

    def visit_substring_func(self, func, **kw):
        s = self.process(func.clauses.clauses[0], **kw)
        start = self.process(func.clauses.clauses[1], **kw)
        if len(func.clauses.clauses) > 2:
            length = self.process(func.clauses.clauses[2], **kw)
            return "SUBSTRING(%s FROM %s FOR %s)" % (s, start, length)
        else:
            return "SUBSTRING(%s FROM %s)" % (s, start)

    def _on_conflict_target(self, clause, **kw):

        if clause.constraint_target is not None:
            # target may be a name of an Index, UniqueConstraint or
            # ExcludeConstraint.  While there is a separate
            # "max_identifier_length" for indexes, PostgreSQL uses the same
            # length for all objects so we can use
            # truncate_and_render_constraint_name
            target_text = (
                "ON CONSTRAINT %s"
                % self.preparer.truncate_and_render_constraint_name(
                    clause.constraint_target
                )
            )
        elif clause.inferred_target_elements is not None:
            target_text = "(%s)" % ", ".join(
                (
                    self.preparer.quote(c)
                    if isinstance(c, util.string_types)
                    else self.process(c, include_table=False, use_schema=False)
                )
                for c in clause.inferred_target_elements
            )
            if clause.inferred_target_whereclause is not None:
                target_text += " WHERE %s" % self.process(
                    clause.inferred_target_whereclause,
                    include_table=False,
                    use_schema=False,
                )
        else:
            target_text = ""

        return target_text

    def visit_on_conflict_do_nothing(self, on_conflict, **kw):

        target_text = self._on_conflict_target(on_conflict, **kw)

        if target_text:
            return "ON CONFLICT %s DO NOTHING" % target_text
        else:
            return "ON CONFLICT DO NOTHING"

    def visit_on_conflict_do_update(self, on_conflict, **kw):

        clause = on_conflict

        target_text = self._on_conflict_target(on_conflict, **kw)

        action_set_ops = []

        set_parameters = dict(clause.update_values_to_set)
        # create a list of column assignment clauses as tuples

        insert_statement = self.stack[-1]["selectable"]
        cols = insert_statement.table.c
        for c in cols:
            col_key = c.key

            if col_key in set_parameters:
                value = set_parameters.pop(col_key)
            elif c in set_parameters:
                value = set_parameters.pop(c)
            else:
                continue

            if coercions._is_literal(value):
                value = elements.BindParameter(None, value, type_=c.type)

            else:
                if (
                    isinstance(value, elements.BindParameter)
                    and value.type._isnull
                ):
                    value = value._clone()
                    value.type = c.type
            value_text = self.process(value.self_group(), use_schema=False)

            key_text = self.preparer.quote(col_key)
            action_set_ops.append("%s = %s" % (key_text, value_text))

        # check for names that don't match columns
        if set_parameters:
            util.warn(
                "Additional column names not matching "
                "any column keys in table '%s': %s"
                % (
                    self.current_executable.table.name,
                    (", ".join("'%s'" % c for c in set_parameters)),
                )
            )
            for k, v in set_parameters.items():
                key_text = (
                    self.preparer.quote(k)
                    if isinstance(k, util.string_types)
                    else self.process(k, use_schema=False)
                )
                value_text = self.process(
                    coercions.expect(roles.ExpressionElementRole, v),
                    use_schema=False,
                )
                action_set_ops.append("%s = %s" % (key_text, value_text))

        action_text = ", ".join(action_set_ops)
        if clause.update_whereclause is not None:
            action_text += " WHERE %s" % self.process(
                clause.update_whereclause, include_table=True, use_schema=False
            )

        return "ON CONFLICT %s DO UPDATE SET %s" % (target_text, action_text)

    def update_from_clause(
        self, update_stmt, from_table, extra_froms, from_hints, **kw
    ):
        kw["asfrom"] = True
        return "FROM " + ", ".join(
            t._compiler_dispatch(self, fromhints=from_hints, **kw)
            for t in extra_froms
        )

    def delete_extra_from_clause(
        self, delete_stmt, from_table, extra_froms, from_hints, **kw
    ):
        """Render the DELETE .. USING clause specific to PostgreSQL."""
        kw["asfrom"] = True
        return "USING " + ", ".join(
            t._compiler_dispatch(self, fromhints=from_hints, **kw)
            for t in extra_froms
        )

    def fetch_clause(self, select, **kw):
        # pg requires parens for non literal clauses. It's also required for
        # bind parameters if a ::type casts is used by the driver (asyncpg),
        # so it's easiest to just always add it
        text = ""
        if select._offset_clause is not None:
            text += "\n OFFSET (%s) ROWS" % self.process(
                select._offset_clause, **kw
            )
        if select._fetch_clause is not None:
            text += "\n FETCH FIRST (%s)%s ROWS %s" % (
                self.process(select._fetch_clause, **kw),
                " PERCENT" if select._fetch_clause_options["percent"] else "",
                "WITH TIES"
                if select._fetch_clause_options["with_ties"]
                else "ONLY",
            )
        return text


class PGDDLCompiler(compiler.DDLCompiler):
    def get_column_specification(self, column, **kwargs):

        colspec = self.preparer.format_column(column)
        impl_type = column.type.dialect_impl(self.dialect)
        if isinstance(impl_type, sqltypes.TypeDecorator):
            impl_type = impl_type.impl

        has_identity = (
            column.identity is not None
            and self.dialect.supports_identity_columns
        )

        if (
            column.primary_key
            and column is column.table._autoincrement_column
            and (
                self.dialect.supports_smallserial
                or not isinstance(impl_type, sqltypes.SmallInteger)
            )
            and not has_identity
            and (
                column.default is None
                or (
                    isinstance(column.default, schema.Sequence)
                    and column.default.optional
                )
            )
        ):
            if isinstance(impl_type, sqltypes.BigInteger):
                colspec += " BIGSERIAL"
            elif isinstance(impl_type, sqltypes.SmallInteger):
                colspec += " SMALLSERIAL"
            else:
                colspec += " SERIAL"
        else:
            colspec += " " + self.dialect.type_compiler.process(
                column.type,
                type_expression=column,
                identifier_preparer=self.preparer,
            )
            default = self.get_column_default_string(column)
            if default is not None:
                colspec += " DEFAULT " + default

        if column.computed is not None:
            colspec += " " + self.process(column.computed)
        if has_identity:
            colspec += " " + self.process(column.identity)

        if not column.nullable and not has_identity:
            colspec += " NOT NULL"
        elif column.nullable and has_identity:
            colspec += " NULL"
        return colspec

    def visit_check_constraint(self, constraint):
        if constraint._type_bound:
            typ = list(constraint.columns)[0].type
            if (
                isinstance(typ, sqltypes.ARRAY)
                and isinstance(typ.item_type, sqltypes.Enum)
                and not typ.item_type.native_enum
            ):
                raise exc.CompileError(
                    "PostgreSQL dialect cannot produce the CHECK constraint "
                    "for ARRAY of non-native ENUM; please specify "
                    "create_constraint=False on this Enum datatype."
                )

        return super(PGDDLCompiler, self).visit_check_constraint(constraint)

    def visit_drop_table_comment(self, drop):
        return "COMMENT ON TABLE %s IS NULL" % self.preparer.format_table(
            drop.element
        )

    def visit_create_enum_type(self, create):
        type_ = create.element

        return "CREATE TYPE %s AS ENUM (%s)" % (
            self.preparer.format_type(type_),
            ", ".join(
                self.sql_compiler.process(sql.literal(e), literal_binds=True)
                for e in type_.enums
            ),
        )

    def visit_drop_enum_type(self, drop):
        type_ = drop.element

        return "DROP TYPE %s" % (self.preparer.format_type(type_))

    def visit_create_index(self, create):
        preparer = self.preparer
        index = create.element
        self._verify_index_table(index)
        text = "CREATE "
        if index.unique:
            text += "UNIQUE "
        text += "INDEX "

        if self.dialect._supports_create_index_concurrently:
            concurrently = index.dialect_options["postgresql"]["concurrently"]
            if concurrently:
                text += "CONCURRENTLY "

        if create.if_not_exists:
            text += "IF NOT EXISTS "

        text += "%s ON %s " % (
            self._prepared_index_name(index, include_schema=False),
            preparer.format_table(index.table),
        )

        using = index.dialect_options["postgresql"]["using"]
        if using:
            text += (
                "USING %s "
                % self.preparer.validate_sql_phrase(using, IDX_USING).lower()
            )

        ops = index.dialect_options["postgresql"]["ops"]
        text += "(%s)" % (
            ", ".join(
                [
                    self.sql_compiler.process(
                        expr.self_group()
                        if not isinstance(expr, expression.ColumnClause)
                        else expr,
                        include_table=False,
                        literal_binds=True,
                    )
                    + (
                        (" " + ops[expr.key])
                        if hasattr(expr, "key") and expr.key in ops
                        else ""
                    )
                    for expr in index.expressions
                ]
            )
        )

        includeclause = index.dialect_options["postgresql"]["include"]
        if includeclause:
            inclusions = [
                index.table.c[col]
                if isinstance(col, util.string_types)
                else col
                for col in includeclause
            ]
            text += " INCLUDE (%s)" % ", ".join(
                [preparer.quote(c.name) for c in inclusions]
            )

        withclause = index.dialect_options["postgresql"]["with"]
        if withclause:
            text += " WITH (%s)" % (
                ", ".join(
                    [
                        "%s = %s" % storage_parameter
                        for storage_parameter in withclause.items()
                    ]
                )
            )

        tablespace_name = index.dialect_options["postgresql"]["tablespace"]
        if tablespace_name:
            text += " TABLESPACE %s" % preparer.quote(tablespace_name)

        whereclause = index.dialect_options["postgresql"]["where"]
        if whereclause is not None:
            whereclause = coercions.expect(
                roles.DDLExpressionRole, whereclause
            )

            where_compiled = self.sql_compiler.process(
                whereclause, include_table=False, literal_binds=True
            )
            text += " WHERE " + where_compiled

        return text

    def visit_drop_index(self, drop):
        index = drop.element

        text = "\nDROP INDEX "

        if self.dialect._supports_drop_index_concurrently:
            concurrently = index.dialect_options["postgresql"]["concurrently"]
            if concurrently:
                text += "CONCURRENTLY "

        if drop.if_exists:
            text += "IF EXISTS "

        text += self._prepared_index_name(index, include_schema=True)
        return text

    def visit_exclude_constraint(self, constraint, **kw):
        text = ""
        if constraint.name is not None:
            text += "CONSTRAINT %s " % self.preparer.format_constraint(
                constraint
            )
        elements = []
        for expr, name, op in constraint._render_exprs:
            kw["include_table"] = False
            exclude_element = self.sql_compiler.process(expr, **kw) + (
                (" " + constraint.ops[expr.key])
                if hasattr(expr, "key") and expr.key in constraint.ops
                else ""
            )

            elements.append("%s WITH %s" % (exclude_element, op))
        text += "EXCLUDE USING %s (%s)" % (
            self.preparer.validate_sql_phrase(
                constraint.using, IDX_USING
            ).lower(),
            ", ".join(elements),
        )
        if constraint.where is not None:
            text += " WHERE (%s)" % self.sql_compiler.process(
                constraint.where, literal_binds=True
            )
        text += self.define_constraint_deferrability(constraint)
        return text

    def post_create_table(self, table):
        table_opts = []
        pg_opts = table.dialect_options["postgresql"]

        inherits = pg_opts.get("inherits")
        if inherits is not None:
            if not isinstance(inherits, (list, tuple)):
                inherits = (inherits,)
            table_opts.append(
                "\n INHERITS ( "
                + ", ".join(self.preparer.quote(name) for name in inherits)
                + " )"
            )

        if pg_opts["partition_by"]:
            table_opts.append("\n PARTITION BY %s" % pg_opts["partition_by"])

        if pg_opts["with_oids"] is True:
            table_opts.append("\n WITH OIDS")
        elif pg_opts["with_oids"] is False:
            table_opts.append("\n WITHOUT OIDS")

        if pg_opts["on_commit"]:
            on_commit_options = pg_opts["on_commit"].replace("_", " ").upper()
            table_opts.append("\n ON COMMIT %s" % on_commit_options)

        if pg_opts["tablespace"]:
            tablespace_name = pg_opts["tablespace"]
            table_opts.append(
                "\n TABLESPACE %s" % self.preparer.quote(tablespace_name)
            )

        return "".join(table_opts)

    def visit_computed_column(self, generated):
        if generated.persisted is False:
            raise exc.CompileError(
                "PostrgreSQL computed columns do not support 'virtual' "
                "persistence; set the 'persisted' flag to None or True for "
                "PostgreSQL support."
            )

        return "GENERATED ALWAYS AS (%s) STORED" % self.sql_compiler.process(
            generated.sqltext, include_table=False, literal_binds=True
        )

    def visit_create_sequence(self, create, **kw):
        prefix = None
        if create.element.data_type is not None:
            prefix = " AS %s" % self.type_compiler.process(
                create.element.data_type
            )

        return super(PGDDLCompiler, self).visit_create_sequence(
            create, prefix=prefix, **kw
        )


class PGTypeCompiler(compiler.GenericTypeCompiler):
    def visit_TSVECTOR(self, type_, **kw):
        return "TSVECTOR"

    def visit_INET(self, type_, **kw):
        return "INET"

    def visit_CIDR(self, type_, **kw):
        return "CIDR"

    def visit_MACADDR(self, type_, **kw):
        return "MACADDR"

    def visit_MONEY(self, type_, **kw):
        return "MONEY"

    def visit_OID(self, type_, **kw):
        return "OID"

    def visit_FLOAT(self, type_, **kw):
        if not type_.precision:
            return "FLOAT"
        else:
            return "FLOAT(%(precision)s)" % {"precision": type_.precision}

    def visit_DOUBLE_PRECISION(self, type_, **kw):
        return "DOUBLE PRECISION"

    def visit_BIGINT(self, type_, **kw):
        return "BIGINT"

    def visit_JSON(self, type_, **kw):
        return "JSON"

    def visit_JSONB(self, type_, **kw):
        return "JSONB"

    def visit_INT4RANGE(self, type_, **kw):
        return "INT4RANGE"

    def visit_INT8RANGE(self, type_, **kw):
        return "INT8RANGE"

    def visit_NUMRANGE(self, type_, **kw):
        return "NUMRANGE"

    def visit_DATERANGE(self, type_, **kw):
        return "DATERANGE"

    def visit_TSRANGE(self, type_, **kw):
        return "TSRANGE"

    def visit_TSTZRANGE(self, type_, **kw):
        return "TSTZRANGE"

    def visit_datetime(self, type_, **kw):
        return self.visit_TIMESTAMP(type_, **kw)

    def visit_enum(self, type_, **kw):
        if not type_.native_enum or not self.dialect.supports_native_enum:
            return super(PGTypeCompiler, self).visit_enum(type_, **kw)
        else:
            return self.visit_ENUM(type_, **kw)

    def visit_ENUM(self, type_, identifier_preparer=None, **kw):
        if identifier_preparer is None:
            identifier_preparer = self.dialect.identifier_preparer
        return identifier_preparer.format_type(type_)

    def visit_TIMESTAMP(self, type_, **kw):
        return "TIMESTAMP%s %s" % (
            "(%d)" % type_.precision
            if getattr(type_, "precision", None) is not None
            else "",
            (type_.timezone and "WITH" or "WITHOUT") + " TIME ZONE",
        )

    def visit_TIME(self, type_, **kw):
        return "TIME%s %s" % (
            "(%d)" % type_.precision
            if getattr(type_, "precision", None) is not None
            else "",
            (type_.timezone and "WITH" or "WITHOUT") + " TIME ZONE",
        )

    def visit_INTERVAL(self, type_, **kw):
        text = "INTERVAL"
        if type_.fields is not None:
            text += " " + type_.fields
        if type_.precision is not None:
            text += " (%d)" % type_.precision
        return text

    def visit_BIT(self, type_, **kw):
        if type_.varying:
            compiled = "BIT VARYING"
            if type_.length is not None:
                compiled += "(%d)" % type_.length
        else:
            compiled = "BIT(%d)" % type_.length
        return compiled

    def visit_UUID(self, type_, **kw):
        return "UUID"

    def visit_large_binary(self, type_, **kw):
        return self.visit_BYTEA(type_, **kw)

    def visit_BYTEA(self, type_, **kw):
        return "BYTEA"

    def visit_ARRAY(self, type_, **kw):

        inner = self.process(type_.item_type, **kw)
        return re.sub(
            r"((?: COLLATE.*)?)$",
            (
                r"%s\1"
                % (
                    "[]"
                    * (type_.dimensions if type_.dimensions is not None else 1)
                )
            ),
            inner,
            count=1,
        )


class PGIdentifierPreparer(compiler.IdentifierPreparer):

    reserved_words = RESERVED_WORDS

    def _unquote_identifier(self, value):
        if value[0] == self.initial_quote:
            value = value[1:-1].replace(
                self.escape_to_quote, self.escape_quote
            )
        return value

    def format_type(self, type_, use_schema=True):
        if not type_.name:
            raise exc.CompileError("PostgreSQL ENUM type requires a name.")

        name = self.quote(type_.name)
        effective_schema = self.schema_for_object(type_)

        if (
            not self.omit_schema
            and use_schema
            and effective_schema is not None
        ):
            name = self.quote_schema(effective_schema) + "." + name
        return name


class PGInspector(reflection.Inspector):
    def get_table_oid(self, table_name, schema=None):
        """Return the OID for the given table name."""

        with self._operation_context() as conn:
            return self.dialect.get_table_oid(
                conn, table_name, schema, info_cache=self.info_cache
            )

    def get_enums(self, schema=None):
        """Return a list of ENUM objects.

        Each member is a dictionary containing these fields:

            * name - name of the enum
            * schema - the schema name for the enum.
            * visible - boolean, whether or not this enum is visible
              in the default search path.
            * labels - a list of string labels that apply to the enum.

        :param schema: schema name.  If None, the default schema
         (typically 'public') is used.  May also be set to '*' to
         indicate load enums for all schemas.

        .. versionadded:: 1.0.0

        """
        schema = schema or self.default_schema_name
        with self._operation_context() as conn:
            return self.dialect._load_enums(conn, schema)

    def get_foreign_table_names(self, schema=None):
        """Return a list of FOREIGN TABLE names.

        Behavior is similar to that of
        :meth:`_reflection.Inspector.get_table_names`,
        except that the list is limited to those tables that report a
        ``relkind`` value of ``f``.

        .. versionadded:: 1.0.0

        """
        schema = schema or self.default_schema_name
        with self._operation_context() as conn:
            return self.dialect._get_foreign_table_names(conn, schema)

    def get_view_names(self, schema=None, include=("plain", "materialized")):
        """Return all view names in `schema`.

        :param schema: Optional, retrieve names from a non-default schema.
         For special quoting, use :class:`.quoted_name`.

        :param include: specify which types of views to return.  Passed
         as a string value (for a single type) or a tuple (for any number
         of types).  Defaults to ``('plain', 'materialized')``.

         .. versionadded:: 1.1

        """

        with self._operation_context() as conn:
            return self.dialect.get_view_names(
                conn, schema, info_cache=self.info_cache, include=include
            )


class CreateEnumType(schema._CreateDropBase):
    __visit_name__ = "create_enum_type"


class DropEnumType(schema._CreateDropBase):
    __visit_name__ = "drop_enum_type"


class PGExecutionContext(default.DefaultExecutionContext):
    def fire_sequence(self, seq, type_):
        return self._execute_scalar(
            (
                "select nextval('%s')"
                % self.identifier_preparer.format_sequence(seq)
            ),
            type_,
        )

    def get_insert_default(self, column):
        if column.primary_key and column is column.table._autoincrement_column:
            if column.server_default and column.server_default.has_argument:

                # pre-execute passive defaults on primary key columns
                return self._execute_scalar(
                    "select %s" % column.server_default.arg, column.type
                )

            elif column.default is None or (
                column.default.is_sequence and column.default.optional
            ):
                # execute the sequence associated with a SERIAL primary
                # key column. for non-primary-key SERIAL, the ID just
                # generates server side.

                try:
                    seq_name = column._postgresql_seq_name
                except AttributeError:
                    tab = column.table.name
                    col = column.name
                    tab = tab[0 : 29 + max(0, (29 - len(col)))]
                    col = col[0 : 29 + max(0, (29 - len(tab)))]
                    name = "%s_%s_seq" % (tab, col)
                    column._postgresql_seq_name = seq_name = name

                if column.table is not None:
                    effective_schema = self.connection.schema_for_object(
                        column.table
                    )
                else:
                    effective_schema = None

                if effective_schema is not None:
                    exc = 'select nextval(\'"%s"."%s"\')' % (
                        effective_schema,
                        seq_name,
                    )
                else:
                    exc = "select nextval('\"%s\"')" % (seq_name,)

                return self._execute_scalar(exc, column.type)

        return super(PGExecutionContext, self).get_insert_default(column)

    def should_autocommit_text(self, statement):
        return AUTOCOMMIT_REGEXP.match(statement)


class PGReadOnlyConnectionCharacteristic(
    characteristics.ConnectionCharacteristic
):
    transactional = True

    def reset_characteristic(self, dialect, dbapi_conn):
        dialect.set_readonly(dbapi_conn, False)

    def set_characteristic(self, dialect, dbapi_conn, value):
        dialect.set_readonly(dbapi_conn, value)

    def get_characteristic(self, dialect, dbapi_conn):
        return dialect.get_readonly(dbapi_conn)


class PGDeferrableConnectionCharacteristic(
    characteristics.ConnectionCharacteristic
):
    transactional = True

    def reset_characteristic(self, dialect, dbapi_conn):
        dialect.set_deferrable(dbapi_conn, False)

    def set_characteristic(self, dialect, dbapi_conn, value):
        dialect.set_deferrable(dbapi_conn, value)

    def get_characteristic(self, dialect, dbapi_conn):
        return dialect.get_deferrable(dbapi_conn)


class PGDialect(default.DefaultDialect):
    name = "denodo"
    supports_statement_cache = True
    supports_alter = True
    max_identifier_length = 63
    supports_sane_rowcount = True

    supports_native_enum = True
    supports_native_boolean = True
    supports_smallserial = True

    supports_sequences = True
    sequences_optional = True
    preexecute_autoincrement_sequences = True
    postfetch_lastrowid = False

    supports_comments = True
    supports_default_values = True

    supports_default_metavalue = True

    supports_empty_insert = False
    supports_multivalues_insert = True
    supports_identity_columns = True

    default_paramstyle = "pyformat"
    ischema_names = ischema_names
    colspecs = colspecs

    statement_compiler = PGCompiler
    ddl_compiler = PGDDLCompiler
    type_compiler = PGTypeCompiler
    preparer = PGIdentifierPreparer
    execution_ctx_cls = PGExecutionContext
    inspector = PGInspector
    isolation_level = None

    implicit_returning = True
    full_returning = True

    connection_characteristics = (
        default.DefaultDialect.connection_characteristics
    )
    connection_characteristics = connection_characteristics.union(
        {
            "postgresql_readonly": PGReadOnlyConnectionCharacteristic(),
            "postgresql_deferrable": PGDeferrableConnectionCharacteristic(),
        }
    )

    construct_arguments = [
        (
            schema.Index,
            {
                "using": False,
                "include": None,
                "where": None,
                "ops": {},
                "concurrently": False,
                "with": {},
                "tablespace": None,
            },
        ),
        (
            schema.Table,
            {
                "ignore_search_path": False,
                "tablespace": None,
                "partition_by": None,
                "with_oids": None,
                "on_commit": None,
                "inherits": None,
            },
        ),
    ]

    reflection_options = ("postgresql_ignore_search_path",)

    _backslash_escapes = True
    _supports_create_index_concurrently = True
    _supports_drop_index_concurrently = True

    def __init__(
        self,
        isolation_level=None,
        json_serializer=None,
        json_deserializer=None,
        **kwargs
    ):
        default.DefaultDialect.__init__(self, **kwargs)

        # the isolation_level parameter to the PGDialect itself is legacy.
        # still works however the execution_options method is the one that
        # is documented.
        self.isolation_level = isolation_level
        self._json_deserializer = json_deserializer
        self._json_serializer = json_serializer

    def initialize(self, connection):
        super(PGDialect, self).initialize(connection)

        if self.server_version_info <= (8, 2):
            self.full_returning = self.implicit_returning = False

        self.supports_native_enum = self.server_version_info >= (8, 3)
        if not self.supports_native_enum:
            self.colspecs = self.colspecs.copy()
            # pop base Enum type
            self.colspecs.pop(sqltypes.Enum, None)
            # psycopg2, others may have placed ENUM here as well
            self.colspecs.pop(ENUM, None)

        # https://www.postgresql.org/docs/9.3/static/release-9-2.html#AEN116689
        self.supports_smallserial = self.server_version_info >= (9, 2)

        self._backslash_escapes = self.server_version_info < (8, 2) == 'off'

        self._supports_create_index_concurrently = (
            self.server_version_info >= (8, 2)
        )
        self._supports_drop_index_concurrently = self.server_version_info >= (
            9,
            2,
        )
        self.supports_identity_columns = self.server_version_info >= (10,)

    def on_connect(self):
        if self.isolation_level is not None:

            def connect(conn):
                self.set_isolation_level(conn, self.isolation_level)

            return connect
        else:
            return None

    _isolation_lookup = set(
        [
            "SERIALIZABLE",
            "READ UNCOMMITTED",
            "READ COMMITTED",
            "REPEATABLE READ",
        ]
    )

    def set_isolation_level(self, connection, level):
        level = level.replace("_", " ")
        if level not in self._isolation_lookup:
            raise exc.ArgumentError(
                "Invalid value '%s' for isolation_level. "
                "Valid isolation levels for %s are %s"
                % (level, self.name, ", ".join(self._isolation_lookup))
            )
        cursor = connection.cursor()
        cursor.execute(
            "SET SESSION CHARACTERISTICS AS TRANSACTION "
            "ISOLATION LEVEL %s" % level
        )
        cursor.execute("COMMIT")
        cursor.close()

    def get_isolation_level(self, connection):
        return 'read committed'

    def set_readonly(self, connection, value):
        raise NotImplementedError()

    def get_readonly(self, connection):
        raise NotImplementedError()

    def set_deferrable(self, connection, value):
        raise NotImplementedError()

    def get_deferrable(self, connection):
        raise NotImplementedError()

    def do_begin_twophase(self, connection, xid):
        self.do_begin(connection.connection)

    def do_prepare_twophase(self, connection, xid):
        connection.exec_driver_sql("PREPARE TRANSACTION '%s'" % xid)

    def do_rollback_twophase(
        self, connection, xid, is_prepared=True, recover=False
    ):
        if is_prepared:
            if recover:
                # FIXME: ugly hack to get out of transaction
                # context when committing recoverable transactions
                # Must find out a way how to make the dbapi not
                # open a transaction.
                connection.exec_driver_sql("ROLLBACK")
            connection.exec_driver_sql("ROLLBACK PREPARED '%s'" % xid)
            connection.exec_driver_sql("BEGIN")
            self.do_rollback(connection.connection)
        else:
            self.do_rollback(connection.connection)

    def do_commit_twophase(
        self, connection, xid, is_prepared=True, recover=False
    ):
        if is_prepared:
            if recover:
                connection.exec_driver_sql("ROLLBACK")
            connection.exec_driver_sql("COMMIT PREPARED '%s'" % xid)
            connection.exec_driver_sql("BEGIN")
            self.do_rollback(connection.connection)
        else:
            self.do_commit(connection.connection)

    def do_recover_twophase(self, connection):
        resultset = connection.execute(
            sql.text("SELECT gid FROM pg_prepared_xacts")
        )
        return [row[0] for row in resultset]

    def _get_default_schema_name(self, connection):
        return connection.exec_driver_sql("select current_schema()").scalar()

    def has_schema(self, connection, schema):
        query = (
            "select nspname from pg_namespace " "where lower(nspname)=:schema"
        )
        cursor = connection.execute(
            sql.text(query).bindparams(
                sql.bindparam(
                    "schema",
                    util.text_type(schema.lower()),
                    type_=sqltypes.Unicode,
                )
            )
        )

        return bool(cursor.first())

    def has_table(self, connection, table_name, schema=None):
        self._ensure_has_table_connection(connection)
        # seems like case gets folded in pg_class...
        if schema is None:
            cursor = connection.execute(
                sql.text(
                    "select name as relname "
                    "FROM GET_ELEMENTS() "
                    "WHERE input_name = :name and input_type = 'Views' "
                ).bindparams(
                    sql.bindparam(
                        "name",
                        util.text_type(table_name),
                        type_=sqltypes.Unicode,
                    )
                )
            )
        else:
            cursor = connection.execute(
                sql.text(
                    "select name as relname "
                    "FROM GET_ELEMENTS() "
                    "WHERE input_name = :name and input_database_name = :schema and input_type = 'Views' "
                ).bindparams(
                    sql.bindparam(
                        "name",
                        util.text_type(table_name),
                        type_=sqltypes.Unicode,
                    ),
                    sql.bindparam(
                        "schema",
                        util.text_type(schema),
                        type_=sqltypes.Unicode,
                    ),
                )
            )
        return bool(cursor.first())

    def has_sequence(self, connection, sequence_name, schema=None):
        return false

    def has_type(self, connection, type_name, schema=None):
        return true

    def _get_server_version_info(self, connection):
        v = 'PostgreSQL 9.6.8'
        m = re.match(
            r".*(?:PostgreSQL|EnterpriseDB) "
            r"(\d+)\.?(\d+)?(?:\.(\d+))?(?:\.\d+)?(?:devel|beta)?",
            v,
        )
        if not m:
            raise AssertionError(
                "Could not determine version from string '%s'" % v
            )
        return tuple([int(x) for x in m.group(1, 2, 3) if x is not None])

    @reflection.cache
    def get_table_oid(self, connection, table_name, schema=None, **kw):
        return table_name

    @reflection.cache
    def get_schema_names(self, connection, **kw):
        result = connection.execute(
            sql.text(
                "select distinct database_name as nspname from get_elements() " 
                "where database_name is not null "
                "ORDER BY 1"
            ).columns(nspname=sqltypes.Unicode)
        )
        return [name for name, in result]

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        result = connection.execute(
            sql.text(
                "SELECT name as relname "
                "FROM GET_ELEMENTS() "
                "WHERE input_database_name = :schema and input_type = 'Views' "
            ).columns(relname=sqltypes.Unicode),
            dict(
                schema=schema
                if schema is not None
                else self.default_schema_name
            ),
        )
        return [name for name, in result]

    @reflection.cache
    def _get_foreign_table_names(self, connection, schema=None, **kw):
        return []

    @reflection.cache
    def get_view_names(
        self, connection, schema=None, include=("plain", "materialized"), **kw
    ):

        result = connection.execute(
            sql.text(
                "SELECT name as relname "
                "FROM GET_ELEMENTS() "
                "WHERE input_database_name = :schema and input_type = 'Views' "
                "and subtype = 'derived'"
            ).columns(relname=sqltypes.Unicode),
            dict(
                schema=schema
                if schema is not None
                else self.default_schema_name
            ),
        )
        return [name for name, in result]

    @reflection.cache
    def get_sequence_names(self, connection, schema=None, **kw):
        return []

    @reflection.cache
    def get_view_definition(self, connection, view_name, schema=None, **kw):
        return view_name

    @reflection.cache
    def get_columns(self, connection, table_name, schema=None, **kw):

        SQL_COLS = """
            select column_name as attname, column_sql_type as format_type, cast(null as text) as "DEFAULT", 
            column_is_nullable as attnotnull, column_is_autoincrement as autoincrement, rownum() as attnum,
            view_name as tableoid,  cast(null as text) as description from GET_VIEW_COLUMNS()
            WHERE input_database_name = :schema and input_view_name= :table_name
        """ 
        s = (
            sql.text(SQL_COLS)
            .bindparams(sql.bindparam("table_name", type_=sqltypes.Unicode),
                        sql.bindparam("schema", type_=sqltypes.Unicode))
            .columns(attname=sqltypes.Unicode, format_type=sqltypes.Unicode, default=sqltypes.Unicode)
        )
        c = connection.execute(s, dict(table_name=table_name, schema=schema))
        rows = c.fetchall()

        # dictionary with (name, ) if default search path or (schema, name)
        # as keys
        domains = self._load_domains(connection)

        # dictionary with (name, ) if default search path or (schema, name)
        # as keys
        enums = dict(
            ((rec["name"],), rec)
            if rec["visible"]
            else ((rec["schema"], rec["name"]), rec)
            for rec in self._load_enums(connection, schema="*")
        )

        # format columns
        columns = []
        generated = False

        for (
            name,
            format_type,
            default_,
            notnull,
            autoincrement,
            identity,
            table_oid,
            comment,
        ) in rows:
            column_info = self._get_column_info(
                name,
                format_type,
                default_,
                notnull,
                autoincrement,
                domains,
                enums,
                schema,
                comment,
                generated,
                identity,
            )
            columns.append(column_info)

        return columns

    def _get_column_info(
        self,
        name,
        format_type,
        default,
        notnull,
        autoincrement,
        domains,
        enums,
        schema,
        comment,
        generated,
        identity,
    ):
        def _handle_array_type(attype):
            return (
                # strip '[]' from integer[], etc.
                re.sub(r"\[\]$", "", attype),
                attype.endswith("[]"),
            )

        # strip (*) from character varying(5), timestamp(5)
        # with time zone, geometry(POLYGON), etc.
        attype = re.sub(r"\(.*\)", "", format_type)

        # strip '[]' from integer[], etc. and check if an array
        attype, is_array = _handle_array_type(attype)

        # strip quotes from case sensitive enum or domain names
        enum_or_domain_key = tuple(util.quoted_token_parser(attype))

        nullable = notnull

        charlen = re.search(r"\(([\d,]+)\)", format_type)
        if charlen:
            charlen = charlen.group(1)
        args = re.search(r"\((.*)\)", format_type)
        if args and args.group(1):
            args = tuple(re.split(r"\s*,\s*", args.group(1)))
        else:
            args = ()
        kwargs = {}

        if attype == "numeric":
            if charlen:
                prec, scale = charlen.split(",")
                args = (int(prec), int(scale))
            else:
                args = ()
        elif attype == "double precision":
            args = (53,)
        elif attype == "integer":
            args = ()
        elif attype in ("timestamp with time zone", "time with time zone"):
            kwargs["timezone"] = True
            if charlen:
                kwargs["precision"] = int(charlen)
            args = ()
        elif attype in (
            "timestamp without time zone",
            "time without time zone",
            "time",
        ):
            kwargs["timezone"] = False
            if charlen:
                kwargs["precision"] = int(charlen)
            args = ()
        elif attype == "bit varying":
            kwargs["varying"] = True
            if charlen:
                args = (int(charlen),)
            else:
                args = ()
        elif attype.startswith("interval"):
            field_match = re.match(r"interval (.+)", attype, re.I)
            if charlen:
                kwargs["precision"] = int(charlen)
            if field_match:
                kwargs["fields"] = field_match.group(1)
            attype = "interval"
            args = ()
        elif charlen:
            args = (int(charlen),)

        while True:
            # looping here to suit nested domains
            if attype in self.ischema_names:
                coltype = self.ischema_names[attype]
                break
            elif enum_or_domain_key in enums:
                enum = enums[enum_or_domain_key]
                coltype = ENUM
                kwargs["name"] = enum["name"]
                if not enum["visible"]:
                    kwargs["schema"] = enum["schema"]
                args = tuple(enum["labels"])
                break
            elif enum_or_domain_key in domains:
                domain = domains[enum_or_domain_key]
                attype = domain["attype"]
                attype, is_array = _handle_array_type(attype)
                # strip quotes from case sensitive enum or domain names
                enum_or_domain_key = tuple(util.quoted_token_parser(attype))
                # A table can't override a not null on the domain,
                # but can override nullable
                nullable = nullable and domain["nullable"]
                if domain["default"] and not default:
                    # It can, however, override the default
                    # value, but can't set it to null.
                    default = domain["default"]
                continue
            else:
                coltype = None
                break
                

        if coltype:
            coltype = coltype(*args, **kwargs)
            if is_array:
                coltype = self.ischema_names["_array"](coltype)
        else:
            util.warn(
                "Did not recognize type '%s' of column '%s'" % (attype, name)
            )
            coltype = sqltypes.NULLTYPE

        # If a zero byte or blank string depending on driver (is also absent
        # for older PG versions), then not a generated column. Otherwise, s =
        # stored. (Other values might be added in the future.)
        if generated not in (None, "", b"\x00"):
            computed = dict(
                sqltext=default, persisted=generated in ("s", b"s")
            )
            default = None
        else:
            computed = None

        column_info = dict(
            name=name,
            type=coltype,
            nullable=nullable,
            default=default,
            autoincrement=autoincrement,
            comment=comment,
        )
        if computed is not None:
            column_info["computed"] = computed
        if identity is not None:
            column_info["identity"] = identity
        return column_info

    @reflection.cache
    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        return None

    @reflection.cache
    def get_foreign_keys(
        self,
        connection,
        table_name,
        schema=None,
        postgresql_ignore_search_path=False,
        **kw
    ):
        return []

    def _pg_index_any(self, col, compare_to):
        if self.server_version_info < (8, 1):
            # https://www.postgresql.org/message-id/10279.1124395722@sss.pgh.pa.us
            # "In CVS tip you could replace this with "attnum = ANY (indkey)".
            # Unfortunately, most array support doesn't work on int2vector in
            # pre-8.1 releases, so I think you're kinda stuck with the above
            # for now.
            # regards, tom lane"
            return "(%s)" % " OR ".join(
                "%s[%d] = %s" % (compare_to, ind, col) for ind in range(0, 10)
            )
        else:
            return "%s = ANY(%s)" % (col, compare_to)

    @reflection.cache
    def get_indexes(self, connection, table_name, schema, **kw):
        table_oid = self.get_table_oid(
            connection, table_name, schema, info_cache=kw.get("info_cache")
        )

        return []

    @reflection.cache
    def get_unique_constraints(
        self, connection, table_name, schema=None, **kw
    ):
        return []

    @reflection.cache
    def get_table_comment(self, connection, table_name, schema=None, **kw):
        return {"text": ""}

    @reflection.cache
    def get_check_constraints(self, connection, table_name, schema=None, **kw):
        return []

    def _load_enums(self, connection, schema=None):
        return []

    def _load_domains(self, connection):
        return []
