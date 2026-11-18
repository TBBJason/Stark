import unittest
from datetime import date

from normalize_data import normalize_movie

class NormalizeMovieTests(unittest.TestCase):
    def test_normalizes_a_complete_movie(self) -> None:
        raw_movie = {
            "id": 12345,
            "title": "Example Movie",
            "release_date": "2026-04-12",
            "overview": "An example overview.",
        }

        result = normalize_movie(raw_movie)

        self.assertEqual(result["tmdb_id"], 12345)
        self.assertEqual(result["title"], "Example Movie")
        self.assertEqual(
            result["release_date"],
            date(2026, 4, 12),
        )
        self.assertEqual(
            result["overview"],
            "An example overview.",
        )

    def test_converts_empty_optional_fields_to_none(self) -> None:
        raw_movie = {
            "id": 12345,
            "title": "Example Movie",
            "release_date": "",
            "overview": "",
        }

        result = normalize_movie(raw_movie)

        self.assertIsNone(result["release_date"])
        self.assertIsNone(result["overview"])

    def test_rejects_an_invalid_release_date(self) -> None:
        raw_movie = {
            "id": 12345,
            "title": "Example Movie",
            "release_date": "not-a-date",
            "overview": "An example overview.",
        }

        with self.assertRaises(ValueError):
            normalize_movie(raw_movie)

    def test_rejects_a_movie_without_an_id(self) -> None:
        raw_movie = {
            "title": "Example Movie",
            "release_date": "2026-04-12",
            "overview": "An example overview.",
        }

        with self.assertRaises(KeyError):
            normalize_movie(raw_movie)

if __name__ == "__main__":
    unittest.main()
