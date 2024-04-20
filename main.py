import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.utils.class_weight import compute_class_weight
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import numpy as np

# read train file and test file
train_file_path = 'train1_utf8.csv'
# test_file_path = '/Users/jingxinshi/Desktop/eps/test.csv'

df = pd.read_csv(train_file_path)
# test_df = pd.read_csv(test_file_path)

# define boundary
age_lower_bound, age_upper_bound = 18, 100
annual_income_lower_bound, annual_income_upper_bound = 10000, 1000000
monthly_salary_lower_bound, monthly_salary_upper_bound = 500, 100000
num_bank_accounts_lower_bound, num_bank_accounts_upper_bound = 0, 10
num_credit_cards_lower_bound, num_credit_cards_upper_bound = 0, 10
interest_rate_lower_bound, interest_rate_upper_bound = 0, 50
num_loans_lower_bound, num_loans_upper_bound = 0, 10
delay_from_due_date_lower_bound, delay_from_due_date_upper_bound = 0, 180
num_delayed_payments_lower_bound, num_delayed_payments_upper_bound = 0, 50
changed_credit_limit_lower_bound, changed_credit_limit_upper_bound = -100, 100
num_credit_inquiries_lower_bound, num_credit_inquiries_upper_bound = 0, 20
credit_utilization_ratio_lower_bound, credit_utilization_ratio_upper_bound = 0, 1
total_emi_lower_bound, total_emi_upper_bound = 0, 100000
amount_invested_monthly_lower_bound, amount_invested_monthly_upper_bound = 0, 100000
monthly_balance_lower_bound, monthly_balance_upper_bound = -100000, 1000000


def preprocess_data(df):
    df['Credit_History_Age'] = df['Credit_History_Age'].str.extract('(\d+)').astype(float)

    df['Age'] = pd.to_numeric(df['Age'], errors='coerce')

    df['Annual_Income'] = pd.to_numeric(df['Annual_Income'].str.replace(',', '').str.replace('_', ''), errors='coerce')

    df['Monthly_Inhand_Salary'] = pd.to_numeric(df['Monthly_Inhand_Salary'], errors='coerce')

    df['Num_of_Loan'] = pd.to_numeric(df['Num_of_Loan'], errors='coerce')

    df['Delay_from_due_date'] = pd.to_numeric(df['Delay_from_due_date'], errors='coerce')

    df['Changed_Credit_Limit'] = pd.to_numeric(
        df['Changed_Credit_Limit'].str.extract('([-+]?\d*\.\d+|\d+)', expand=False), errors='coerce')

    df['Num_of_Delayed_Payment'] = pd.to_numeric(df['Num_of_Delayed_Payment'], errors='coerce')

    df['Num_Credit_Inquiries'] = pd.to_numeric(df['Num_Credit_Inquiries'], errors='coerce')

    df['Credit_Utilization_Ratio'] = pd.to_numeric(df['Credit_Utilization_Ratio'], errors='coerce')

    df['Total_EMI_per_month'] = pd.to_numeric(df['Total_EMI_per_month'], errors='coerce')

    df['Outstanding_Debt'] = pd.to_numeric(df['Outstanding_Debt'].str.extract('([-+]?\d*\.\d+|\d+)', expand=False),
                                           errors='coerce')

    df['Amount_invested_monthly'] = pd.to_numeric(
        df['Amount_invested_monthly'].str.extract('([-+]?\d*\.\d+|\d+)', expand=False), errors='coerce')

    df['Monthly_Balance'] = pd.to_numeric(df['Monthly_Balance'].str.extract('([-+]?\d*\.\d+|\d+)', expand=False),
                                          errors='coerce')

    return df


df = preprocess_data(df)


