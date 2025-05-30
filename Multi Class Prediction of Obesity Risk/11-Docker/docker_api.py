import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import PolynomialFeatures
import lightgbm as lgb
from sklearn.metrics import accuracy_score
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.model_selection import StratifiedKFold
import uvicorn
from pathlib import Path
import pickle

app = FastAPI()


def load_data(path):
    df = pd.read_csv(path)
    train_df, test_df = train_test_split(df, test_size=0.35, random_state=42)
    (
        train_df,
        val_df,
    ) = train_test_split(train_df, test_size=0.20, random_state=42)
    train_df = train_df.drop(["id"], axis=1).drop_duplicates().reset_index(drop=True)
    test_df = test_df.drop(["id"], axis=1).drop_duplicates().reset_index(drop=True)
    val_df = val_df.drop(["id"], axis=1).drop_duplicates().reset_index(drop=True)
    return train_df, val_df, test_df


def encode_target(train):
    target_key = {
        "Insufficient_Weight": 0,
        "Normal_Weight": 1,
        "Overweight_Level_I": 2,
        "Overweight_Level_II": 3,
        "Obesity_Type_I": 4,
        "Obesity_Type_II": 5,
        "Obesity_Type_III": 6,
    }
    train["NObeyesdad"] = train["NObeyesdad"].map(target_key)
    return train


def datatypes(train):
    train["Weight"] = train["Weight"].astype(float)
    train["Age"] = train["Age"].astype(float)
    train["Height"] = train["Height"].astype(float)
    return train


# def age_binning(train_df):
#     train_df['Age_Group'] = pd.cut(train_df['Age'], bins=[0, 20, 30, 40, 50, train_df['Age'].max()], labels=['0-20', '21-30', '31-40', '41-50', '50+'])
#     return train_df


def age_binning(df):
    age_groups = []
    for age in df["Age"]:
        if age <= 20:
            age_group = 1
        elif age <= 30:
            age_group = 2
        elif age <= 40:
            age_group = 3
        elif age <= 50:
            age_group = 4
        else:
            age_group = 5
        age_groups.append(age_group)
    df["Age_Group"] = age_groups
    return df


def age_scaling_log(train_df):
    train_df["Age"] = train_df["Age"].astype(float)
    train_df["Log_Age"] = np.log1p(train_df["Age"])
    return train_df


def age_scaling_minmax(train_df):
    train_df["Age"] = train_df["Age"].astype(float)
    scaler_age = MinMaxScaler()
    train_df["Scaled_Age"] = scaler_age.fit_transform(
        train_df["Age"].values.reshape(-1, 1)
    )
    return train_df, scaler_age


def weight_scaling_log(train_df):
    train_df["Weight"] = train_df["Weight"].astype(float)
    train_df["Log_Weight"] = np.log1p(train_df["Weight"])
    return train_df


def weight_scaling_minmax(train_df):
    train_df["Weight"] = train_df["Weight"].astype(float)
    scaler_weight = MinMaxScaler()
    train_df["Scaled_Weight"] = scaler_weight.fit_transform(
        train_df["Weight"].values.reshape(-1, 1)
    )
    return train_df, scaler_weight


def height_scaling_log(train_df):
    train_df["Log_Height"] = np.log1p(train_df["Height"])
    return train_df


def height_scaling_minmax(train_df):
    scaler_height = MinMaxScaler()
    train_df["Scaled_Height"] = scaler_height.fit_transform(
        train_df["Height"].values.reshape(-1, 1)
    )
    return train_df, scaler_height


def make_gender_binary(train):
    train["Gender"] = train["Gender"].map({"Female": 1, "Male": 0})
    return train


def fix_binary_columns(train):
    Binary_Cols = ["family_history_with_overweight", "FAVC", "SCC", "SMOKE"]
    # if yes then 1 else 0
    for col in Binary_Cols:
        train[col] = train[col].map({"yes": 1, "no": 0})
    return train


def freq_cat_cols(train):
    # One hot encoding
    cat_cols = ["CAEC", "CALC"]
    for col in cat_cols:
        train[col] = train[col].map(
            {"no": 0, "Sometimes": 1, "Frequently": 2, "Always": 3}
        )
    return train


