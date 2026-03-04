"""\
Export a MySQL table to CSV without loading all rows into memory.

Usage examples:
  python export_table.py --table dta
  python export_table.py --table ppi --out output/ppi.csv
  python export_table.py --table drug_protein_action --chunk-size 50000

Notes:
- Connection settings are taken from config.Config (env vars supported).
- For very large tables, export and open the CSV to view all rows.
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple

import pymysql

from config import Config


def _escape_identifier(name: str) -> str:
    """Backtick-escape an identifier for MySQL."""
    return "`" + name.replace("`", "``") + "`"


def _ensure_output_path(path_str: str) -> Path:
    path = Path(path_str)
    if not path.is_absolute():
        path = Path.cwd() / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _connect() -> pymysql.connections.Connection:
    cfg = Config.get_db_config()
    return pymysql.connect(
        host=cfg["host"],
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"],
        port=cfg.get("port", 3306),
        charset=cfg.get("charset", "utf8mb4"),
        autocommit=True,
    )


def _table_exists(conn: pymysql.connections.Connection, table: str) -> bool:
    with conn.cursor() as cursor:
        cursor.execute("SHOW TABLES LIKE %s", (table,))
        return cursor.fetchone() is not None


def _get_columns(conn: pymysql.connections.Connection, table: str) -> List[str]:
    with conn.cursor() as cursor:
        cursor.execute(f"SHOW COLUMNS FROM {_escape_identifier(table)}")
        rows = cursor.fetchall()

    # PyMySQL returns tuples by default: (Field, Type, Null, Key, Default, Extra)
    return [row[0] for row in rows]


def _count_rows(conn: pymysql.connections.Connection, table: str, where: Optional[str]) -> Optional[int]:
    sql = f"SELECT COUNT(*) FROM {_escape_identifier(table)}"
    if where:
        sql += f" WHERE {where}"
    with conn.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchone()
        if not row:
            return None
        return int(row[0])


def _iter_rows(
    conn: pymysql.connections.Connection,
    table: str,
    columns: Sequence[str],
    where: Optional[str],
    order_by: Optional[str],
    chunk_size: int,
) -> Iterable[Sequence[object]]:
    sql = "SELECT " + ", ".join(_escape_identifier(c) for c in columns)
    sql += f" FROM {_escape_identifier(table)}"
    if where:
        sql += f" WHERE {where}"
    if order_by:
        sql += f" ORDER BY {order_by}"

    stream_cursor = conn.cursor(pymysql.cursors.SSCursor)
    stream_cursor.arraysize = chunk_size
    try:
        stream_cursor.execute(sql)
        while True:
            batch = stream_cursor.fetchmany(chunk_size)
            if not batch:
                break
            for row in batch:
                yield row
    finally:
        stream_cursor.close()


def export_table_to_csv(
    table: str,
    out_path: Path,
    where: Optional[str],
    order_by: Optional[str],
    chunk_size: int,
    include_header: bool,
    encoding: str,
    no_count: bool,
) -> None:
    start = time.time()

    conn = _connect()
    try:
        if not _table_exists(conn, table):
            raise SystemExit(f"[ERROR] Table not found: {table}")

        columns = _get_columns(conn, table)
        total = None if no_count else _count_rows(conn, table, where)

        exported = 0
        with out_path.open("w", newline="", encoding=encoding) as f:
            writer = csv.writer(f)
            if include_header:
                writer.writerow(columns)

            for row in _iter_rows(conn, table, columns, where, order_by, chunk_size):
                writer.writerow(row)
                exported += 1
                if exported % max(1, chunk_size) == 0:
                    if total is not None and total > 0:
                        pct = exported / total * 100
                        print(f"[PROGRESS] {exported}/{total} ({pct:.1f}%)")
                    else:
                        print(f"[PROGRESS] exported {exported} rows")

        seconds = time.time() - start
        if total is not None:
            print(f"[DONE] Exported {exported}/{total} rows -> {out_path} ({seconds:.1f}s)")
        else:
            print(f"[DONE] Exported {exported} rows -> {out_path} ({seconds:.1f}s)")

    finally:
        conn.close()


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Export a MySQL table to CSV")
    parser.add_argument("--table", required=True, help="table name in drug_discovery")
    parser.add_argument(
        "--out",
        default=None,
        help="output CSV path (default: output/<table>.csv)",
    )
    parser.add_argument(
        "--where",
        default=None,
        help="optional SQL WHERE clause (without the 'WHERE' keyword)",
    )
    parser.add_argument(
        "--order-by",
        default=None,
        help="optional SQL ORDER BY clause (without the 'ORDER BY' keyword)",
    )
    parser.add_argument("--chunk-size", type=int, default=100_000)
    parser.add_argument("--no-header", action="store_true", help="do not write CSV header")
    parser.add_argument(
        "--encoding",
        default="utf-8-sig",
        help="CSV encoding (default utf-8-sig, friendly for Excel)",
    )
    parser.add_argument("--no-count", action="store_true", help="skip COUNT(*)")

    args = parser.parse_args(argv)

    out = args.out
    if out is None:
        out = str(Path("output") / f"{args.table}.csv")

    out_path = _ensure_output_path(out)

    export_table_to_csv(
        table=args.table,
        out_path=out_path,
        where=args.where,
        order_by=args.order_by,
        chunk_size=max(1, int(args.chunk_size)),
        include_header=not args.no_header,
        encoding=str(args.encoding),
        no_count=bool(args.no_count),
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
