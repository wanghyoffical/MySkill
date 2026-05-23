#!/usr/bin/env python3
"""Fetch GitHub repository activity and recent star/fork signals.

This script is intentionally small and dependency-free so a skill can run it
without extra setup. It treats recent stars and forks as confidence-graded signals:
exact when the scan crosses the requested cutoff, sampled when the page limit
is hit first, and unknown when the API cannot provide timestamps.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Iterable, List, Optional


GITHUB_API = "https://api.github.com"
DEFAULT_WINDOWS = [30, 90]


class GitHubApiError(RuntimeError):
    pass


def parse_github_time(value: str) -> dt.datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return dt.datetime.fromisoformat(value).astimezone(dt.timezone.utc)


def format_github_time(value: Optional[dt.datetime]) -> Optional[str]:
    if value is None:
        return None
    return value.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def summarize_recent_stars(
    pages: List[List[str]],
    windows: Iterable[int],
    as_of: dt.datetime,
    hit_scan_limit: bool,
) -> Dict[str, Any]:
    """Summarize starred_at timestamps from newest pages scanned backward."""

    return summarize_recent_events(
        pages=pages,
        windows=windows,
        as_of=as_of,
        hit_scan_limit=hit_scan_limit,
        latest_key="latest_starred_at",
        earliest_key="earliest_scanned_starred_at",
    )


def summarize_recent_forks(
    pages: List[List[str]],
    windows: Iterable[int],
    as_of: dt.datetime,
    hit_scan_limit: bool,
) -> Dict[str, Any]:
    """Summarize fork created_at timestamps from newest pages scanned forward."""

    return summarize_recent_events(
        pages=pages,
        windows=windows,
        as_of=as_of,
        hit_scan_limit=hit_scan_limit,
        latest_key="latest_fork_created_at",
        earliest_key="earliest_scanned_fork_created_at",
    )


def summarize_recent_events(
    pages: List[List[str]],
    windows: Iterable[int],
    as_of: dt.datetime,
    hit_scan_limit: bool,
    latest_key: str,
    earliest_key: str,
) -> Dict[str, Any]:
    """Summarize ISO timestamps from newest-to-oldest scanned pages.

    `pages` must be ordered newest page first. Each page may contain timestamps
    in any order; callers sort by timestamp before evaluating cutoffs.
    """

    as_of = as_of.astimezone(dt.timezone.utc)
    parsed_pages = [
        sorted(parse_github_time(starred_at) for starred_at in page) for page in pages
    ]
    all_stars = [starred_at for page in parsed_pages for starred_at in page]
    latest = max(all_stars) if all_stars else None
    earliest = min(all_stars) if all_stars else None

    window_results: Dict[str, Dict[str, Any]] = {}
    any_sampled = False

    for window in sorted(set(int(value) for value in windows)):
        cutoff = as_of - dt.timedelta(days=window)
        count = sum(1 for starred_at in all_stars if starred_at >= cutoff)

        crosses_cutoff = earliest is None or earliest < cutoff
        confidence = "sampled" if hit_scan_limit and not crosses_cutoff else "exact"
        is_lower_bound = confidence == "sampled"
        any_sampled = any_sampled or is_lower_bound

        window_results[str(window)] = {
            "days": window,
            "cutoff": format_github_time(cutoff),
            "count": count,
            "confidence": confidence,
            "is_lower_bound": is_lower_bound,
        }

    return {
        latest_key: format_github_time(latest),
        earliest_key: format_github_time(earliest),
        "overall_confidence": "sampled" if any_sampled else "exact",
        "windows": window_results,
    }


def parse_repo(value: str) -> str:
    value = value.strip()
    if value.startswith("https://github.com/"):
        value = value.removeprefix("https://github.com/")
    value = value.strip("/")
    parts = value.split("/")
    if len(parts) < 2 or not parts[0] or not parts[1]:
        raise argparse.ArgumentTypeError("repo must be OWNER/REPO or a GitHub URL")
    return "/".join(parts[:2])


def github_request(path_or_url: str, token: Optional[str], accept: str) -> Any:
    url = path_or_url
    if not url.startswith("https://"):
        url = f"{GITHUB_API}{path_or_url}"

    headers = {
        "Accept": accept,
        "User-Agent": "learning-project-scout",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
            return json.loads(body), dict(response.headers)
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise GitHubApiError(f"GitHub API {error.code} for {url}: {body}") from error
    except urllib.error.URLError as error:
        raise GitHubApiError(f"GitHub API request failed for {url}: {error}") from error


def read_gh_cli_token() -> Optional[str]:
    try:
        completed = subprocess.run(
            ["gh", "auth", "token"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        return None

    token = completed.stdout.strip()
    if completed.returncode != 0 or not token:
        return None
    return token


def resolve_token(args: argparse.Namespace) -> Dict[str, Optional[str]]:
    if args.token:
        return {"token": args.token, "source": "argument", "error": None}

    if args.token_source == "none":
        return {"token": None, "source": "none", "error": None}

    if args.token_source in ("auto", "env"):
        for env_name in ("GITHUB_TOKEN", "GH_TOKEN"):
            token = os.environ.get(env_name)
            if token:
                return {"token": token, "source": env_name, "error": None}

    if args.token_source in ("auto", "gh"):
        token = read_gh_cli_token()
        if token:
            return {"token": token, "source": "gh", "error": None}
        if args.token_source == "gh":
            return {
                "token": None,
                "source": "gh",
                "error": "GitHub CLI token unavailable. Run `gh auth login` first.",
            }

    return {"token": None, "source": "none", "error": None}


def fetch_auth_status(token: Optional[str], source: str) -> Dict[str, Any]:
    status: Dict[str, Any] = {
        "token_source": source,
        "authenticated": bool(token),
    }
    try:
        rate_limit, _headers = github_request(
            "/rate_limit",
            token=token,
            accept="application/vnd.github+json",
        )
        status["rate_limit"] = rate_limit.get("resources", {}).get("core")
    except GitHubApiError as error:
        status["rate_limit_error"] = str(error)

    if token:
        try:
            user, _headers = github_request(
                "/user",
                token=token,
                accept="application/vnd.github+json",
            )
            status["login"] = user.get("login")
        except GitHubApiError as error:
            status["user_error"] = str(error)
    return status


def fetch_repo_metadata(repo: str, token: Optional[str]) -> Dict[str, Any]:
    data, _headers = github_request(
        f"/repos/{repo}",
        token=token,
        accept="application/vnd.github+json",
    )
    return data


def fetch_stargazer_page(
    repo: str,
    page: int,
    per_page: int,
    token: Optional[str],
) -> List[str]:
    query = urllib.parse.urlencode({"per_page": per_page, "page": page})
    data, _headers = github_request(
        f"/repos/{repo}/stargazers?{query}",
        token=token,
        accept="application/vnd.github.star+json",
    )
    starred = []
    for item in data:
        starred_at = item.get("starred_at")
        if isinstance(starred_at, str):
            starred.append(starred_at)
    return starred


def fetch_fork_page(
    repo: str,
    page: int,
    per_page: int,
    token: Optional[str],
) -> List[str]:
    query = urllib.parse.urlencode(
        {"sort": "newest", "per_page": per_page, "page": page}
    )
    data, _headers = github_request(
        f"/repos/{repo}/forks?{query}",
        token=token,
        accept="application/vnd.github+json",
    )
    created = []
    for item in data:
        created_at = item.get("created_at")
        if isinstance(created_at, str):
            created.append(created_at)
    return created


def scan_recent_star_pages(
    repo: str,
    total_stars: int,
    windows: List[int],
    as_of: dt.datetime,
    max_pages: int,
    per_page: int,
    token: Optional[str],
) -> Dict[str, Any]:
    if total_stars <= 0:
        summary = summarize_recent_stars([], windows, as_of, hit_scan_limit=False)
        summary.update(
            {
                "pages_scanned": 0,
                "max_pages": max_pages,
                "per_page": per_page,
                "scan_direction": "newest_to_oldest",
            }
        )
        return summary

    last_page = max(1, math.ceil(total_stars / per_page))
    oldest_cutoff = as_of.astimezone(dt.timezone.utc) - dt.timedelta(days=max(windows))
    pages: List[List[str]] = []
    hit_scan_limit = False

    for index, page_number in enumerate(range(last_page, 0, -1), start=1):
        if index > max_pages:
            hit_scan_limit = True
            break

        page = fetch_stargazer_page(repo, page_number, per_page, token)
        pages.append(page)

        parsed = [parse_github_time(value) for value in page]
        if parsed and min(parsed) < oldest_cutoff:
            break

    summary = summarize_recent_stars(
        pages=pages,
        windows=windows,
        as_of=as_of,
        hit_scan_limit=hit_scan_limit,
    )
    summary.update(
        {
            "pages_scanned": len(pages),
            "last_page": last_page,
            "max_pages": max_pages,
            "per_page": per_page,
            "scan_direction": "newest_to_oldest",
        }
    )
    return summary


def scan_recent_fork_pages(
    repo: str,
    total_forks: int,
    windows: List[int],
    as_of: dt.datetime,
    max_pages: int,
    per_page: int,
    token: Optional[str],
) -> Dict[str, Any]:
    if total_forks <= 0:
        summary = summarize_recent_forks([], windows, as_of, hit_scan_limit=False)
        summary.update(
            {
                "pages_scanned": 0,
                "max_pages": max_pages,
                "per_page": per_page,
                "scan_direction": "newest_to_oldest",
            }
        )
        return summary

    last_page = max(1, math.ceil(total_forks / per_page))
    oldest_cutoff = as_of.astimezone(dt.timezone.utc) - dt.timedelta(days=max(windows))
    pages: List[List[str]] = []
    hit_scan_limit = False

    for page_number in range(1, last_page + 1):
        if page_number > max_pages:
            hit_scan_limit = True
            break

        page = fetch_fork_page(repo, page_number, per_page, token)
        if not page:
            break
        pages.append(page)

        parsed = [parse_github_time(value) for value in page]
        if parsed and min(parsed) < oldest_cutoff:
            break

    summary = summarize_recent_forks(
        pages=pages,
        windows=windows,
        as_of=as_of,
        hit_scan_limit=hit_scan_limit,
    )
    summary.update(
        {
            "pages_scanned": len(pages),
            "last_page": last_page,
            "max_pages": max_pages,
            "per_page": per_page,
            "scan_direction": "newest_to_oldest",
        }
    )
    return summary


def summarize_repo(
    repo: str,
    windows: List[int],
    max_star_pages: int,
    max_fork_pages: int,
    per_page: int,
    token: Optional[str],
    as_of: dt.datetime,
    include_stars: bool,
    include_forks: bool,
) -> Dict[str, Any]:
    metadata = fetch_repo_metadata(repo, token)
    license_info = metadata.get("license") or {}
    result: Dict[str, Any] = {
        "repo": metadata.get("full_name", repo),
        "html_url": metadata.get("html_url"),
        "description": metadata.get("description"),
        "language": metadata.get("language"),
        "size_kb": metadata.get("size"),
        "stars_total": metadata.get("stargazers_count", 0),
        "forks": metadata.get("forks_count", 0),
        "open_issues": metadata.get("open_issues_count", 0),
        "archived": metadata.get("archived"),
        "disabled": metadata.get("disabled"),
        "pushed_at": metadata.get("pushed_at"),
        "updated_at": metadata.get("updated_at"),
        "created_at": metadata.get("created_at"),
        "license": license_info.get("spdx_id") or license_info.get("key"),
        "topics": metadata.get("topics", []),
        "as_of": format_github_time(as_of),
    }

    if include_stars:
        try:
            result["recent_stars"] = scan_recent_star_pages(
                repo=repo,
                total_stars=int(result["stars_total"] or 0),
                windows=windows,
                as_of=as_of,
                max_pages=max_star_pages,
                per_page=per_page,
                token=token,
            )
        except GitHubApiError as error:
            result["recent_stars"] = unknown_recent_activity(windows, str(error))

    if include_forks:
        try:
            result["recent_forks"] = scan_recent_fork_pages(
                repo=repo,
                total_forks=int(result["forks"] or 0),
                windows=windows,
                as_of=as_of,
                max_pages=max_fork_pages,
                per_page=per_page,
                token=token,
            )
        except GitHubApiError as error:
            result["recent_forks"] = unknown_recent_activity(windows, str(error))

    return result


def unknown_recent_activity(windows: List[int], error: str) -> Dict[str, Any]:
    return {
        "overall_confidence": "unknown",
        "error": error,
        "windows": {
            str(window): {
                "days": window,
                "count": None,
                "confidence": "unknown",
                "is_lower_bound": False,
            }
            for window in windows
        },
    }


def summarize_repo_safe(
    repo: str,
    windows: List[int],
    max_star_pages: int,
    max_fork_pages: int,
    per_page: int,
    token: Optional[str],
    as_of: dt.datetime,
    include_stars: bool,
    include_forks: bool,
) -> Dict[str, Any]:
    try:
        return summarize_repo(
            repo=repo,
            windows=windows,
            max_star_pages=max_star_pages,
            max_fork_pages=max_fork_pages,
            per_page=per_page,
            token=token,
            as_of=as_of,
            include_stars=include_stars,
            include_forks=include_forks,
        )
    except GitHubApiError as error:
        result: Dict[str, Any] = {
            "repo": repo,
            "html_url": f"https://github.com/{repo}",
            "error": str(error),
            "as_of": format_github_time(as_of),
        }
        if include_stars:
            result["recent_stars"] = unknown_recent_activity(windows, str(error))
        if include_forks:
            result["recent_forks"] = unknown_recent_activity(windows, str(error))
        return result


def render_markdown(results: List[Dict[str, Any]]) -> str:
    lines = ["# GitHub 项目活跃度查询", ""]
    for item in results:
        lines.append(f"## {item['repo']}")
        lines.append(f"- 链接：{item.get('html_url')}")
        if item.get("error"):
            lines.append(f"- error：{item['error']}")
        lines.append(f"- 描述：{item.get('description') or ''}")
        lines.append(f"- 语言：{item.get('language') or 'unknown'}")
        lines.append(f"- 代码规模：{item.get('size_kb')} KB")
        lines.append(f"- stars：{item.get('stars_total')}")
        lines.append(f"- forks：{item.get('forks')}")
        lines.append(f"- open issues：{item.get('open_issues')}")
        lines.append(f"- license：{item.get('license') or 'unknown'}")
        lines.append(f"- pushed_at：{item.get('pushed_at')}")
        lines.append(f"- updated_at：{item.get('updated_at')}")

        recent = item.get("recent_stars")
        if recent:
            lines.append(
                f"- recent star confidence：{recent.get('overall_confidence')}"
            )
            for window, window_result in sorted(
                recent.get("windows", {}).items(), key=lambda pair: int(pair[0])
            ):
                count = window_result.get("count")
                prefix = ">=" if window_result.get("is_lower_bound") else ""
                lines.append(
                    f"- 最近 {window} 天 stars：{prefix}{count} "
                    f"({window_result.get('confidence')})"
                )
            if recent.get("error"):
                lines.append(f"- recent star error：{recent['error']}")
            else:
                lines.append(
                    f"- star 扫描：{recent.get('scan_direction')}, "
                    f"pages={recent.get('pages_scanned')}/{recent.get('max_pages')}, "
                    f"per_page={recent.get('per_page')}"
                )
        recent_forks = item.get("recent_forks")
        if recent_forks:
            lines.append(
                f"- recent fork confidence：{recent_forks.get('overall_confidence')}"
            )
            for window, window_result in sorted(
                recent_forks.get("windows", {}).items(), key=lambda pair: int(pair[0])
            ):
                count = window_result.get("count")
                prefix = ">=" if window_result.get("is_lower_bound") else ""
                lines.append(
                    f"- 最近 {window} 天 forks：{prefix}{count} "
                    f"({window_result.get('confidence')})"
                )
            if recent_forks.get("error"):
                lines.append(f"- recent fork error：{recent_forks['error']}")
            else:
                lines.append(
                    f"- fork 扫描：{recent_forks.get('scan_direction')}, "
                    f"pages={recent_forks.get('pages_scanned')}/{recent_forks.get('max_pages')}, "
                    f"per_page={recent_forks.get('per_page')}"
                )
        lines.append("")
    return "\n".join(lines)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Query GitHub repo activity and confidence-graded recent star/fork signals."
    )
    parser.add_argument(
        "--repo",
        action="append",
        type=parse_repo,
        help="GitHub repository as OWNER/REPO or https://github.com/OWNER/REPO. Repeatable.",
    )
    parser.add_argument(
        "--window",
        action="append",
        type=int,
        dest="windows",
        help="Recent activity window in days. Repeatable. Defaults to 30 and 90.",
    )
    parser.add_argument(
        "--max-star-pages",
        type=int,
        default=2,
        help="Maximum newest stargazer pages to scan per repo before marking sampled.",
    )
    parser.add_argument(
        "--max-fork-pages",
        type=int,
        default=2,
        help="Maximum newest fork pages to scan per repo before marking sampled.",
    )
    parser.add_argument(
        "--per-page",
        type=int,
        default=100,
        help="GitHub page size for stargazers and forks. Maximum is 100.",
    )
    parser.add_argument(
        "--as-of",
        help="UTC date or datetime for cutoff calculations, e.g. 2026-05-23.",
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="json",
        help="Output format.",
    )
    parser.add_argument(
        "--no-recent-stars",
        action="store_true",
        help="Only fetch repository metadata; skip stargazer timestamp scan.",
    )
    parser.add_argument(
        "--no-recent-forks",
        action="store_true",
        help="Only fetch repository metadata; skip fork created_at scan.",
    )
    parser.add_argument(
        "--token",
        help="GitHub token. Prefer GITHUB_TOKEN or GH_TOKEN env vars to avoid shell history.",
    )
    parser.add_argument(
        "--token-source",
        choices=["auto", "env", "gh", "none"],
        default="auto",
        help="Token lookup mode. auto uses --token, env vars, then `gh auth token`.",
    )
    parser.add_argument(
        "--auth-status",
        action="store_true",
        help="Print token source and GitHub rate-limit status, then exit.",
    )
    return parser.parse_args(argv)


def parse_as_of(value: Optional[str]) -> dt.datetime:
    if not value:
        return dt.datetime.now(dt.timezone.utc)
    if len(value) == 10:
        return dt.datetime.fromisoformat(value).replace(tzinfo=dt.timezone.utc)
    return parse_github_time(value)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    windows = sorted(set(args.windows or DEFAULT_WINDOWS))
    if any(window <= 0 for window in windows):
        print("--window values must be positive", file=sys.stderr)
        return 2
    if args.max_star_pages <= 0:
        print("--max-star-pages must be positive", file=sys.stderr)
        return 2
    if args.max_fork_pages <= 0:
        print("--max-fork-pages must be positive", file=sys.stderr)
        return 2
    if args.per_page <= 0 or args.per_page > 100:
        print("--per-page must be between 1 and 100", file=sys.stderr)
        return 2

    token_info = resolve_token(args)
    token = token_info["token"]
    if args.auth_status:
        status = fetch_auth_status(token, token_info["source"] or "none")
        if token_info.get("error"):
            status["token_error"] = token_info["error"]
        print(json.dumps(status, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    if not args.repo:
        print("--repo is required unless --auth-status is used", file=sys.stderr)
        return 2

    as_of = parse_as_of(args.as_of)
    results = [
        summarize_repo_safe(
            repo=repo,
            windows=windows,
            max_star_pages=args.max_star_pages,
            max_fork_pages=args.max_fork_pages,
            per_page=args.per_page,
            token=token,
            as_of=as_of,
            include_stars=not args.no_recent_stars,
            include_forks=not args.no_recent_forks,
        )
        for repo in args.repo
    ]

    if args.format == "markdown":
        print(render_markdown(results))
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
