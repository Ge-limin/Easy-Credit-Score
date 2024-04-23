from mpyc.runtime import mpc


# With 3 parties:
#   python3 mpc.py -M3 -I0 --no-log
#   python3 mpc.py -M3 -I1 --no-log
#   python3 mpc.py -M3 -I2 --no-log

async def get_agency_info():
    sec_int = mpc.SecInt(16)
    avg_payment_score = -100
    avg_delay_score = -100

    if mpc.pid != 0:
        print('Please provide info about the most recent transaction between you and the user.')

    avg_payment_score = await cal_score(sec_int, "payment")
    avg_delay_score = await cal_score(sec_int, "delay")
    
    
    return {"payment_score": avg_payment_score, "delay_score": avg_delay_score}


async def cal_score(sec_int, transaction_type):
    weighted_score = -100
    if mpc.pid != 0:
        weighted_scores = []
        months_ago = int(input(f'How many months ago did last {transaction_type} happen?, If never, enter 100: '))
        amount = int(input(f'Enter the amount of the {transaction_type} in dollars: '))
        
        month_weight = get_weight_by_months(months_ago)
        amount_weight = get_weight_by_amount(amount)
        weighted_score = int(month_weight * amount_weight)
        # TODO: add phe encryption
        # weighted_score = phe_pub_key.encrypt(weighted_score)
        weighted_scores.append(weighted_score)
        print(f"The approximate scores of {transaction_type} is: {weighted_score}")
    
    all_scores = mpc.input(sec_int(weighted_score), senders = 1)
    if not isinstance(all_scores, list):
        all_scores = [all_scores]
    m = len(mpc.parties) - 1
    sum_scores = sum(all_scores)
    avg_score = await mpc.output(sum_scores) / m
    
    print(f'Average score of recent {transaction_type} from all agencies is: {avg_score}')
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


# print(mpc.run(execute()))
