from Model.QuestionModel import Question
import pandas as pd

def one_hot_encoding(df):
    # renaming columns
    df.rename(columns={
        'Increase' : 'NEW_Increase',
        'AVG_Service_Fee' : 'NEW_AVG_Service_Fee'
    }, inplace=True)
    # one hot encoding
    df.loc[df["Contract"] == 2, "Contract_2.0"] = 1
    df.loc[df["Contract"] != 2, "Contract_2.0"] = 0
    df.loc[df["PaymentMethod"] == 2, "PaymentMethod_2.0"] = 1
    df.loc[df["PaymentMethod"] != 2, "PaymentMethod_2.0"] = 0
    df.loc[df["InternetService"] == 1, "InternetService_1.0"] = 1
    df.loc[df["InternetService"] != 1, "InternetService_1.0"] = 0
    df.loc[df["InternetService"] == 2, "InternetService_2.0"] = 1
    df.loc[df["InternetService"] != 2, "InternetService_2.0"] = 0
    df.loc[df["Contract"] == 1, "Contract_1.0"] = 1
    df.loc[df["Contract"] != 1, "Contract_1.0"] = 0
    df.loc[df["SeniorCitizen"] == 1, "SeniorCitizen_1.0"] = 1
    df.loc[df["SeniorCitizen"] != 1, "SeniorCitizen_1.0"] = 0
    df.loc[df["OnlineSecurity"] == 1, "OnlineSecurity_1.0"] = 1
    df.loc[df["OnlineSecurity"] != 1, "OnlineSecurity_1.0"] = 0
    df.loc[df["Dependents"] == 1, "Dependents_1.0"] = 1
    df.loc[df["Dependents"] != 1, "Dependents_1.0"] = 0
    df.loc[df["TechSupport"] == 1, "TechSupport_1.0"] = 1
    df.loc[df["TechSupport"] != 1, "TechSupport_1.0"] = 0
    df.loc[df["PaymentMethod"] == 1, "PaymentMethod_1.0"] = 1
    df.loc[df["PaymentMethod"] != 1, "PaymentMethod_1.0"] = 0
    df.loc[df["PaperlessBilling"] == 1, "PaperlessBilling_1.0"] = 1
    df.loc[df["PaperlessBilling"] != 1, "PaperlessBilling_1.0"] = 0
    df.loc[df["TotalServices"] == 2, "NEW_TotalServices_2.0"] = 1
    df.loc[df["TotalServices"] != 2, "NEW_TotalServices_2.0"] = 0
    df.loc[df["Partner"] == 1, "Partner_1.0"] = 1
    df.loc[df["Partner"] != 1, "Partner_1.0"] = 0
    df.loc[df["TENURE_YEAR"] == 4, "NEW_TENURE_YEAR_4.0"] = 1
    df.loc[df["TENURE_YEAR"] != 4, "NEW_TENURE_YEAR_4.0"] = 0
    df.loc[df["TotalServices"] == 6, "NEW_TotalServices_6.0"] = 1
    df.loc[df["TotalServices"] != 6, "NEW_TotalServices_6.0"] = 0
    df.drop(['PaymentMethod', 'Contract', 'InternetService', 'SeniorCitizen', 'OnlineSecurity', 'TechSupport', 'Dependents',
                'PaperlessBilling', 'Partner', 'TotalServices', 'TENURE_YEAR','TotalCharges','AVG_Charges'], axis=1, inplace=True)
    return df
    
