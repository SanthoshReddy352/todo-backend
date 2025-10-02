import secrets

# Generate a URL-safe text string, containing 32 random bytes
random_string = secrets.token_urlsafe(32)

print(random_string)