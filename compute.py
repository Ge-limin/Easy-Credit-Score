from mpyc.runtime import mpc


# With 3 parties:
#   python compute.py -M3 -I0 --no-log
async def main():
    sec_int = mpc.SecInt(16)
    print('Please wait for other parties to join...')
    await mpc.start()
    print('All parties have joined')
    print('Please input the most recent 3 transactions that happened between you and the customer')
    """Asks about the most recent 3 transactions"""
    weighted_scores = []
    for _ in range(3):
        months_ago = int(input('How many months ago did this transaction happen? '))
        amount = int(input('Enter the amount of the transaction in dollars: '))

        month_weight = get_weight_by_months(months_ago)
        amount_weight = get_weight_by_amount(amount)

        weighted_score = month_weight * amount_weight
        weighted_scores.append(weighted_score)

        print(f"The approximate scores is: {weighted_score}")

    for i, score in enumerate(weighted_scores):
        recent_transaction_products = mpc.input(sec_int(score))

        total_scores = sum(recent_transaction_products)
        max_score = mpc.max(recent_transaction_products)
        m = len(mpc.parties)

        print('Average score of recent transaction:', await mpc.output(total_scores) / m)
        print('Maximum score of recent transaction:', await mpc.output(max_score))

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
