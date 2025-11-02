from django.core.cache import cache
from .models import Property

from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    # Try to get queryset from Redis cache
    properties = cache.get('all_properties')

    if properties is None:
        # Cache miss → Fetch from DB
        properties = list(
            Property.objects.all().values(
                "id", "title", "description", "price", "location", "created_at"
            )
        )

        # Store in Redis for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)

    return properties



def get_redis_cache_metrics():
    """
    Retrieves Redis cache hit/miss metrics and calculates hit ratio.
    Returns a dictionary with hits, misses, and hit ratio.
    """
    try:
        redis_conn = get_redis_connection("default")  # connect to Redis used by Django
        info = redis_conn.info()

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)

        total = hits + misses
        hit_ratio = (hits / total) if total > 0 else 0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": round(hit_ratio, 3)
        }

        logger.info(f"Redis Metrics: Hits={hits}, Misses={misses}, Hit Ratio={hit_ratio}")

        return metrics

    except Exception as e:
        logger.error(f"Error retrieving Redis metrics: {e}")
        return {"error": str(e)}
