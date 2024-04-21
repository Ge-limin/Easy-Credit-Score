import ml


def generate(mpc_result):
    synthetic_data = generate_from_mpc_result(mpc_result)
    generate_from_agency(synthetic_data, None)
    return synthetic_data


def generate_from_agency(synthetic_data, agency_info):
    """use information from agencies to generate synthetic data that is compatible with the AI model"""
    synthetic_data['Age'] = agency_info['Age']
    synthetic_data['Occupation'] = agency_info['Occupation']
    synthetic_data['Annual_Income'] = agency_info['Annual_Income']
    synthetic_data['Monthly_Inhand_Salary'] = agency_info['Monthly_Inhand_Salary']
    synthetic_data['Num_Bank_Accounts'] = agency_info['Num_Bank_Accounts']
    synthetic_data['Num_Credit_Card'] = agency_info['Num_Credit_Card']
    synthetic_data['Interest_Rate'] = agency_info['Interest_Rate']
    synthetic_data['Num_of_Loan'] = agency_info['Num_of_Loan']


def generate_from_mpc_result(mpc_result):
    """use the result from the MPC computation to generate synthetic data that is compatible with the AI model"""
    # based on avg from the training data
    Credit_History_Age = "17 Years and 5 Months"

    # below are based on delay_score
    Delay_from_due_date = map_num(mpc_result['delay_score'], 0, 100,
                                  ml.delay_from_due_date_lower_bound, ml.delay_from_due_date_upper_bound)
    Num_of_Delayed_Payment = map_num(mpc_result['delay_score'], 0, 100,
                                     ml.num_delayed_payments_lower_bound, ml.num_delayed_payments_upper_bound)
    Changed_Credit_Limit = map_num(mpc_result['delay_score'], 0, 100, 30, -5)
    Num_Credit_Inquiries = map_num(mpc_result['delay_score'], 0, 100,
                                   ml.num_credit_inquiries_lower_bound, ml.num_credit_inquiries_upper_bound)
    Credit_Mix = map_from_num_to_str(mpc_result['delay_score'], 0, 100, ['Good','Standard','Bad'])
    Outstanding_Debt = map_num(mpc_result['delay_score'], 0, 100, 0, 5000)
    Credit_Utilization_Ratio = map_num(mpc_result['delay_score'], 0, 100,
                                       ml.credit_utilization_ratio_lower_bound, ml.credit_utilization_ratio_upper_bound)

    # below are based on payment_score
    Payment_of_Min_Amount = map_from_num_to_str(mpc_result['payment_score'], 0, 100,
                                    ["NO", "YES"])
    Total_EMI_per_month = map_num(mpc_result['payment_score'], 0, 100, 0, 2000)
    Amount_invested_monthly = map_num(mpc_result['payment_score'], 0, 100,0, 2000)
    Monthly_Balance = map_num(mpc_result['payment_score'], 0, 100, 0, 2000)
    return {
        'Delay_from_due_date': Delay_from_due_date,
        'Num_of_Delayed_Payment': Num_of_Delayed_Payment,
        'Changed_Credit_Limit': Changed_Credit_Limit,
        'Num_Credit_Inquiries': Num_Credit_Inquiries,
        'Credit_Mix': Credit_Mix,
        'Outstanding_Debt': Outstanding_Debt,
        'Credit_Utilization_Ratio': Credit_Utilization_Ratio,
        'Credit_History_Age': Credit_History_Age,
        'Payment_of_Min_Amount': Payment_of_Min_Amount,
        'Total_EMI_per_month': Total_EMI_per_month,
        'Amount_invested_monthly': Amount_invested_monthly,
        'Monthly_Balance': Monthly_Balance
    }


def map_num(original_num, min_num, max_num, min_target, max_target):
    return min_target + (max_target - min_target) * ((original_num - min_num) / (max_num - min_num))


def map_from_num_to_str(original_num, min_num, max_num, target_list):
    return target_list[int(map_num(original_num, min_num, max_num, 0, len(target_list)))]