def handle_outliers(df):
    df['Age'] = np.where(df['Age'] > age_upper_bound, np.nan, df['Age'])
    df['Age'] = np.where(df['Age'] < age_lower_bound, np.nan, df['Age'])

    df['Annual_Income'] = np.where(df['Annual_Income'] > annual_income_upper_bound, np.nan, df['Annual_Income'])
    df['Annual_Income'] = np.where(df['Annual_Income'] < annual_income_lower_bound, np.nan, df['Annual_Income'])

    df['Monthly_Inhand_Salary'] = np.where(df['Monthly_Inhand_Salary'] > monthly_salary_upper_bound, np.nan,
                                           df['Monthly_Inhand_Salary'])
    df['Monthly_Inhand_Salary'] = np.where(df['Monthly_Inhand_Salary'] < monthly_salary_lower_bound, np.nan,
                                           df['Monthly_Inhand_Salary'])

    df['Num_Bank_Accounts'] = np.where(df['Num_Bank_Accounts'] > num_bank_accounts_upper_bound, np.nan,
                                       df['Num_Bank_Accounts'])
    df['Num_Bank_Accounts'] = np.where(df['Num_Bank_Accounts'] < num_bank_accounts_lower_bound, np.nan,
                                       df['Num_Bank_Accounts'])

    df['Num_Credit_Card'] = np.where(df['Num_Credit_Card'] > num_credit_cards_upper_bound, np.nan,
                                     df['Num_Credit_Card'])
    df['Num_Credit_Card'] = np.where(df['Num_Credit_Card'] < num_credit_cards_lower_bound, np.nan,
                                     df['Num_Credit_Card'])

    df['Interest_Rate'] = np.where(df['Interest_Rate'] > interest_rate_upper_bound, np.nan, df['Interest_Rate'])
    df['Interest_Rate'] = np.where(df['Interest_Rate'] < interest_rate_lower_bound, np.nan, df['Interest_Rate'])

    df['Num_of_Loan'] = np.where(df['Num_of_Loan'] > num_loans_upper_bound, np.nan, df['Num_of_Loan'])
    df['Num_of_Loan'] = np.where(df['Num_of_Loan'] < num_loans_lower_bound, np.nan, df['Num_of_Loan'])

    df['Delay_from_due_date'] = np.where(df['Delay_from_due_date'] > delay_from_due_date_upper_bound, np.nan,
                                         df['Delay_from_due_date'])
    df['Delay_from_due_date'] = np.where(df['Delay_from_due_date'] < delay_from_due_date_lower_bound, np.nan,
                                         df['Delay_from_due_date'])

    df['Num_of_Delayed_Payment'] = np.where(df['Num_of_Delayed_Payment'] > num_delayed_payments_upper_bound, np.nan,
                                            df['Num_of_Delayed_Payment'])
    df['Num_of_Delayed_Payment'] = np.where(df['Num_of_Delayed_Payment'] < num_delayed_payments_lower_bound, np.nan,
                                            df['Num_of_Delayed_Payment'])

    df['Changed_Credit_Limit'] = np.where(df['Changed_Credit_Limit'] > changed_credit_limit_upper_bound, np.nan,
                                          df['Changed_Credit_Limit'])
    df['Changed_Credit_Limit'] = np.where(df['Changed_Credit_Limit'] < changed_credit_limit_lower_bound, np.nan,
                                          df['Changed_Credit_Limit'])

    df['Num_Credit_Inquiries'] = np.where(df['Num_Credit_Inquiries'] > num_credit_inquiries_upper_bound, np.nan,
                                          df['Num_Credit_Inquiries'])
    df['Num_Credit_Inquiries'] = np.where(df['Num_Credit_Inquiries'] < num_credit_inquiries_lower_bound, np.nan,
                                          df['Num_Credit_Inquiries'])

    df['Credit_Utilization_Ratio'] = np.where(df['Credit_Utilization_Ratio'] > credit_utilization_ratio_upper_bound,
                                              np.nan, df['Credit_Utilization_Ratio'])
    df['Credit_Utilization_Ratio'] = np.where(df['Credit_Utilization_Ratio'] < credit_utilization_ratio_lower_bound,
                                              np.nan, df['Credit_Utilization_Ratio'])

    df['Total_EMI_per_month'] = np.where(df['Total_EMI_per_month'] > total_emi_upper_bound, np.nan,
                                         df['Total_EMI_per_month'])
    df['Total_EMI_per_month'] = np.where(df['Total_EMI_per_month'] < total_emi_lower_bound, np.nan,
                                         df['Total_EMI_per_month'])

    df['Amount_invested_monthly'] = np.where(df['Amount_invested_monthly'] > amount_invested_monthly_upper_bound,
                                             np.nan, df['Amount_invested_monthly'])
    df['Amount_invested_monthly'] = np.where(df['Amount_invested_monthly'] < amount_invested_monthly_lower_bound,
                                             np.nan, df['Amount_invested_monthly'])

    df['Monthly_Balance'] = np.where(df['Monthly_Balance'] > monthly_balance_upper_bound, np.nan, df['Monthly_Balance'])
    df['Monthly_Balance'] = np.where(df['Monthly_Balance'] < monthly_balance_lower_bound, np.nan, df['Monthly_Balance'])

    return df


