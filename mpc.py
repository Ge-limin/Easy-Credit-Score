from mpyc.runtime import mpc


# With 3 parties:
#   python3 mpc.py -M3 -I0 --no-log
#   python3 mpc.py -M3 -I1 --no-log
#   python3 mpc.py -M3 -I2 --no-log
async def main():
    secint = mpc.SecInt(16)
    input('Please tell us who are you?\n')
    print('Please wait for other parties to join...')
    await mpc.start()
    print('All parties have joined')
    print('Please input the most recent one transaction that happened between you and the customer')
    """Asks about the most recent 3 transactions"""
    weighted_scores = []
    
    months_ago = int(input('How many months ago did this transaction happen? '))
    amount = int(input('Enter the amount of the transaction in dollars: '))

    month_weight = get_weight_by_months(months_ago)
    amount_weight = get_weight_by_amount(amount)

    weighted_score = int(month_weight * amount_weight * 100)
    weighted_scores.append(weighted_score)
    print(f"The approximate scores is: {weighted_score}")

    all_scores = mpc.input(secint(weighted_score))
    m = len(mpc.parties)
    sum_scores = sum(all_scores)

    print('Average score of recent transaction from all agencies is:', await mpc.output(sum_scores) / m)

    await mpc.shutdown()


def get_weight_by_months(months):
    weights = {
        0: 1.0,
        1: 0.9,
        2: 0.8,
        3: 0.7,
        4: 0.6,
        5: 0.5,
        6: 0.4,
        7: 0.3,
        8: 0.2,
        9: 0.1,
    }
    return weights.get(months, 0.0)


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


mpc.run(main())
