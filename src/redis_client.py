import os
import redis
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD"),
    username="default",
    decode_responses=True
)


def get_transcript_from_redis(video_id: str) -> str | None:
    """
    Fetch transcript from Redis cache.
    """
    return redis_client.get(f"transcript:{video_id}")


def save_transcript_to_redis(
    video_id: str,
    text: str,
    ttl: int | None = 86400
):
    """
    Save transcript to Redis.
    Default TTL = 24 hours.
    Set ttl=None for permanent storage.
    """
    key = f"transcript:{video_id}"

    if ttl is None:
        redis_client.set(key, text)
    else:
        redis_client.setex(key, ttl, text)
