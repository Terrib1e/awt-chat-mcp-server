"""
Web Tools for MCP Server

This module demonstrates network operations and how to handle:
1. HTTP requests and responses
2. Web scraping with HTML parsing
3. API interactions
4. Error handling for network operations
5. Rate limiting and security
"""

import asyncio
import json
import re
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin, urlparse
import aiohttp
import aiofiles
from bs4 import BeautifulSoup

from mcp.types import Tool

# Security and rate limiting
ALLOWED_DOMAINS = ['example.com', 'httpbin.org', 'jsonplaceholder.typicode.com']
MAX_RESPONSE_SIZE = 1024 * 1024  # 1MB
REQUEST_TIMEOUT = 30
MAX_CONCURRENT_REQUESTS = 5

# Rate limiting
REQUEST_SEMAPHORE = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

def _validate_url(url: str) -> str:
    """
    Validate URL for security.

    This function demonstrates:
    - URL validation
    - Security checks
    - Protocol validation
    - Domain whitelisting
    """
    try:
        parsed = urlparse(url)

        # Check protocol
        if parsed.scheme not in ['http', 'https']:
            raise ValueError("Only HTTP and HTTPS URLs are allowed")

        # Check domain (for security - in production, you might want to be more flexible)
        if not any(parsed.netloc.endswith(domain) for domain in ALLOWED_DOMAINS):
            # For demo purposes, we'll allow any domain but log it
            print(f"Warning: Accessing domain not in whitelist: {parsed.netloc}")

        return url

    except Exception as e:
        raise ValueError(f"Invalid URL: {str(e)}")

