# EasyCredit: Simplified Credit Risk Classification for Moderate Transactions
Introducing EasyCredit, a streamlined credit assessing system designed for moderate-sized transactions that don't require a comprehensive credit report. EasyCredit provides a machine-generated assessment of your financial reliability by securely analyzing your transaction history with some other parties, such as rental agencies or utility companies, without disclosing sensitive details to your trading partners. This innovative system is perfect for situations where a transaction is significant enough to warrant an endorsement of your creditworthiness but doesn't necessitate a hard credit check.

EasyCredit leverages technologies such as Multi-Party Computation (MPC), Homomorphic Encryption and Neural Networks to ensure the highest levels of security, privacy, and efficiency. By employing these advanced techniques, EasyCredit guarantees that your financial information remains confidential throughout the credit assessment process.

## Workflow:
Parties:

- User: the individual whose credit risk is being assessed
- Company: the organization that is requesting the credit risk assessment of the user
- Agency: a third party who is contact to provide informatiom about their transactions with the user. Multiple agencies may join.

### Step 1. Initiation:

Once the user, company, and all relevant third party agencies have joined on their own MPC threads, a Paillier private key is generated for the user, and the corresponding public key is shared with the agencies.

### Step 2. Third Parties Input Data:

The third party agencies are asked to provide information about their recent transactions with the user: the time and amount of payments and delays. These values will then be encrypted with the public key and securely aggregated to produce scores which are returned to the server. The user will then use the private key to decrypt the scores.

### Step 3. Server Processes Data:

The server loads the user's sensitive financial data from a file and immediately pseudo-encrypts it. When it has received and decrypted the aggregated scores from the MPC threads, it compiles the data and the scores into one dataframe. The trained neural network model is loaded and the dataframe is passed in to produce the prediction of the user's credit risk: 'Poor' or 'Good'. This prediction is once again encrypted with the public key and sent to the user and the company's servers.

### Step 4. Results Shared:

The user and company receive the encrypted result, which they then decrypt using the private key. They both now have access to the user's predicted credit risk and may use it for next steps in the loan application process.

## Demo Usage:

The program is run from demo.py, and each party runs its own version of the file in an individual terminal window with a modified command. The value attached to the -M flag indicated how many total parties are expected to join, while the values attached to the -I flag indicate the identity of the party. I0 denotes the user, I1 denotes the company, and I2...N indicate the third party agencies.

#### With 3 parties:
python3 demo.py -M3 -I0 --no-log # -> user

python3 demo.py -M3 -I1 --no-log # -> comppany

python3 demo.py -M3 -I2 --no-log # -> 2...N for each agency

