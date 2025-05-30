import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import PolynomialFeatures

def load_data(path):
    df = pd.read_csv(path)
    train_df, test_df = train_test_split(df, test_size=0.35, random_state=42)
    train_df, val_df,  = train_test_split(train_df, test_size=0.20, random_state=42)
    train_df = train_df.drop(['id'], axis=1).drop_duplicates().reset_index(drop=True)
    test_df = test_df.drop(['id'], axis=1).drop_duplicates().reset_index(drop=True)
    val_df = val_df.drop(['id'], axis=1).drop_duplicates().reset_index(drop=True)
    return train_df, val_df, test_df

def encode_target(train):
    target_key = {'Insufficient_Weight': 0, 'Normal_Weight': 1, 'Overweight_Level_I': 2, 'Overweight_Level_II': 3, 'Obesity_Type_I': 4,'Obesity_Type_II' : 5, 'Obesity_Type_III': 6}
    train['NObeyesdad'] = train['NObeyesdad'].map(target_key)
    return train

def datatypes(train):
    train['Weight'] = train['Weight'].astype(float)
    train['Age'] = train['Age'].astype(float)
    train['Height'] = train['Height'].astype(float)
    return train

def age_binning(train_df):
    train_df['Age_Group'] = pd.cut(train_df['Age'], bins=[0, 20, 30, 40, 50, train_df['Age'].max()], labels=['0-20', '21-30', '31-40', '41-50', '50+'])
    return train_df

def age_scaling_log(train_df):
    train_df['Age'] = train_df['Age'].astype(float)
    train_df['Log_Age'] = np.log1p(train_df['Age'])
    return train_df

def age_scaling_minmax(train_df):
    train_df['Age'] = train_df['Age'].astype(float)
    scaler_age = MinMaxScaler()
    train_df['Scaled_Age'] = scaler_age.fit_transform(train_df['Age'].values.reshape(-1, 1))
    return train_df, scaler_age

def weight_scaling_log(train_df):
    train_df['Weight'] = train_df['Weight'].astype(float)
    train_df['Log_Weight'] = np.log1p(train_df['Weight'])
    return train_df

def weight_scaling_minmax(train_df):
    train_df['Weight'] = train_df['Weight'].astype(float)
    scaler_weight = MinMaxScaler()
    train_df['Scaled_Weight'] = scaler_weight.fit_transform(train_df['Weight'].values.reshape(-1, 1))
    return train_df, scaler_weight

def height_scaling_log(train_df):
    train_df['Log_Height'] = np.log1p(train_df['Height'])
    return train_df

def height_scaling_minmax(train_df):
    scaler_height = MinMaxScaler()
    train_df['Scaled_Height'] = scaler_height.fit_transform(train_df['Height'].values.reshape(-1, 1))
    return train_df, scaler_height

def other_features(train):
    # Print data types of 'Age' and 'Gender' columns
    print("Data types:")
    print(train[['Age', 'Gender']].dtypes)

    # Check for non-numeric values in 'Age' and 'Gender' columns
    print("\nUnique values in 'Age' column:")
    print(train['Age'].unique())
    print("\nUnique values in 'Gender' column:")
    print(train['Gender'].unique())

    # Perform multiplication
    train['BMI'] = train['Weight'] / (train['Height'] ** 2)
    train = make_gender_binary(train)
    train['Age * Gender'] = train['Age'] * train['Gender']   
    categorical_features = ['family_history_with_overweight', 'Age_Group', 'FAVC','CAEC', 'SMOKE','SCC', 'CALC', 'MTRANS']
    train = pd.get_dummies(train, columns=categorical_features)
    polynomial_features = PolynomialFeatures(degree=2)
    X_poly = polynomial_features.fit_transform(train[['Age', 'BMI']])
    poly_features_df = pd.DataFrame(X_poly, columns=['Age^2', 'Age^3', 'BMI^2', 'Age * BMI', 'Age * BMI^2', 'Age^2 * BMI^2'])
    train = pd.concat([train, poly_features_df], axis=1)
    return train

def test_pipeline(test, scaler_age, scaler_weight, scaler_height):
    test = encode_target(test)
    test = age_binning(test)
    test = age_scaling_log(test)
    test['Scaled_Age'] = scaler_age.transform(test['Age'].values.reshape(-1, 1))
    test = weight_scaling_log(test)
    test['Scaled_Weight'] = scaler_weight.transform(test['Weight'].values.reshape(-1, 1))
    test = height_scaling_log(test)
    test['Scaled_Height'] = scaler_height.transform(test['Height'].values.reshape(-1, 1))
    test = other_features(test)
    return test

