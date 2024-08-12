# Use the official Redis image as a parent image
FROM redis:latest

# Open port 6379 for external connections to Redis
EXPOSE 6379

CMD ["sh", "-c", "exec redis-server --requirepass \"$REDIS_PASSWORD\""]