from Crypto.Util.number import bytes_to_long
from sage.all import *

flag = "Breach{[REDACTED]}"[7:-1]

def random_invertible_matrix_gf_p(m, p, a):
    """
    Generate a random invertible m x m matrix over GF(p) with entries in [0, a].
    """
    assert 0 <= a < p, "a must be in the range [0, p-1]"
    F = GF(p)
    while True:
        M = Matrix(F, m, m, [F(randint(0, a)) for _ in range(m * m)])
        if M.is_invertible():
            return M

def generate_matrices_with_det_below(num_matrices, m, p, a):
    """
    Generate 'num_matrices' random invertible matrices over GF(p) with entries in [0,a],
    ensuring that each matrix has a distinct determinant (as an integer) that is below 'bound'.
    """
    matrices = []
    while len(matrices) < num_matrices:
        M = random_invertible_matrix_gf_p(m, p, a)
        # Convert the determinant to an integer in [1, p-1]
        d = int(M.determinant())
        # Accept matrix only if d is below the bound and not already seen
        if d <p//2:
            matrices.append(M)
    return matrices

# ------------------------------
# Recommended parameters
# ------------------------------

num_matrices = 256
p = 2**553+549
a = 2        
m = 10      

matrix_array = generate_matrices_with_det_below(num_matrices, m, p, a)

mid = len(matrix_array) // 2
A1 = matrix_array[:mid]
A2 = matrix_array[mid:]

print("A1 = ", A1)
print("A2 = ", A2)

def encrypt_message(message, A1, A2):
    """
    Encrypts a binary message by selecting matrices from A1 for '0' and A2 for '1',
    and then multiplying them in order.
    
    Parameters:
      message -- a string of bits, e.g., "01100110"
      A1, A2 -- lists of matrices (the two partitions)
    
    Returns:
      The ciphertext matrix (the product of the selected matrices)
    """
    # Get the base field from the first matrix in A1.
    F = A1[0].base_ring()
    # Start with the identity matrix of appropriate size.
    C = identity_matrix(F, A1[0].nrows())
    
    for i,bit in enumerate(message):
        if bit == '0':
            # Select next matrix from A1.
            M = A1[i]
        elif bit == '1':
            # Select next matrix from A2.
            M = A2[i]
        else:
            raise ValueError("Message must be a binary string.")
        # Multiply into the ciphertext product.
        C = C * M
    return C

m = bin(bytes_to_long(flag.encode()))[2:]

C = encrypt_message(m, A1, A2)
print("C = ",C)
