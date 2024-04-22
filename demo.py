from mpyc.runtime import mpc

from mpc import cal_score, get_agency_info
from synthetic import generate
# from synthetic import generate

# With 3 parties:
#   python3 mpc.py -M3 -I0 --no-log
#   python3 mpc.py -M3 -I1 --no-log
#   python3 mpc.py -M3 -I2 --no-log


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
    secflt = mpc.SecFlt(16)
    sec_int = mpc.SecInt(16)

    print('Please wait for other parties to join...')
    await mpc.start()
    print('All parties have joined! Proceeding...')
    
    # print(mpc.pid)

    if mpc.pid == 0:
        print("Welcome, user! Waiting for agencies to provide information...")

    mpc_data = await get_agency_info()
    print(mpc_data)

    if mpc.pid == 0:
        print("Calculating your credit risk now.")
        user_generated_data = generate(mpc_data)
        print(user_generated_data)
        # TODO: load model and use data for prediction, print and return
    else:
        print("Thank you for providing info for user!")
    


    await mpc.shutdown()


mpc.run(main())

