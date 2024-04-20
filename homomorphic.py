

# todo
def encrypt(original_data, encryption_method):
    """Each agency will call this function to encrypt the data before sending it to the MPC server"""
    return encryption_method(original_data)