def preProcess(question: Question):
    # converting question to dataframe
    df = pd.DataFrame([question.dict()])
    # converting datetime to date
    df['birthday'] = pd.to_datetime(df['birthday']).dt.date
    # converting date to age
    df['age'] = (pd.to_datetime('today').date() - df['birthday']).astype('<m8[Y]')
    df['SeniorCitizen'] = df['age'].apply(lambda x: 1 if x >= 65 else 0)
    # dropping birthday column
    df.drop(['birthday','age'], axis=1, inplace=True)
    # converting boolean to int
    df['hasPartner'] = df['hasPartner'].astype(int)
    df['hasDependents'] = df['hasDependents'].astype(int)
    df['hasOnlineSecurity'] = df['hasOnlineSecurity'].astype(int)
    df['hasTechSupport'] = df['hasTechSupport'].astype(int)
    df['paperlessBilling'] = df['paperlessBilling'].astype(int)

    # renaming columns
    df.rename(columns={'hasPartner': 'Partner', 'hasDependents': 'Dependents', 'hasOnlineSecurity': 'OnlineSecurity',
                          'hasTechSupport': 'TechSupport', 'contractType': 'Contract', 'paperlessBilling': 'PaperlessBilling',
                            'paymentMethod': 'PaymentMethod', 'monthlyCharges': 'MonthlyCharges', 'totalCharges': 'TotalCharges',
                                'totalServices':'TotalServices'}, inplace=True)
    df = featureExtraction(df)
    df = one_hot_encoding(df)
    print(df.head())
    print(df.columns)
   
    # save to csv
    df.to_csv("data.csv", index=False)
    return df

def featureExtraction(df):
     # read class mapping json
    import json
    with open('class_mapping.json') as f:
        class_mapping = json.load(f)
    # converting categorical to numerical
        df.loc[(df["tenure"] >= 0) & (df["tenure"] <= 12), "TENURE_YEAR"] = class_mapping["TENURE_YEAR"]["0-1 Year"]
        df.loc[(df["tenure"] > 12) & (df["tenure"] <= 24), "TENURE_YEAR"] = class_mapping["TENURE_YEAR"]["1-2 Year"]
        df.loc[(df["tenure"] > 24) & (df["tenure"] <= 36), "TENURE_YEAR"] = class_mapping["TENURE_YEAR"]["2-3 Year"]
        df.loc[(df["tenure"] > 36) & (df["tenure"] <= 48), "TENURE_YEAR"] = class_mapping["TENURE_YEAR"]["3-4 Year"]
        df.loc[(df["tenure"] > 48) & (df["tenure"] <= 60), "TENURE_YEAR"] = class_mapping["TENURE_YEAR"]["4-5 Year"]
        df.loc[(df["tenure"] > 60) & (df["tenure"] <= 72), "TENURE_YEAR"] = class_mapping["TENURE_YEAR"]["5-6 Year"]

        df.loc[df["InternetService"] == "DSL", "InternetService"] = class_mapping["InternetService"]["DSL"]
        df.loc[df["InternetService"] == "Fiber optic", "InternetService"] = class_mapping["InternetService"]["Fiber optic"]
        df.loc[df["InternetService"] == "No", "InternetService"] = class_mapping["InternetService"]["No"]

        df.loc[df["Contract"] == "Month-to-month", "Contract"] = class_mapping["Contract"]["Month-to-month"]
        df.loc[df["Contract"] == "One year", "Contract"] = class_mapping["Contract"]["One year"]
        df.loc[df["Contract"] == "Two year", "Contract"] = class_mapping["Contract"]["Two year"]

        df.loc[df["PaymentMethod"] == "Electronic check", "PaymentMethod"] = class_mapping["PaymentMethod"]["Electronic check"]
        df.loc[df["PaymentMethod"] == "Mailed check", "PaymentMethod"] = class_mapping["PaymentMethod"]["Mailed check"]
        df.loc[df["PaymentMethod"] == "Bank transfer (automatic)", "PaymentMethod"] = class_mapping["PaymentMethod"]["Bank transfer (automatic)"]
        df.loc[df["PaymentMethod"] == "Credit card (automatic)", "PaymentMethod"] = class_mapping["PaymentMethod"]["Credit card (automatic)"]

        
        df["AVG_Charges"] = df["TotalCharges"] / (df["tenure"] +0.1)
        df["Increase"] = df["AVG_Charges"] / (df["MonthlyCharges"] + 1)
        df["AVG_Service_Fee"] = df["MonthlyCharges"] / (df['TotalServices'] + 1)


        # drop unnecessary column
        return df