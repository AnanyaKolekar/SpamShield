import pandas as pd
rows = []
with open("SMSSpamCollection.txt","r",encoding="utf-8") as file:
    for line in file:
        label, message=line.strip().split("\t",1)
        if label=="ham":
            rows.append([message,""])
        else:
            rows.append(["",message])

df = pd.DataFrame(rows, columns=["ham", "spam"])

df.to_csv("sms_ham_spam.csv", index=False)

print("CSV with separate ham & spam columns created!")