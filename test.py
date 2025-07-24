from upstash_search import Search

client = Search()

index = client.index("what")

info = index.fetch("what")
