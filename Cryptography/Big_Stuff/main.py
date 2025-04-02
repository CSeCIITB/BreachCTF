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
# Main parameters (adjust as needed)
# ------------------------------

num_matrices = 256       # Total number of matrices required (should be even for an equal split)
p = 2**553+549 # A prime; choose p large enough so that determinants can be below 'bound'
a = 2                  # Maximum matrix entry (0 <= entry <= a)
m = 10                  # Dimension of the square matrices (m x m)

# num_matrices = 256       # Total number of matrices required (should be even for an equal split)
# p = 2**553 + 549 # A prime; choose p large enough so that determinants can be below 'bound'
# a = 2                  # Maximum matrix entry (0 <= entry <= a)
# m = 10                  # Dimension of the square matrices (m x m)
            # All determinants will be strictly less than this value

# Generate the matrices with distinct determinants below the bound.
matrix_array = generate_matrices_with_det_below(num_matrices, m, p, a)

# Sort matrices in ascending order based on their determinants (converted to integers).
matrix_array.sort(key=lambda M: int(M.determinant()))

# Partition the sorted list into two halves: A1 (first half) and A2 (second half)
mid = len(matrix_array) // 2
A1 = matrix_array[:mid]
A2 = matrix_array[mid:]

# Print the sorted matrices and their determinants in each partition.
print("=== Partition A1 ===")
for i, M in enumerate(A1):
    print(f"A1 Matrix {i+1}:\n{M}\nDeterminant: {M.determinant()}\n")

print("=== Partition A2 ===")
for i, M in enumerate(A2):
    print(f"A2 Matrix {i+1}:\n{M}\nDeterminant: {M.determinant()}\n")


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
        T = C
        C = C * M
        assert C * M.inverse() == T, "reversibility check failed"
        print("Current matrix is ", C)
    return C

# Example usage:
# f is your binary message string, e.g.,
f = '01010101010111110011010001110010001100110101111101101101001101000011011101110010001100010111100001011111011001110011000001100100'

# A1 and A2 have been generated, sorted, and partitioned as in the previous script.
# For example, if A1 and A2 are defined as:
#   A1 = sorted_matrix_list[:mid]
#   A2 = sorted_matrix_list[mid:]
# then:

C = encrypt_message(f, A1, A2)
print("Ciphertext matrix C:")
print(C)

def matrix_leq(M1, M2):
    """
    Implements the entry-wise comparison for matrices over prime finite fields.
    M1 ≤ M2 if |M1[i,j]| ≤ |M2[i,j]| for all i,j where |x| is the integer
    representation of the field element in {0,...,p-1}.
    
    Parameters:
      M1, M2 -- matrices over the same prime finite field
      
    Returns:
      True if M1 ≤ M2 according to the entry-wise ordering, False otherwise
    """
    # Get dimensions
    n = M1.nrows()
    m = M1.ncols()
    
    # Check each entry
    for i in range(n):
        for j in range(m):
            # Convert field elements to integers in {0,...,p-1}
            val1 = int(M1[i,j])
            val2 = int(M2[i,j])
            
            if val1 > val2:
                return False
    
    return True

def decrypt_message(C, A1, A2):
    """
    Decrypts a ciphertext matrix C using the decomposition algorithm with
    proper entry-wise matrix comparison.
    
    Parameters:
      C -- the ciphertext matrix (product of matrices)
      A1, A2 -- lists of matrices for '0' and '1' bits respectively
    
    Returns:
      The decrypted binary message as a string
    """
    assert len(A1) == len(A2), "Lists A1 and A2 must have the same length"
    flag = ""
    
    for i in range(len(A1)):
        m1, m2 = A1[len(A1)-1-i], A2[len(A1)-1-i]
        
        # Compute inverses
        T1 = C * m1.inverse()
        T2 = C * m2.inverse()
        
        print(f"Step {i+1}:")
        print("Current C:", C)
        print("T1 (bit 0):", T1)
        print("T2 (bit 1):", T2)
        
        # Check using proper entry-wise comparison
        t1_leq_c = matrix_leq(T1, C)
        t2_leq_c = matrix_leq(T2, C)
        
        print(f"T1 ≤ C: {t1_leq_c}")
        print(f"T2 ≤ C: {t2_leq_c}")
        
        # Try the first condition: T1 ≤ C
        if t1_leq_c:
            C = T1
            flag += "0"
            print("Chose bit 0")
        # Try the second condition: T2 ≤ C
        elif t2_leq_c:
            C = T2
            flag += "1"
            print("Chose bit 1")
        else:
            # If neither condition holds, try the strict inequality
            t1_lt_c = matrix_lt(T1, C)
            t2_lt_c = matrix_lt(T2, C)
            
            print(f"T1 < C: {t1_lt_c}")
            print(f"T2 < C: {t2_lt_c}")
            
            if t1_lt_c:
                C = T1
                flag += "0"
                print("Chose bit 0 (strict)")
            elif t2_lt_c:
                C = T2
                flag += "1"
                print("Chose bit 1 (strict)")
            else:
                # If all else fails, try the alternative orientation
                c_leq_t1 = matrix_leq(C, T1)
                c_leq_t2 = matrix_leq(C, T2)
                
                print(f"C ≤ T1: {c_leq_t1}")
                print(f"C ≤ T2: {c_leq_t2}")
                
                if c_leq_t1:
                    C = T1
                    flag += "0"
                    print("Chose bit 0 (reverse)")
                elif c_leq_t2:
                    C = T2
                    flag += "1"
                    print("Chose bit 1 (reverse)")
                else:
                    # Last resort: check if T1 or T2 is very close to the identity matrix
                    # This might be useful for the last step
                    F = C.base_ring()
                    I = identity_matrix(F, C.nrows())
                    
                    if T1 == I:
                        C = T1
                        flag += "0"
                        print("Chose bit 0 (identity)")
                    elif T2 == I:
                        C = T2
                        flag += "1"
                        print("Chose bit 1 (identity)")
                    else:
                        raise ValueError(f"Decryption failed: no valid Matrix found. Current flag: {flag}")
    
    # Reverse the flag since we're working backwards
    flag = flag[::-1]
    print(f"Decrypted flag: {flag}")
    return flag

recovered_flag = decrypt_message(C, A1, A2)
print("Recovered flag:", recovered_flag)
