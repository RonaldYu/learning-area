import redis
from redis.exceptions import RedisError
import time
from urllib.parse import quote_plus


def main():
    # Create a connection pool
    password = quote_plus('XXXX')
    host = quote_plus('ryredis.redis.cache.windows.net')
    port = quote_plus('6380')
    db_indx =quote_plus('0')
    pool = redis.ConnectionPool.from_url(
        f'rediss://:{password}@{host}:{port}/{db_indx}',
        decode_responses=True,  # Automatically decode responses to strings
        max_connections=10      # Maximum number of connections in the pool
    )

    try:
        # Create a Redis client using the connection pool
        redis_client = redis.Redis(connection_pool=pool)

        # Example 1: Basic string operations
        print("Example 1: String operations")
        redis_client.set('my_key', 'Hello Redis!')
        value = redis_client.get('my_key')
        print(f"Retrieved value: {value}")

        # Example 2: List operations with TTL
        print("\nExample 2: List operations with TTL")
        redis_client.lpush('my_list', 'item1', 'item2', 'item3')
        redis_client.expire('my_list', 10)  # Set TTL to 10 seconds
        list_items = redis_client.lrange('my_list', 0, -1)
        list_ttl = redis_client.ttl('my_list')
        print(f"List items: {list_items}")
        print(f"List TTL: {list_ttl} seconds")
        time.sleep(11)
        list_items = redis_client.lrange('my_list', 0, -1)
        print(f"List items after 11 seconds: {list_items}")
        

        # Example 3: Hash operations with TTL
        print("\nExample 3: Hash operations with TTL")
        redis_client.hset('my_hash', mapping={
            'field1': 'value1',
            'field2': 'value2'
        })
        redis_client.expire('my_hash', 10)  # Set TTL to 10 seconds
        hash_data = redis_client.hgetall('my_hash')
        hash_ttl = redis_client.ttl('my_hash')
        print(f"Hash data: {hash_data}")
        print(f"Hash TTL: {hash_ttl} seconds")
        time.sleep(11)
        hash_data = redis_client.hgetall('my_hash')
        print(f"Hash data after 11 seconds: {hash_data}")

        # Example 4: Set operations with TTL
        print("\nExample 4: Set operations with TTL")
        redis_client.sadd('my_set', 'member1', 'member2', 'member3')
        redis_client.expire('my_set', 10)  # Set TTL to 10 seconds
        set_members = redis_client.smembers('my_set')
        set_ttl = redis_client.ttl('my_set')
        print(f"Set members: {set_members}")
        print(f"Set TTL: {set_ttl} seconds")
        time.sleep(11)
        set_members = redis_client.smembers('my_set')
        print(f"Set members after 11 seconds: {set_members}")

        # Wait to see the expiration
        print("\nWaiting 11 seconds to see expiration...")
        time.sleep(11)

        # Check if keys still exist
        print("\nChecking keys after expiration:")
        print(f"List exists: {redis_client.exists('my_list')}")
        print(f"Hash exists: {redis_client.exists('my_hash')}")
        print(f"Set exists: {redis_client.exists('my_set')}")

        # Example 5: Key expiration
        print("\nExample 5: Key expiration")
        redis_client.setex('expiring_key', 10, 'This will expire in 10 seconds')
        ttl = redis_client.ttl('expiring_key')
        print(f"Time to live: {ttl} seconds")
        value = redis_client.get('expiring_key')
        print(f"Value : {value}")
        time.sleep(11)
        value = redis_client.get('expiring_key')
        print(f"Value after 11 seconds: {value}")
        
    except RedisError as e:
        print(f"Redis error occurred: {e}")
    finally:
        # Clean up
        redis_client.close()

if __name__ == "__main__":
    main() 