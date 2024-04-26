from mpyc.runtime import mpc
from synthetic import generate
from evaluate import predict_credit_score
from mpc_calc import get_agency_info
import phe

# With 3 parties:
#   python3 demo.py -M3 -I0 --no-log -> user
#   python3 demo.py -M3 -I1 --no-log -> requesting org
#   python3 demo.py -M3 -I2 --no-log -> 2...N is for external agencies providing info

def get_scores(priv_key, pub_key, pays, delays):
    m = len(mpc.parties) - 1
    pay = sum([phe.EncryptedNumber(pub_key, x) for x in pays])
    delay = sum([phe.EncryptedNumber(pub_key, x) for x in delays])
    pay = priv_key.decrypt(pay) / m
    delay = priv_key.decrypt(delay) / m
    mpc_data  = {"payment_score": pay, "delay_score": delay}
    return mpc_data

def get_result(mpc_data):
    print("Calculating your credit risk now.")
    user_generated_data = generate(mpc_data)
    print(user_generated_data)
    result = predict_credit_score(user_generated_data)
    return result

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

    # organization party that requested credit risk assessment
    if mpc.pid == 1:
        print("Please wait for the credit risk assessment to be produced...")
        
       
    # transmit public key to all agencies
    pub_n = mpc.input(sec_int(pub_n), senders = 0)
    pub_n = await mpc.output(pub_n, receivers = [i for i in range(2,len(mpc.parties))])
    
    if pub_n: 
        pub_key = phe.PaillierPublicKey(pub_n)

    pays = [-1]
    delays = [-1]
    pays, delays = await get_agency_info(pub_key)

    # each agency provides info to get aggregated pay and delay scores
    result = -1
    if mpc.pid == 0:
        mpc_data = get_scores(priv_key, pub_key, pays, delays)
        result = get_result(mpc_data)

    result = mpc.input(sec_int(result), senders = 0)
    result = await mpc.output(result, receivers = [0, 1])
    credit_score_mapping = {0: 'Poor', 1: 'Good'}
    if result:
        result = credit_score_mapping[result]
    
    # user party
    # decrypt aggregated statistics and use to produce user data for model, get prediction
    if mpc.pid == 0:
        print("Your predicted credit risk is: ", result)
    elif mpc.pid == 1:
        print("The user's predicted credit risk is ", result)
    else:
        print("Thank you for providing info for user!")


    await mpc.shutdown()

mpc.run(main())


