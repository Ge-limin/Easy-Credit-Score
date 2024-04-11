# EasyCredit: Simplified Credit Scoring for Moderate Transactions
Introducing EasyCredit, a streamlined credit scoring system designed for moderate-sized transactions that don't require a comprehensive credit report. EasyCredit provides a machine-generated assessment of your financial reliability by securely analyzing your transaction history without disclosing sensitive details to your trading partners. This innovative system is perfect for situations where a transaction is significant enough to warrant an endorsement of your creditworthiness but doesn't necessitate a full credit check.

EasyCredit leverages technologies including Multi-Party Computation (MPC), Zero-Knowledge Proofs and neural networks to ensure the highest levels of security, privacy, and efficiency. By employing these advanced techniques, EasyCredit guarantees that your financial information remains confidential throughout the credit scoring process.

## Example Workflow:
User0 (the trading partner requesting an individual's trustworthiness) initiates the process by sending a request for an EasyCredit score and registering with the server to obtain a unique key.

User1 (the trading individual) provides basic demographic information, such as age, sex, and occupation, to the server.

User2 (Agency 1), User3 (Utility Company 2), and User4 (Decoration Company 3) each send their respective transaction histories in their own formats to the server.

User1's device employs Homomorphic Encryption to secure their data before sending it to the server.

Users 2, 3, and 4 utilize Multi-Party Computation (MPC) to protect their sensitive information.

The server runs a AI model to compute the EasyCredit score using the encrypted data provided by Users 1-4, ensuring that no sensitive information is revealed during the process.

The server generates a report containing the EasyCredit score, signs it with a digital signature, and encrypts it for secure transmission.

User0 receives the encrypted report and uses the server's public key to validate its authenticity. They then decrypt the report using their own unique key to access the EasyCredit score.

By utilizing EasyCredit, trading partners can quickly and securely assess an individual's financial reliability without compromising their privacy or requiring a full credit check. This streamlined system revolutionizes the way moderate-sized transactions are conducted, providing a trusted and efficient solution for both parties involved.

# How to use the model?
This repository contains a pre-trained model for predicting credit scores based on various features. The model classifies credit scores into three categories: 'Poor', 'Standard', and 'Good'.

Requirements

Python 3.x,
pandas,
numpy,
scikit-learn,
tensorflow

Usage

1. Clone the repository and navigate to the project directory.
   
2. Install the required dependencies:
   
`pip install pandas numpy scikit-learn tensorflow`

3. Load the pre-trained model:
   
`from tensorflow.keras.models import load_model

model = load_model("checkpoint.h5")`

4. Prepare the input data as a DataFrame or 2D NumPy array with the following features:

`'Age': integer or float
'Occupation': string
'Annual_Income': integer or float
'Monthly_Inhand_Salary': integer or float
'Num_Bank_Accounts': integer
'Num_Credit_Card': integer
'Interest_Rate': float
'Num_of_Loan': integer
'Delay_from_due_date': integer
'Num_of_Delayed_Payment': integer
'Changed_Credit_Limit': float
'Num_Credit_Inquiries': integer
'Credit_Mix': string
'Outstanding_Debt': integer or float
'Credit_Utilization_Ratio': float (between 0 and 1)
'Credit_History_Age': integer or float
'Payment_of_Min_Amount': string
'Total_EMI_per_month': integer or float
'Amount_invested_monthly': integer or float
'Monthly_Balance': integer or float`

5. Preprocess the input data:
Use the preprocess_data function to handle data types and extract numeric values.
Use the handle_outliers function to handle outliers.
Fill missing values in numeric features with the median.
Fill missing values in the 'Occupation' feature with the mode.

6. Select the same features used during training:
`useful_features = [
    'Age', 'Occupation', 'Annual_Income', 'Monthly_Inhand_Salary',
    'Num_Bank_Accounts', 'Num_Credit_Card', 'Interest_Rate', 'Num_of_Loan',
    'Delay_from_due_date', 'Num_of_Delayed_Payment',
    'Changed_Credit_Limit', 'Num_Credit_Inquiries', 'Credit_Mix',
    'Outstanding_Debt', 'Credit_Utilization_Ratio', 'Credit_History_Age',
    'Payment_of_Min_Amount', 'Total_EMI_per_month', 'Amount_invested_monthly',
    'Monthly_Balance'
]`

7.Transform the input data using the preprocessor object from the training script.

8.Make predictions using the loaded model:
`predictions = model.predict(new_data_transformed)
predicted_classes = np.argmax(predictions, axis=1)`
The model output will be probabilities for each class.
Use np.argmax to get the predicted class index:
0: 'Poor'
1: 'Standard'
2: 'Good'







