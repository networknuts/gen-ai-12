import redis 

# SETUP THE REDIS CONNECTION
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

job_id = "e49dfff5-363c-49e5-888c-376cd8309633"
answer = redis_client.get(job_id)
print(answer)