from mpyc.runtime import mpc
import phe 

async def get_agency_info(pub_key):
    sec_int = mpc.SecInt(16)
    avg_payment_score = -100
    avg_delay_score = -100

    # agency parties
    if mpc.pid != 0:
        input('What is your relationship with the user?\n')
        print('Please provide info about the most recent transaction between you and the user.')

    avg_payment_score = await cal_score(sec_int, "payment",pub_key)
    avg_delay_score = await cal_score(sec_int, "delay",pub_key)
    
    return avg_payment_score, avg_delay_score



# maps inputs to weights and produces final score for each agency, then aggregates for all w mean
async def cal_score(sec_int, transaction_type,pub_key):
    weighted_score = -100
    # agency party
    # request inputs from agencies about transactions of transaction_type: payment, delay
    if mpc.pid != 0:
        weighted_scores = []
        months_ago = int(input(f'How many months ago did last {transaction_type} happen?, If never, enter 100: '))
        amount = int(input(f'Enter the amount of the {transaction_type} in dollars: '))
        
        month_weight = get_weight_by_months(months_ago)
        amount_weight = get_weight_by_amount(amount)
        weighted_score = int(month_weight * amount_weight)
        print(f"The approximate scores of {transaction_type} is: {weighted_score}")
        
        weighted_score = pub_key.encrypt(weighted_score).ciphertext()
        print(weighted_score)
        weighted_scores.append(weighted_score)
        
    
    # collect encrypted scores forom all agencies, then take mean and output
    all_scores = mpc.input(sec_int(weighted_score), senders = [i for i in range(1,len(mpc.parties))])
    if not isinstance(all_scores, list):
        all_scores = [all_scores]
    # sum_scores = [phe.EncryptedNumber(pub_key, x) for x in all_scores]
    # sum_scores = sum(all_scores)
    avg_score = await mpc.output(all_scores)
    
    return avg_score


def get_weight_by_months(months):
    return 100 - months if months < 100 else 0


def get_weight_by_amount(amount):
    weights = {
        range(0, 100): 0.4,
        range(100, 500): 0.6,
        range(500, 1000): 0.7,
        range(1000, 5000): 0.8,
        range(5000, 999999): 1.0,
    }
    for amt_range, weight in weights.items():
        if amount in amt_range:
            return weight
    return 0.0
