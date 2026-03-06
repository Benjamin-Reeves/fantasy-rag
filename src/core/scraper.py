from __future__ import annotations

import re
from collections import deque
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urldefrag, urljoin, urlparse

import requests
from bs4 import BeautifulSoup


@dataclass
class ScrapedPage:
    source_url: str
    canonical_url: str
    title: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


class WebsiteScraper:
    """Scrape and extract blog-style content from web pages using BeautifulSoup."""

    _DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        )
    }

    _BLOCKED_SUFFIXES = {
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".svg",
        ".webp",
        ".zip",
        ".rar",
        ".mp4",
        ".mp3",
        ".css",
        ".js",
        ".ico",
    }

    _BLOG_HINTS = ("blog", "post", "article", "news", "insights")

    def __init__(self, timeout_seconds: int = 20, headers: dict[str, str] | None = None):
        self.timeout_seconds = timeout_seconds
        self.session = requests.Session()
        merged_headers = dict(self._DEFAULT_HEADERS)
        if headers:
            merged_headers.update(headers)
        self.session.headers.update(merged_headers)

    def scrape_page(self, url: str) -> ScrapedPage | None:
        """Scrape a single URL and return extracted page content."""
        normalized_url = self._normalize_url(url, url)
        if not normalized_url:
            return None

        html = self._fetch_html(normalized_url)
        if not html:
            return None

        soup = BeautifulSoup(html, "html.parser")
        return self._extract_page(normalized_url, soup)

    def scrape_site(self, start_url: str, max_pages: int = 10, follow_links: bool = True) -> list[ScrapedPage]:
        """Breadth-first scrape of a site, focused on likely blog/article pages."""
        normalized_start = self._normalize_url(start_url, start_url)
        if not normalized_start:
            return []

        allowed_domain = urlparse(normalized_start).netloc
        queue: deque[str] = deque([normalized_start])
        visited: set[str] = set()
        pages: list[ScrapedPage] = []

        while queue and len(pages) < max_pages:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)

            html = self._fetch_html(current)
            if not html:
                continue

            soup = BeautifulSoup(html, "html.parser")
            page = self._extract_page(current, soup)
            if page:
                pages.append(page)

            if not follow_links:
                continue

            links = self._extract_internal_links(
                base_url=current,
                soup=soup,
                allowed_domain=allowed_domain,
            )
            for link in links:
                if link not in visited:
                    queue.append(link)

        return pages

    def _fetch_html(self, url: str) -> str:
        try:
            response = self.session.get(url, timeout=self.timeout_seconds)
            response.raise_for_status()
            return response.text
        except requests.RequestException as exc:
            print(f"Error fetching content from {url}: {exc}")
            return ""

    def _extract_page(self, url: str, soup: BeautifulSoup) -> ScrapedPage | None:
        canonical_url = self._extract_canonical_url(url, soup)
        title = self._extract_title(soup)
        metadata = self._extract_metadata(soup)
        content = self._extract_main_content(soup)

        if len(content) < 150:
            return None

        return ScrapedPage(
            source_url=url,
            canonical_url=canonical_url,
            title=title,
            content=content,
            metadata=metadata,
        )

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        for tag in soup(["script", "style", "noscript", "svg", "iframe"]):
            tag.decompose()
        for tag in soup(["nav", "footer", "header", "aside", "form"]):
            tag.decompose()

        candidates: list[str] = []
        selectors = (
            "article",
            "main",
            "[role='main']",
            ".post-content",
            ".entry-content",
            ".article-content",
            ".blog-post",
            ".post",
            ".content",
        )

        for selector in selectors:
            for node in soup.select(selector):
                text = node.get_text("\n", strip=True)
                cleaned = self._clean_text(text)
                if len(cleaned) >= 150:
                    candidates.append(cleaned)

        if candidates:
            return max(candidates, key=len)

        body = soup.body or soup
        return self._clean_text(body.get_text("\n", strip=True))

    def _extract_title(self, soup: BeautifulSoup) -> str:
        og_title = soup.find("meta", attrs={"property": "og:title"})
        if og_title and og_title.get("content"):
            return og_title["content"].strip()

        if soup.title and soup.title.string:
            return soup.title.string.strip()

        h1 = soup.find("h1")
        return h1.get_text(strip=True) if h1 else "Untitled"

    def _extract_metadata(self, soup: BeautifulSoup) -> dict[str, Any]:
        metadata: dict[str, Any] = {}

        description = soup.find("meta", attrs={"name": "description"})
        if description and description.get("content"):
            metadata["description"] = description["content"].strip()

        author = soup.find("meta", attrs={"name": "author"})
        if author and author.get("content"):
            metadata["author"] = author["content"].strip()

        published = soup.find("meta", attrs={"property": "article:published_time"})
        if published and published.get("content"):
            metadata["published_time"] = published["content"].strip()

        return metadata

    def _extract_canonical_url(self, fallback_url: str, soup: BeautifulSoup) -> str:
        canonical_link = soup.find("link", rel="canonical")
        if canonical_link and canonical_link.get("href"):
            normalized = self._normalize_url(fallback_url, canonical_link["href"])
            if normalized:
                return normalized
        return fallback_url

    def _extract_internal_links(self, base_url: str, soup: BeautifulSoup, allowed_domain: str) -> list[str]:
        links: list[str] = []

        for anchor in soup.find_all("a", href=True):
            normalized = self._normalize_url(base_url, anchor["href"])
            if not normalized:
                continue

            parsed = urlparse(normalized)
            if parsed.netloc != allowed_domain:
                continue

            if any(parsed.path.lower().endswith(suffix) for suffix in self._BLOCKED_SUFFIXES):
                continue

            path_lower = parsed.path.lower()
            if not path_lower or path_lower == "/":
                continue

            # Favor links that look like articles/blog posts to avoid crawling entire sites.
            if not any(hint in path_lower for hint in self._BLOG_HINTS):
                continue

            links.append(normalized)

        return links

    @staticmethod
    def _normalize_url(base_url: str, href: str) -> str:
        if not href:
            return ""

        absolute = urljoin(base_url, href)
        absolute, _ = urldefrag(absolute)
        parsed = urlparse(absolute)

        if parsed.scheme not in {"http", "https"}:
            return ""

        path = parsed.path or "/"
        normalized = f"{parsed.scheme}://{parsed.netloc}{path}"
        return normalized.rstrip("/") if path != "/" else normalized

    @staticmethod
    def _clean_text(text: str) -> str:
        text = text.replace("\xa0", " ")
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r" ?\n ?", "\n", text)
        return text.strip()