def Mtrans(train):
    """
    Public_Transportation    8692
    Automobile               1835
    Walking                   231
    Motorbike                  19
    Bike                       16
    """
    # train['MTRANS'] = train['MTRANS'].map({'Public_Transportation': 3, 'Automobile': 5, 'Walking': 1, 'Motorbike': 4, 'Bike': 2})
    # dummify column
    train = pd.get_dummies(train, columns=["MTRANS"])
    return train


def other_features(train):
    train["BMI"] = train["Weight"] / (train["Height"] ** 2)
    # train['Age'*'Gender'] = train['Age'] * train['Gender']
    polynomial_features = PolynomialFeatures(degree=2)
    X_poly = polynomial_features.fit_transform(train[["Age", "BMI"]])
    poly_features_df = pd.DataFrame(
        X_poly,
        columns=[
            "Age^2",
            "Age^3",
            "BMI^2",
            "Age * BMI",
            "Age * BMI^2",
            "Age^2 * BMI^2",
        ],
    )
    train = pd.concat([train, poly_features_df], axis=1)
    return train


def test_pipeline(test, scaler_age, scaler_weight, scaler_height):
    test = datatypes(test)
    test = encode_target(test)
    test = age_binning(test)
    test = age_scaling_log(test)
    test["Scaled_Age"] = scaler_age.transform(test["Age"].values.reshape(-1, 1))
    test = weight_scaling_log(test)
    test["Scaled_Weight"] = scaler_weight.transform(
        test["Weight"].values.reshape(-1, 1)
    )
    test = height_scaling_log(test)
    test["Scaled_Height"] = scaler_height.transform(
        test["Height"].values.reshape(-1, 1)
    )
    test = make_gender_binary(test)
    test = fix_binary_columns(test)
    test = freq_cat_cols(test)
    test = Mtrans(test)
    test = other_features(test)

    return test


def train_model(params, X_train, y_train):
    lgb_train = lgb.Dataset(X_train, y_train)
    model = lgb.train(params, lgb_train, num_boost_round=1000)
    return model


def evaluate_model(model, X_val, y_val):
    y_pred = model.predict(X_val)
    y_pred = [np.argmax(y) for y in y_pred]
    accuracy = accuracy_score(y_val, y_pred)
    return accuracy


def objective(trial, X_train, y_train):
    params = {
        "objective": "multiclass",
        "num_class": 7,
        "metric": "multi_logloss",
        "boosting_type": "gbdt",
        "learning_rate": trial.suggest_loguniform("learning_rate", 0.005, 0.5),
        "num_leaves": trial.suggest_int("num_leaves", 10, 1000),
        "max_depth": trial.suggest_int("max_depth", -1, 20),
        "bagging_fraction": trial.suggest_uniform("bagging_fraction", 0.6, 0.95),
        "feature_fraction": trial.suggest_uniform("feature_fraction", 0.6, 0.95),
        "verbosity": -1,
    }

    n_splits = 5
    kf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    scores = []

    for train_index, val_index in kf.split(X_train, y_train):
        X_tr, X_val = X_train.iloc[train_index], X_train.iloc[val_index]
        y_tr, y_val = y_train.iloc[train_index], y_train.iloc[val_index]

        model = train_model(params, X_tr, y_tr)
        accuracy = evaluate_model(model, X_val, y_val)
        scores.append(accuracy)

    return np.mean(scores)


def optimize_hyperparameters(X_train, y_train, n_trials=2):
    study = optuna.create_study(direction="maximize")
    study.optimize(lambda trial: objective(trial, X_train, y_train), n_trials=n_trials)
    return study.best_params


def New_Test_Instances_Pipeline(test, scaler_age, scaler_weight, scaler_height):
    test = datatypes(test)
    test = age_binning(test)
    test = age_scaling_log(test)
    test["Scaled_Age"] = scaler_age.transform(test["Age"].values.reshape(-1, 1))
    test = weight_scaling_log(test)
    test["Scaled_Weight"] = scaler_weight.transform(
        test["Weight"].values.reshape(-1, 1)
    )
    test = height_scaling_log(test)
    test["Scaled_Height"] = scaler_height.transform(
        test["Height"].values.reshape(-1, 1)
    )
    test = make_gender_binary(test)
    test = fix_binary_columns(test)
    test = freq_cat_cols(test)
    test = Mtrans(test)
    test = other_features(test)

    return test


############################################
# Define your input data model
class InputData(BaseModel):
    id: int
    Gender: str
    Age: float
    Height: float
    Weight: float
    family_history_with_overweight: str
    FAVC: str
    FCVC: float
    NCP: float
    CAEC: str
    SMOKE: str
    CH2O: float
    SCC: str
    FAF: float
    TUE: float
    CALC: str
    MTRANS: str
    DRIFT: int