df = handle_outliers(df)

# pick useful variables
useful_features = [
    'Age', 'Occupation', 'Annual_Income', 'Monthly_Inhand_Salary',
    'Num_Bank_Accounts', 'Num_Credit_Card', 'Interest_Rate', 'Num_of_Loan',
    'Delay_from_due_date', 'Num_of_Delayed_Payment',
    'Changed_Credit_Limit', 'Num_Credit_Inquiries', 'Credit_Mix',
    'Outstanding_Debt', 'Credit_Utilization_Ratio', 'Credit_History_Age',
    'Payment_of_Min_Amount', 'Total_EMI_per_month', 'Amount_invested_monthly',
    'Monthly_Balance'
]

numeric_features = df[useful_features].select_dtypes(include=['float64', 'int64']).columns

df[numeric_features] = df[numeric_features].fillna(df[numeric_features].median())

most_frequent_occupation = df['Occupation'].mode()[0]
df['Occupation'] = df['Occupation'].fillna(most_frequent_occupation)

df = df.dropna(subset=['Credit_Score'])

credit_score_mapping = {'Good': 2, 'Standard': 1, 'Poor': 0}
df['Credit_Score'] = df['Credit_Score'].map(credit_score_mapping)

X = df[useful_features]
y = df['Credit_Score']

class_weights = compute_class_weight('balanced', classes=np.unique(y), y=y)
y = tf.keras.utils.to_categorical(y, num_classes=3)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

categorical_features = X_train.select_dtypes(include=['object']).columns

numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())])

categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)])

X_train_transformed = preprocessor.fit_transform(X_train)
X_test_transformed = preprocessor.transform(X_test)

# model = tf.keras.Sequential([
#     tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train_transformed.shape[1],)),
#     tf.keras.layers.Dense(32, activation='relu'),
#     tf.keras.layers.Dense(16, activation='relu'),
#     tf.keras.layers.Dense(8, activation='relu'),
#     tf.keras.layers.Dense(3, activation='softmax')
# ])

model = tf.keras.Sequential([
    tf.keras.layers.Reshape((X_train_transformed.shape[1], 1)),
    tf.keras.layers.Conv1D(filters=32, kernel_size=3, activation='relu'),
    tf.keras.layers.MaxPooling1D(pool_size=2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, verbose=1, min_lr=1e-6)
opt = tf.keras.optimizers.Adam(learning_rate=1e-3)
model.compile(optimizer=opt,
              loss='categorical_crossentropy',
              metrics=['accuracy'])
X_train_transformed[np.isnan(X_train_transformed)] = 0
X_test_transformed[np.isnan(X_test_transformed)] = 0

model.fit(X_train_transformed, y_train, epochs=10, batch_size=32, validation_split=0.2,
          callbacks=[reduce_lr])  # , class_weight={i:j for i,j in enumerate(class_weights.tolist())})
print(model.summary())

y_pred_prob = model.predict(X_test_transformed)
y_pred = np.argmax(y_pred_prob, axis=1)
y_test = np.argmax(y_test, axis=1)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
model.save("checkpoint.h5")
