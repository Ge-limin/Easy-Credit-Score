import phe as paillier


def encrypt(original_data, some_args):
    """Each agency will call this function to encrypt the data before sending it to the MPC server"""
    paillier.generate_paillier_keypair(n_length=5)
    return