@app.post("/predict", response_model=dict)
async def predict(item: InputData):
    input_data = item.model_dump()
    drift = item.DRIFT
    if drift == 1:
        # load model
        with open("model.pkl", "rb") as f:
            model = pickle.load(f)
    else:
        # load model
        with open("model2.pkl", "rb") as f:
            model = pickle.load(f)

    # # #Sample input data
    # input_data = {
    #     "id": 6204,
    #     "Gender": "Female",
    #     "Age": 23.0,
    #     "Height": 1.581527,
    #     "Weight": 78.089575,
    #     "family_history_with_overweight": "yes",
    #     "FAVC": "yes",
    #     "FCVC": 2.0,
    #     "NCP": 2.070033,
    #     "CAEC": "Sometimes",
    #     "SMOKE": "no",
    #     "CH2O": 2.953192,
    #     "SCC": "no",
    #     "FAF": 0.118271,
    #     "TUE": 0.0,
    #     "CALC": "no",
    #     "MTRANS": "Public_Transportation",
    # }
    # convert input to df
    input_df = pd.DataFrame([input_data])
    # drop drift
    input_df = input_df.drop(columns=["DRIFT"])

    path = "train.csv"
    train_df, val_df, test_df = load_data(path)
    # train test val pipeline
    train_df = datatypes(train_df)
    train_df = encode_target(train_df)
    train_df = age_binning(train_df)
    train_df, scaler_age = age_scaling_minmax(train_df)
    train_df = age_scaling_log(train_df)
    train_df, scaler_weight = weight_scaling_minmax(train_df)
    train_df = weight_scaling_log(train_df)
    train_df, scaler_height = height_scaling_minmax(train_df)
    train_df = height_scaling_log(train_df)
    train_df = make_gender_binary(train_df)
    train_df = fix_binary_columns(train_df)
    train_df = freq_cat_cols(train_df)
    train_df = Mtrans(train_df)
    train_df = other_features(train_df)

    input_df = New_Test_Instances_Pipeline(
        input_df, scaler_age, scaler_weight, scaler_height
    )

    # target & predictors
    Target = "NObeyesdad"

    features = [
        "Gender",
        "Age",
        "Height",
        "Weight",
        "family_history_with_overweight",
        "FAVC",
        "FCVC",
        "NCP",
        "CAEC",
        "SMOKE",
        "CH2O",
        "SCC",
        "FAF",
        "TUE",
        "CALC",
        "Age_Group",
        "MTRANS_Automobile",
        "MTRANS_Bike",
        "MTRANS_Motorbike",
        "MTRANS_Public_Transportation",
        "MTRANS_Walking",
        "BMI",
        "Age^2",
        "Age^3",
        "BMI^2",
        "Age * BMI",
        "Age * BMI^2",
        "Age^2 * BMI^2",
    ]

    # X input to have same columns as features
    X_input = pd.DataFrame(columns=features)
    # if input df does not have a column that is in features, add it with 0s at the same position
    for col in features:
        if col not in input_df.columns:
            if col in [
                "MTRANS_Automobile",
                "MTRANS_Bike",
                "MTRANS_Motorbike",
                "MTRANS_Public_Transportation",
                "MTRANS_Walking",
            ]:
                X_input[col] = False
            else:
                X_input[col] = 0
        else:
            X_input[col] = input_df[col]
        # if MTRANS_Automobile, MTRANS_Bike, MTRANS_Motorbike, MTRANS_Public_Transportation, MTRANS_Walking are zero, make them False

    y_pred_proba = model.predict(X_input)
    y_pred = np.argmax(y_pred_proba)

    probabilities = []

    for prob in y_pred_proba[0]:
        probabilities.append(round(prob, 2))

    return {
        "prediction": int(y_pred),
        "Prob0": float(probabilities[0]),
        "Prob1": float(probabilities[1]),
        "Prob2": float(probabilities[2]),
        "Prob3": float(probabilities[3]),
        "Prob4": float(probabilities[4]),
        "Prob5": float(probabilities[5]),
        "Prob6": float(probabilities[6]),
        "Drift": int(drift),
    }


@app.get("/")
async def home():
    return {"Welcome to Obesity Risk Detector!": 200}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
