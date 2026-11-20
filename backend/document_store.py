"""11월 19일 오후: SQLite documents.db에 문서를 저장하고 읽는 코드."""

import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_DIR / "sqlite_lab" / "documents.db"


def connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL UNIQUE,
            content TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    return connection


def list_documents():
    # 목록: 브라우저에 보일 파일명만 조회
    with connect() as connection:
        rows = connection.execute(
            "SELECT id, filename, created_at FROM documents ORDER BY id"
        ).fetchall()
    return [dict(row) for row in rows]


def all_document_texts():
    # 검색용: 파일명과 본문 전체
    with connect() as connection:
        rows = connection.execute(
            "SELECT filename, content FROM documents ORDER BY id"
        ).fetchall()
    return [dict(row) for row in rows]


def add_document(filename, content):
    # 저장: 사용자가 올린 TXT를 한 행으로 저장 (같은 이름이면 ValueError)
    with connect() as connection:
        found = connection.execute(
            "SELECT id FROM documents WHERE filename = ?", (filename,)
        ).fetchone()
        if found is not None:
            raise ValueError("duplicate")
        cursor = connection.execute(
            "INSERT INTO documents (filename, content) VALUES (?, ?)",
            (filename, content),
        )
        return cursor.lastrowid
