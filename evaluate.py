import json
import numpy as np
import pandas as pd
import os
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from tensorflow.keras.models import load_model
import pickle
import joblib

def predict_credit_score(json_data):
    # data = json.loads(json_data)
    test_data = pd.DataFrame([json_data])

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

    model = load_model('checkpoint.h5')

    y_pred_prob = model.predict(test_data_transformed)
    y_pred = np.argmax(y_pred_prob, axis=1)

    credit_score_mapping = {0: 'Poor', 1: 'Standard', 2: 'Good'}
    predicted_credit_score = credit_score_mapping[y_pred[0]]
    return predicted_credit_score

json_data = {
    "Age": 25,
    "Occupation": "Teacher",
    "Annual_Income": 50000,
    "Monthly_Inhand_Salary": 4000,
    "Num_Bank_Accounts": 2,
    "Num_Credit_Card": 1,
    "Interest_Rate": 5.5,
    "Num_of_Loan": 1,
    "Delay_from_due_date": 0,
    "Num_of_Delayed_Payment": 0,
    "Changed_Credit_Limit": 1000,
    "Num_Credit_Inquiries": 1,
    "Credit_Mix": "Standard",
    "Outstanding_Debt": 5000,
    "Credit_Utilization_Ratio": 0.3,
    "Credit_History_Age": "17 Years and 5 Months",
    "Payment_of_Min_Amount": "No",
    "Total_EMI_per_month": 500,
    "Amount_invested_monthly": 1000,
    "Monthly_Balance": 3000
}


# predicted_credit_score = predict_credit_score(json_data)
# print("Predicted credit classification:", predicted_credit_score)