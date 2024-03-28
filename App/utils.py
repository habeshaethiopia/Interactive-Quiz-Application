from hashlib import sha256

def hash_password(password):
    # Hash password using SHA-256
    return sha256(password.encode()).hexdigest()

def format_date(date):
    # Format date in a specific way
    return date.strftime('%Y-%m-%d')

