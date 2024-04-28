# EasyCredit: Simplified Credit Risk Classification for Moderate Transactions
Introducing EasyCredit, a streamlined credit assessing system designed for moderate-sized transactions that don't require a comprehensive credit report. EasyCredit provides a machine-generated assessment of your financial reliability by securely analyzing your transaction history with some other parties without disclosing sensitive details to your trading partners. This innovative system is perfect for situations where a transaction is significant enough to warrant an endorsement of your creditworthiness but doesn't necessitate a full credit check.

EasyCredit leverages technologies including Multi-Party Computation (MPC), homomorphic encryption and machine learning to ensure the highest levels of security, privacy, and efficiency. By employing these advanced techniques, EasyCredit guarantees that your financial information remains confidential throughout the credit assessment process.

## Workflow Design:

### Step 1. Initiation:

Customer and insurance company start the process to request for easy credit assessment, they exchange keys with the server. 
Third parties (car agency, utility company) are also invited to provide info

### Step 2. Customer Uploads Docs:

Customer uploads financial docs. The docs are authenticated, parsed and encrypted using homomorphic encryption algorithm. For unified data, they are sent to the server directly, for customized data, they are sub-categorized and sent to MPC thread

Now the MPC thread is waiting for other parties.

### Third Parties Upload Docs:

Car agency and utility company upload docs they have, they follow the same process as the customer and join the MPC thread.

### MPC Aggregates Data:

All parties now joined to the MPC thread. They then generate aggregate stats for each data subcategory

### Server Processes Data:

The server gets unified data and MPC aggregate stats, it uses unified data primarily and use aggregate stats as a support. It runs homomorphic ML model that computes encrypted data directly and generate trustworthiness score

### Results Shared:

The customer and insurance company receives the results. They use their own private key to decrypt the results and use them for next steps in discount application process

## Demo Usage:
