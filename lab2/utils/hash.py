def hash2hex(hash, mask=0xFFFFFFFFFFFFFFFF):
    return hex(hash & mask)

def get_hash_digest(obj):
    return hash2hex(hash(obj))