async def fetch_webpage(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fetch a webpage and return its content.

    This function demonstrates:
    - HTTP GET requests
    - Response handling
    - Content type detection
    - Error handling
    - Rate limiting
    """
    async with REQUEST_SEMAPHORE:
        try:
            url = args.get("url", "")
            if not url:
                raise ValueError("url is required")

            validated_url = _validate_url(url)
            include_html = args.get("include_html", False)
            extract_links = args.get("extract_links", False)

            headers = {
                'User-Agent': 'MCP-Server/1.0 (Educational Purpose)',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }

            timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)

            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(validated_url, headers=headers) as response:
                    # Check response size
                    content_length = response.headers.get('content-length')
                    if content_length and int(content_length) > MAX_RESPONSE_SIZE:
                        raise ValueError(f"Response too large: {content_length} bytes")

                    # Read content with size limit
                    content = await response.read()
                    if len(content) > MAX_RESPONSE_SIZE:
                        raise ValueError(f"Response too large: {len(content)} bytes")

                    # Decode content
                    text_content = content.decode('utf-8', errors='ignore')

                    # Parse HTML if requested
                    soup = BeautifulSoup(text_content, 'html.parser')

                    # Extract text content
                    text_only = soup.get_text(strip=True, separator=' ')

                    # Extract links if requested
                    links = []
                    if extract_links:
                        for link in soup.find_all('a', href=True):
                            absolute_url = urljoin(validated_url, link['href'])
                            links.append({
                                'text': link.get_text(strip=True),
                                'url': absolute_url,
                                'title': link.get('title', '')
                            })

                    # Extract metadata
                    title = soup.find('title')
                    title_text = title.get_text(strip=True) if title else ''

                    meta_description = soup.find('meta', attrs={'name': 'description'})
                    description = meta_description.get('content', '') if meta_description else ''

                    return {
                        "url": validated_url,
                        "status_code": response.status,
                        "content_type": response.headers.get('content-type', ''),
                        "title": title_text,
                        "description": description,
                        "text_content": text_only,
                        "html_content": text_content if include_html else None,
                        "links": links if extract_links else None,
                        "response_size": len(content),
                        "headers": dict(response.headers)
                    }

        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to fetch webpage: {str(e)}")

async def search_web(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform a web search (simulated using a search API).

    This function demonstrates:
    - API integration
    - Query parameter handling
    - Result processing
    - Pagination
    """
    try:
        query = args.get("query", "")
        if not query:
            raise ValueError("query is required")

        max_results = args.get("max_results", 10)
        language = args.get("language", "en")

        # This is a simplified simulation - in practice, you'd use a real search API
        # like Google Custom Search API, Bing Search API, etc.

        # For demo purposes, we'll search JSONPlaceholder API
        search_url = f"https://jsonplaceholder.typicode.com/posts"

        async with aiohttp.ClientSession() as session:
            async with session.get(search_url) as response:
                if response.status == 200:
                    posts = await response.json()

                    # Filter posts that match the query
                    matching_posts = []
                    for post in posts:
                        if query.lower() in post['title'].lower() or query.lower() in post['body'].lower():
                            matching_posts.append({
                                'title': post['title'],
                                'snippet': post['body'][:200] + '...' if len(post['body']) > 200 else post['body'],
                                'url': f"https://jsonplaceholder.typicode.com/posts/{post['id']}",
                                'id': post['id']
                            })

                    # Limit results
                    limited_results = matching_posts[:max_results]

                    return {
                        "query": query,
                        "language": language,
                        "max_results": max_results,
                        "total_found": len(matching_posts),
                        "results_returned": len(limited_results),
                        "results": limited_results,
                        "search_time": "simulated"
                    }
                else:
                    raise Exception(f"Search API returned status {response.status}")

    except Exception as e:
        raise Exception(f"Search failed: {str(e)}")

async def download_file(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Download a file from a URL.

    This function demonstrates:
    - File downloading
    - Progress tracking
    - Stream processing
    - File validation
    """
    async with REQUEST_SEMAPHORE:
        try:
            url = args.get("url", "")
            filename = args.get("filename", "")

            if not url:
                raise ValueError("url is required")

            validated_url = _validate_url(url)

            # If no filename provided, extract from URL
            if not filename:
                filename = urlparse(validated_url).path.split('/')[-1]
                if not filename:
                    filename = "downloaded_file"

            # Validate filename
            if '..' in filename or '/' in filename:
                raise ValueError("Invalid filename")

            timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)

            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(validated_url) as response:
                    if response.status != 200:
                        raise Exception(f"Download failed with status {response.status}")

                    # Check file size
                    content_length = response.headers.get('content-length')
                    if content_length and int(content_length) > MAX_RESPONSE_SIZE:
                        raise ValueError(f"File too large: {content_length} bytes")

                    # Download file
                    downloaded_size = 0
                    async with aiofiles.open(filename, 'wb') as file:
                        async for chunk in response.content.iter_chunked(8192):
                            await file.write(chunk)
                            downloaded_size += len(chunk)

                            if downloaded_size > MAX_RESPONSE_SIZE:
                                raise ValueError(f"File too large: {downloaded_size} bytes")

                    return {
                        "url": validated_url,
                        "filename": filename,
                        "size": downloaded_size,
                        "content_type": response.headers.get('content-type', ''),
                        "success": True
                    }

        except Exception as e:
            raise Exception(f"Download failed: {str(e)}")

def get_web_tools() -> List[Tool]:
    """
    Return all web tools with their schemas.

    This function demonstrates:
    - Network tool schemas
    - Optional parameters
    - Security considerations
    - API documentation
    """
    return [
        Tool(
            name="fetch_webpage",
            description="Fetch and parse a webpage",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL of the webpage to fetch"
                    },
                    "include_html": {
                        "type": "boolean",
                        "description": "Include raw HTML content in response",
                        "default": False
                    },
                    "extract_links": {
                        "type": "boolean",
                        "description": "Extract all links from the webpage",
                        "default": False
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="search_web",
            description="Search the web for information (simulated)",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 50
                    },
                    "language": {
                        "type": "string",
                        "description": "Language code for search results",
                        "default": "en"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="download_file",
            description="Download a file from a URL",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL of the file to download"
                    },
                    "filename": {
                        "type": "string",
                        "description": "Local filename to save as (optional)"
                    }
                },
                "required": ["url"]
            }
        )
    ]