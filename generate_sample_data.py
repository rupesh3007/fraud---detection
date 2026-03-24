import pandas as pd
import numpy as np
import random

NUM_ROWS = 100000

transaction_types = [
    "PAYMENT",
    "TRANSFER",
    "CASH_OUT",
    "DEBIT",
    "CASH_IN"
]

def generate_data(rows):

    data = []

    for _ in range(rows):

        step = random.randint(1, 743)

        txn_type = random.choice(transaction_types)

        amount = round(random.uniform(100, 300000), 2)

        nameOrig = "C" + str(random.randint(10000000, 99999999))

        # destination logic
        if txn_type in ["TRANSFER", "CASH_OUT"]:
            nameDest = "C" + str(random.randint(10000000, 99999999))
        else:
            nameDest = "M" + str(random.randint(10000000, 99999999))

        oldbalanceOrg = round(random.uniform(1000, 500000), 2)

        # ensure transaction possible
        if amount > oldbalanceOrg:
            amount = round(random.uniform(100, oldbalanceOrg), 2)

        newbalanceOrig = oldbalanceOrg - amount

        oldbalanceDest = round(random.uniform(0, 500000), 2)
        newbalanceDest = oldbalanceDest + amount

        # fraud logic
        isFraud = 0

        if txn_type in ["TRANSFER", "CASH_OUT"]:
            if amount > 90000 and random.random() < 0.6:
                isFraud = 1
            elif amount > 50000 and random.random() < 0.3:
                isFraud = 1

        # flagged fraud
        isFlaggedFraud = 1 if amount > 200000 else 0

        data.append([
            step,
            txn_type,
            amount,
            nameOrig,
            oldbalanceOrg,
            newbalanceOrig,
            nameDest,
            oldbalanceDest,
            newbalanceDest,
            isFraud,
            isFlaggedFraud
        ])

    columns = [
        "step",
        "type",
        "amount",
        "nameOrig",
        "oldbalanceOrg",
        "newbalanceOrig",
        "nameDest",
        "oldbalanceDest",
        "newbalanceDest",
        "isFraud",
        "isFlaggedFraud"
    ]

    return pd.DataFrame(data, columns=columns)


def main():

    print("Generating dataset...")

    df = generate_data(NUM_ROWS)

    df.to_csv("synthetic_transactions_large.csv", index=False)

    print("Dataset generated successfully!")
    print("Total rows:", len(df))


if __name__ == "__main__":
    main()