# Upstash AI Search Python Client

> [!NOTE]
> **This project is in GA Stage.**
>
> The Upstash Professional Support fully covers this project. It receives regular updates, and bug fixes.
> The Upstash team is committed to maintaining and improving its functionality.

It is a connectionless (HTTP based) AI Search client and designed for:

- Serverless functions (AWS Lambda ...)
- Cloudflare Workers
- Next.js, Jamstack ...
- Client side web/mobile applications
- WebAssembly
- and other environments where HTTP is preferred over TCP.

## Quick Start

### Install

#### Python

```bash
pip install upstash-search
```

### Create Database

Create a new database on [Upstash](https://console.upstash.com/search)

## Basic Usage:

```py
from upstash_search import Search

client = Search(
    url="<UPSTASH_SEARCH_REST_URL>",
    token="<UPSTASH_SEARCH_REST_TOKEN>",
)

# Access the index of a database
index = client.index("movies")

# Upsert documents into index
index.upsert(
    documents=[
        {
            "id": "movie-0",
            "content": {
                "title": "Star Wars",
                "overview": "Sci-fi space opera",
                "genre": "sci-fi",
                "category": "classic",
            },
            "metadata": {
                "poster": "https://poster.link/starwars.jpg",
            },
        },
        {
            "id": "movie-1",
            "content": {
                "title": "Inception",
                "overview": "Mind-bending thriller",
                "genre": "sci-fi",
                "category": "modern",
            },
            "metadata": {
                "poster": "https://poster.link/inception.jpg",
            },
        },
    ],
)

# Fetch documents by ids
documents = index.fetch(
    ids=["movie-0", "movie-1"],
)
print(documents)

# AI search
scores = index.search(
    query="space opera",
    limit=2,
)
print(scores)

# AI search with reranking
scores = index.search(
    query="space opera",
    limit=2,
    reranking=True,
)
print(scores)

# AI search with filtering
scores = index.search(
    query="space opera",
    limit=2,
    filter="category = 'classic'",
)
print(scores)

# Range over documents
range_documents = index.range(
    cursor="",
    limit=1,
)
print(range_documents.documents)

# Range over the next page of documents
range_documents = index.range(
    cursor=range_documents.next_cursor,
    limit=3,
)

# Delete a document by id
index.delete(
    ids=["movie-0"],
)

# Reset the index (delete all documents)
index.reset()

# Get database and index info
info = client.info()
print(info)
```
