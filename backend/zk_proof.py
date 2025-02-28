import hashlib

def generate_proof(data):
    """Generate a simple hash-based 'proof' of the input data."""
    return hashlib.sha256(data.encode()).hexdigest()

def verify_proof(new_proof, stored_proof):
    """
    For this demonstration, we simulate verification by checking if the
    hash difference is within a certain tolerance.
    """
    # For simplicity, we compare the strings directly.
    # In a real ZKP, you'd verify properties without revealing data.
    return new_proof == stored_proof
