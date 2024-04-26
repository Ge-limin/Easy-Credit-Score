from mpyc.runtime import mpc
from synthetic import generate
from evaluate import predict_credit_score
from mpc_calc import get_agency_info
import phe

# With 2 parties:
#   python3 demo.py -M2 -I0 --no-log
#   python3 demo.py -M2 -I1 --no-log


async def main():
    """
    ideal workflow:
        1. Agencies call get_agency_info() from mpc_calc.py to generate some aggregated statistics
        2. Agencies use public key from user to encrypt their data before aggregation
        3. User program combines homomorphic encrypted user data json and aggregated statistics
           to generate a row of data
        4. Run the AI model from ml.py to predict a credit risk assessment from this row of data
        5. (optional) User and requesting organization use pub/priv key to request and decrypt this final result
    demo workflow:
        1. Agencies call get_agency_info() from mpc_calc.py to generate some aggregated statistics
        2. Agencies use public key from user to encrypt their data before aggregation
        3. User program combines homomorphic encrypted user data json and aggregated statistics, 
           **call generate() in synthetic.py to MAP TO** a row of **SYNTHETIC** data
        4. Run the AI model from ml.py to predict a credit risk assessment from this row of data
        5. **RETURN THE RISK DIRECTLY**
    """
    print('Please wait for other parties to join...')
    await mpc.start()
    print('All parties have joined! Proceeding...')
    
    sec_int = mpc.SecInt(32)
    pub_n = 0
    priv_key = None
    pub_key = None

    # user party
    if mpc.pid == 0:
        print("Welcome, user! Waiting for agencies to provide information...")
        pub_key, priv_key = phe.generate_paillier_keypair(n_length = 16)
        pub_n = pub_key.n
    
    # transmit public key to all agencies
    pub_n = mpc.input(sec_int(pub_n), senders = 0)
    pub_n = await mpc.output(pub_n, receivers = [i for i in range(1,len(mpc.parties))])
    
    if pub_n: 
        pub_key = phe.PaillierPublicKey(pub_n)

    # each agency provides info to get aggregated pay and delay scores
    pays, delays = await get_agency_info(pub_key)

    # user party
    # decrypt aggregated statistics and use to produce user data for model, get prediction
    if mpc.pid == 0:
        m = len(mpc.parties) - 1
        pay = sum([phe.EncryptedNumber(pub_key, x) for x in pays])
        delay = sum([phe.EncryptedNumber(pub_key, x) for x in delays])
        pay = priv_key.decrypt(pay) / m
        delay = priv_key.decrypt(delay) / m

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

