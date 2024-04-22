import sys
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
import tensorflow as tf
import pickle
import joblib

if len(sys.argv) != 21:
    print("Please enter the right variables")
    print("Usage: python compute.py Age Occupation Annual_Income Monthly_Inhand_Salary Num_Bank_Accounts Num_Credit_Card Interest_Rate Num_of_Loan Delay_from_due_date Num_of_Delayed_Payment Changed_Credit_Limit Num_Credit_Inquiries Credit_Mix Outstanding_Debt Credit_Utilization_Ratio Credit_History_Age Payment_of_Min_Amount Total_EMI_per_month Amount_invested_monthly Monthly_Balance")
    sys.exit(1)

data = {
    'Age': float(sys.argv[1]),
    'Occupation': sys.argv[2],
    'Annual_Income': float(sys.argv[3]),
    'Monthly_Inhand_Salary': float(sys.argv[4]),
    'Num_Bank_Accounts': int(sys.argv[5]),
    'Num_Credit_Card': int(sys.argv[6]),
    'Interest_Rate': float(sys.argv[7]),
    'Num_of_Loan': int(sys.argv[8]),
    'Delay_from_due_date': int(sys.argv[9]),
    'Num_of_Delayed_Payment': int(sys.argv[10]),
    'Changed_Credit_Limit': float(sys.argv[11]),
    'Num_Credit_Inquiries': int(sys.argv[12]),
    'Credit_Mix': sys.argv[13],
    'Outstanding_Debt': float(sys.argv[14]),
    'Credit_Utilization_Ratio': float(sys.argv[15]),
    'Credit_History_Age': float(sys.argv[16]),
    'Payment_of_Min_Amount': sys.argv[17],
    'Total_EMI_per_month': float(sys.argv[18]),
    'Amount_invested_monthly': float(sys.argv[19]),
    'Monthly_Balance': float(sys.argv[20])
}

test_data = pd.DataFrame([data])


numeric_features = ['Age', 'Annual_Income', 'Monthly_Inhand_Salary', 'Num_Bank_Accounts', 'Num_Credit_Card', 'Interest_Rate', 'Num_of_Loan', 'Delay_from_due_date', 'Num_of_Delayed_Payment', 'Changed_Credit_Limit', 'Num_Credit_Inquiries', 'Outstanding_Debt', 'Credit_Utilization_Ratio', 'Credit_History_Age', 'Total_EMI_per_month', 'Amount_invested_monthly', 'Monthly_Balance']
categorical_features = ['Occupation', 'Credit_Mix', 'Payment_of_Min_Amount']


preprocessor = joblib.load('preprocessor.pkl')

scaler = preprocessor.transformers_[0][1]


with open('vocab.pkl', 'rb') as f:
    vocab = pickle.load(f)


encoder = OneHotEncoder(categories=vocab, handle_unknown='ignore')



dummy_data = pd.DataFrame({'Occupation': ['Teacher'], 'Credit_Mix': ['Standard'], 'Payment_of_Min_Amount': ['No']})
encoder.fit(dummy_data[categorical_features])

test_data_num = scaler.transform(test_data[numeric_features])
test_data_cat = encoder.transform(test_data[categorical_features]).toarray()

test_data_transformed = np.hstack((test_data_num, test_data_cat))

test_data_transformed[np.isnan(test_data_transformed)] = 0

test_data_transformed = test_data_transformed.reshape((1, test_data_transformed.shape[1], 1))

model = tf.keras.models.load_model('checkpoint.h5')

y_pred_prob = model.predict(test_data_transformed)
y_pred = np.argmax(y_pred_prob, axis=1)

credit_score_mapping = {0: 'Poor', 1: 'Standard', 2: 'Good'}
predicted_credit_score = credit_score_mapping[y_pred[0]]
print("Predicted credit classification:", predicted_credit_score)

