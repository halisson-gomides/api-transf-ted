# src/cache.py
from cashews import cache

def setup_cache(settings):
    # Setup cache server
    cache.setup(settings.CACHE_SERVER_URL, 
                enable=True,
                suppress=False)
