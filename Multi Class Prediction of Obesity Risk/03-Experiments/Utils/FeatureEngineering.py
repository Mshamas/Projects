# Advanced feature engineering for training data
def age_stuff(train_df):
    train_df['Age_Group'] = pd.cut(train_df['Age'], bins=[0, 20, 30, 40, 50, 55], labels=['A', 'B', 'C', 'D', 'E'],)
    train_df['Log_Age'] = np.log1p(train_df['Age'])
    scaler = MinMaxScaler()
    train_df['Scaled_Age'] = scaler.fit_transform(train_df['Age'].values.reshape(-1, 1))
    return train_df

def advanced_age_stuff(train):
    train['Age group'] = pd.cut(train['Age'], bins=[0, 18, 30, 45, 60, train['Age'].max()], labels=['0-18', '19-30', '31-45', '46-60', '60+'])
    train['BMI'] = train['Weight'] / (train['Height'] ** 2)

    train['Age * Gender'] = train['Age'] * train['Gender']   

    # categorical_features = ['Gender', 'family_history_with_overweight', 'Age group', 'FAVC','CAEC', 'SMOKE','SCC', 'CALC', 'MTRANS']
    # train = pd.get_dummies(train, columns=categorical_features)

    # polynomial_features = PolynomialFeatures(degree=2)
    # X_poly = polynomial_features.fit_transform(train[['Age', 'BMI']])
    # train = pd.concat([train, pd.DataFrame(X_poly, columns=['Age^2', 'Age^3', 'BMI^2', 'Age * BMI', 'Age * BMI2', 'Age * BMI3'])], axis=1)
    return train



