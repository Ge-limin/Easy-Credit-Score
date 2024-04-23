from mpyc.runtime import mpc
# from evaluate import predict_credit_score
from evaluate import predict_credit_score
from mpc import get_agency_info
# from synthetic import generate
import phe

from synthetic import generate


# With 2 parties:
#   python3 mpc.py -M2 -I0 --no-log
#   python3 mpc.py -M2 -I1 --no-log


async def main():
    """
    ideal workflow:
        1. Agencies call mpc.py to generate some aggregated statistics
        2. Agencies call homomorphic.py to encrypt the other data that the agency have
        3. Combining homomorphic encrypted data and the aggregated statistics to generate a row of data
        4. Run the AI model from ml.py to get a score from this row of data
        5. (optional) Agencies use pub/sec key to request and decrypt this final result
    demo workflow:
        1. Agencies call mpc.py to generate some aggregated statistics
        2. Agencies call homomorphic.py to encrypt the other data that the agency have
        3. Combining homomorphic encrypted data and the aggregated statistics, **call synthetic.py to MAP TO** a row of **SYNTHETIC** data
        4. Run the AI model from ml.py to get a score from this row of data
        5. **RETURN THE SCORE DIRECTLY**
    """
    sec_int = mpc.SecInt(16)
    print('Please wait for other parties to join...')
    await mpc.start()
    print('All parties have joined! Proceeding...')
    
   
    print("Welcome, user! Waiting for agencies to provide information...")

    pub_n = 0
    priv_key = None
    if mpc.pid == 0:
        pub_key, priv_key = phe.generate_paillier_keypair(n_length = 16)
        pub_n = pub_key.n
    
    pub_n = mpc.input(sec_int(pub_n), senders = 0)
    pub_n = await mpc.output(pub_n, receivers = [i for i in range(1,len(mpc.parties))])
    
    if pub_n: 
        pub_key = phe.PaillierPublicKey(pub_n)


  
    pay, delay = await get_agency_info(pub_key)

    if mpc.pid == 0:
        pay = priv_key.decrypt(phe.EncryptedNumber(pub_key, int(pay)))
        delay = priv_key.decrypt(phe.EncryptedNumber(pub_key, int(delay)))

        mpc_data  = {"payment_score": pay, "delay_score": delay}
        print("Calculating your credit risk now.")
        user_generated_data = generate(mpc_data)
        print(user_generated_data)
        result = predict_credit_score(user_generated_data)
        print("Your predicted credit risk is: ", result)
    else:
        print("Thank you for providing info for user!")



    await mpc.shutdown()

mpc.run(main())

