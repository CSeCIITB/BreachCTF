from sage.all import *
from Crypto.Util.number import long_to_bytes

def matrix_lt(M1, M2):
    """
    Implements the entry-wise comparison for matrices over prime finite fields.
    M1 < M2 if |M1[i,j]| < |M2[i,j]| for all i,j where |x| is the integer
    representation of the field element in {0,...,p-1}.
    
    Parameters:
      M1, M2 -- matrices over the same prime finite field
      
    Returns:
      True if M1 < M2 according to the entry-wise ordering, False otherwise
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
            
            if val1 >= val2:
                return False
    
    return True

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
    
    for i in range(len(A1)-2):
        m1, m2 = A1[len(A1)-1-i], A2[len(A1)-1-i]
        
        # Compute inverses
        T1 = C * m1.inverse()
        T2 = C * m2.inverse()
        
        # Check using proper entry-wise comparison
        t1_leq_c = matrix_leq(T1, C)
        t2_leq_c = matrix_leq(T2, C)
        
        # Try the first condition: T1 ≤ C
        if t1_leq_c:
            C = T1
            flag += "0"
        # Try the second condition: T2 ≤ C
        elif t2_leq_c:
            C = T2
            flag += "1"
        else:
            # If neither condition holds, try the strict inequality
            t1_lt_c = matrix_lt(T1, C)
            t2_lt_c = matrix_lt(T2, C)
            
            if t1_lt_c:
                C = T1
                flag += "0"
            elif t2_lt_c:
                C = T2
                flag += "1"
            else:
                # If all else fails, try the alternative orientation
                c_leq_t1 = matrix_leq(C, T1)
                c_leq_t2 = matrix_leq(C, T2)
                
                if c_leq_t1:
                    C = T1
                    flag += "0"
                elif c_leq_t2:
                    C = T2
                    flag += "1"
                else:
                    # Last resort: check if T1 or T2 is very close to the identity matrix
                    # This might be useful for the last step
                    F = C.base_ring()
                    I = identity_matrix(F, C.nrows())
                    
                    if T1 == I:
                        C = T1
                        flag += "0"
                    elif T2 == I:
                        C = T2
                        flag += "1"
                    else:
                        raise ValueError(f"Decryption failed: no valid Matrix found. Current flag: {flag}")
    
    # Reverse the flag since we're working backwards
    flag = flag[::-1]
    return flag

# by observation, flag has msb 1
recovered_flag ='1' + decrypt_message(C, A1, A2)
print("Recovered flag:", "Breach{"+long_to_bytes(int(recovered_flag,2)).decode()+'}')
