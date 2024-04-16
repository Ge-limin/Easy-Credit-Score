from mpyc.runtime import mpc
from get_factor import *
import sys

# With 3 parties:
#   python3 compute.py -M3 -I0 --no-log
#   python3 compute.py -M3 -I1 --no-log
#   python3 compute.py -M3 -I2 --no-log


async def main():
    secflt = mpc.SecFlt(16)

    await mpc.start()

    identity = input('Who are you? \
                         \nA: user \
                         \nB: rental agency \
                         \nC: utility company \
                         \nD: landlord reference\n')
    
    # TODO: ask for info
    # info = input('provide info')

    match identity:
        case 'A':
            # TODO: load json or csv and pass to model
            model_predicted_risk = compute_model_prediction([])
            factor = model_predicted_risk
        # TODO: figure out what info needed from rental/utility/landlord and how to compute
        case 'B':
            rental_score = compute_rental_score([])
            factor = rental_score
        case 'C':
            utility_score = compute_utility_score([])
            factor = utility_score
        case 'D':
            landlordref_score = compute_landlordref_score([])
            factor = landlordref_score
        case _:
            print("invalid identity")
            sys.exit(1)

    
    print(factor)
    mpc_info = mpc.input(secflt(factor))


    combine = sum(mpc_info)

    total_result = await mpc.output(combine)
    
    print("overall score: ", total_result)

    await mpc.shutdown()



mpc.run(main())