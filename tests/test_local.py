import os
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.config import Settings


class SettingsTests(unittest.TestCase):
    def test_defaults_are_consistent(self):
        s = Settings()
        self.assertEqual(s.embedding_model, "text-embedding-3-large")
        self.assertEqual(s.embedding_dimension, 3072)
        self.assertEqual(s.top_k, 5)
        self.assertEqual(s.max_support_retries, 2)
        self.assertEqual(s.max_retrieval_rewrites, 2)
        self.assertEqual(s.max_web_rewrites, 2)

    def test_database_file_resolves_relative_to_project(self):
        s = Settings(database_path="data/example.db")
        self.assertTrue(s.database_file.is_absolute())
        self.assertTrue(str(s.database_file).endswith("data/example.db"))


class DatabaseTests(unittest.TestCase):
    def test_init_save_and_read_audit(self):
        from src import db
        with tempfile.TemporaryDirectory() as td:
            fake = Settings(database_path=str(Path(td) / "audit.db"))
            with patch.object(db, "get_settings", return_value=fake):
                db.init_db()
                db.save_audit("Why is checkout failing?", {
                    "answer": "Check the runbook.",
                    "route": "Private Runbooks",
                    "used_web_search": False,
                    "support_status": "fully_supported",
                    "usefulness": "useful",
                    "trace": ["retrieved"],
                    "sources": [{"title": "checkout"}],
                })
                rows = db.latest_audits(10)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["question"], "Why is checkout failing?")
            self.assertEqual(rows[0]["used_web"], 0)
            self.assertEqual(rows[0]["support_status"], "fully_supported")


if __name__ == "__main__":
    unittest.main()
