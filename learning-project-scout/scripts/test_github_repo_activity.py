import datetime as dt
import os
import unittest
from unittest import mock

import github_repo_activity as activity


class RecentStarScanTests(unittest.TestCase):
    def test_counts_are_exact_when_scan_crosses_oldest_window(self):
        as_of = dt.datetime(2026, 5, 23, tzinfo=dt.timezone.utc)
        pages = [
            [
                "2026-05-22T10:00:00Z",
                "2026-04-20T10:00:00Z",
            ],
            [
                "2026-03-01T10:00:00Z",
                "2026-02-01T10:00:00Z",
            ],
        ]

        result = activity.summarize_recent_stars(
            pages=pages,
            windows=[30, 90],
            as_of=as_of,
            hit_scan_limit=False,
        )

        self.assertEqual(result["latest_starred_at"], "2026-05-22T10:00:00Z")
        self.assertEqual(result["earliest_scanned_starred_at"], "2026-02-01T10:00:00Z")
        self.assertEqual(result["windows"]["30"]["count"], 1)
        self.assertEqual(result["windows"]["30"]["confidence"], "exact")
        self.assertFalse(result["windows"]["30"]["is_lower_bound"])
        self.assertEqual(result["windows"]["90"]["count"], 3)
        self.assertEqual(result["windows"]["90"]["confidence"], "exact")
        self.assertEqual(result["overall_confidence"], "exact")

    def test_counts_are_sampled_when_scan_limit_hits_before_cutoff(self):
        as_of = dt.datetime(2026, 5, 23, tzinfo=dt.timezone.utc)
        pages = [
            [
                "2026-05-22T10:00:00Z",
                "2026-05-21T10:00:00Z",
            ],
            [
                "2026-05-20T10:00:00Z",
                "2026-05-19T10:00:00Z",
            ],
        ]

        result = activity.summarize_recent_stars(
            pages=pages,
            windows=[30, 90],
            as_of=as_of,
            hit_scan_limit=True,
        )

        self.assertEqual(result["windows"]["30"]["count"], 4)
        self.assertEqual(result["windows"]["30"]["confidence"], "sampled")
        self.assertTrue(result["windows"]["30"]["is_lower_bound"])
        self.assertEqual(result["windows"]["90"]["confidence"], "sampled")
        self.assertEqual(result["overall_confidence"], "sampled")

    def test_empty_pages_return_exact_zeroes(self):
        as_of = dt.datetime(2026, 5, 23, tzinfo=dt.timezone.utc)

        result = activity.summarize_recent_stars(
            pages=[],
            windows=[30, 90],
            as_of=as_of,
            hit_scan_limit=False,
        )

        self.assertIsNone(result["latest_starred_at"])
        self.assertEqual(result["windows"]["30"]["count"], 0)
        self.assertEqual(result["windows"]["30"]["confidence"], "exact")
        self.assertEqual(result["windows"]["90"]["count"], 0)
        self.assertEqual(result["overall_confidence"], "exact")

    def test_recent_forks_use_newest_first_scan_confidence(self):
        as_of = dt.datetime(2026, 5, 23, tzinfo=dt.timezone.utc)
        pages = [
            [
                "2026-05-22T10:00:00Z",
                "2026-05-21T10:00:00Z",
            ],
            [
                "2026-05-20T10:00:00Z",
                "2026-05-19T10:00:00Z",
            ],
        ]

        result = activity.summarize_recent_forks(
            pages=pages,
            windows=[30],
            as_of=as_of,
            hit_scan_limit=True,
        )

        self.assertEqual(result["latest_fork_created_at"], "2026-05-22T10:00:00Z")
        self.assertEqual(result["earliest_scanned_fork_created_at"], "2026-05-19T10:00:00Z")
        self.assertEqual(result["windows"]["30"]["count"], 4)
        self.assertEqual(result["windows"]["30"]["confidence"], "sampled")
        self.assertTrue(result["windows"]["30"]["is_lower_bound"])

    def test_repo_api_failure_returns_structured_unknown_result(self):
        as_of = dt.datetime(2026, 5, 23, tzinfo=dt.timezone.utc)

        with mock.patch.object(
            activity,
            "fetch_repo_metadata",
            side_effect=activity.GitHubApiError("rate limit exceeded"),
        ):
            result = activity.summarize_repo_safe(
                repo="owner/repo",
                windows=[30],
                max_star_pages=2,
                max_fork_pages=2,
                per_page=100,
                token=None,
                as_of=as_of,
                include_stars=True,
                include_forks=True,
            )

        self.assertEqual(result["repo"], "owner/repo")
        self.assertEqual(result["error"], "rate limit exceeded")
        self.assertEqual(result["recent_stars"]["overall_confidence"], "unknown")
        self.assertEqual(result["recent_stars"]["windows"]["30"]["confidence"], "unknown")
        self.assertEqual(result["recent_forks"]["overall_confidence"], "unknown")
        self.assertEqual(result["recent_forks"]["windows"]["30"]["confidence"], "unknown")


class TokenResolutionTests(unittest.TestCase):
    def test_explicit_token_wins_over_env_and_gh(self):
        args = mock.Mock(token="explicit-token", token_source="auto")

        with mock.patch.dict(os.environ, {"GITHUB_TOKEN": "env-token"}, clear=True):
            result = activity.resolve_token(args)

        self.assertEqual(result["token"], "explicit-token")
        self.assertEqual(result["source"], "argument")

    def test_env_token_is_used_before_gh_in_auto_mode(self):
        args = mock.Mock(token=None, token_source="auto")

        with mock.patch.dict(os.environ, {"GH_TOKEN": "env-token"}, clear=True):
            result = activity.resolve_token(args)

        self.assertEqual(result["token"], "env-token")
        self.assertEqual(result["source"], "GH_TOKEN")

    def test_auto_mode_can_use_github_cli_token(self):
        args = mock.Mock(token=None, token_source="auto")

        with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(
            activity, "read_gh_cli_token", return_value="gh-token"
        ):
            result = activity.resolve_token(args)

        self.assertEqual(result["token"], "gh-token")
        self.assertEqual(result["source"], "gh")

    def test_none_mode_disables_token_lookup(self):
        args = mock.Mock(token=None, token_source="none")

        with mock.patch.dict(os.environ, {"GITHUB_TOKEN": "env-token"}, clear=True):
            result = activity.resolve_token(args)

        self.assertIsNone(result["token"])
        self.assertEqual(result["source"], "none")


if __name__ == "__main__":
    unittest.main()
