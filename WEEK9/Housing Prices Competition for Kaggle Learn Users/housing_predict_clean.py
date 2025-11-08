# ===== HOUSING PRICE PREDICTION - CLEAN VERSION =====
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from category_encoders import TargetEncoder
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

print("🚀 Starting Housing Price Prediction...")

# ===== 1. LOAD DATA =====
print("\n📂 Loading data...")
train_data = pd.read_csv("train.csv")
test_data = pd.read_csv("test.csv")

# Drop null columns
for col in train_data.columns:
    if train_data[col].isnull().sum() > 500:
        train_data.drop(columns=[col], inplace=True)

# Drop zero columns
def drop_zero_columns(df, threshold_ratio=0.5):
    n_rows = len(df)
    cols_to_drop = []
    for col in df.columns:
        zero_count = (df[col] == 0).sum()
        if zero_count / n_rows > threshold_ratio:
            cols_to_drop.append(col)
    df.drop(columns=cols_to_drop, inplace=True)
    return cols_to_drop

drop_zero_columns(train_data, threshold_ratio=0.5)

print(f"✅ Train shape: {train_data.shape}")
print(f"✅ Test shape: {test_data.shape}")

# ===== 2. FEATURE ENGINEERING FUNCTION =====
def feature_engineering(train_df, test_df, target_col='SalePrice'):
    """Xử lý tất cả feature engineering với scaler riêng biệt"""
    
    # Selected features
    features_ob = ['BsmtExposure','BsmtFinType1','BsmtQual','Exterior1st','Exterior2nd',
                   'ExterQual','Foundation','GarageFinish','GarageType','HeatingQC',
                   'HouseStyle','KitchenQual','LandSlope','LotConfig','LotShape',
                   'MSZoning','Neighborhood','RoofStyle','SaleCondition','YrSold']
    
    features_num = ['OverallQual','YearBuilt','YearRemodAdd','TotalBsmtSF','1stFlrSF',
                    'GrLivArea','FullBath','TotRmsAbvGrd','GarageCars','GarageArea']
    
    all_features = features_num + features_ob + [target_col]
    train_X = train_df[all_features].copy()
    
    features_no_target = [c for c in all_features if c != target_col]
    test_X = test_df[features_no_target].copy()
    
    # Categorical encoding
    col_BsmtFinType1 = {'Unf': 1, 'GLQ': 2, 'ALQ': 3, 'BLQ': 3, 'Rec': 3, 'LwQ': 3}
    train_X['BsmtFinType1'] = train_X['BsmtFinType1'].map(col_BsmtFinType1).fillna(4)
    test_X['BsmtFinType1'] = test_X['BsmtFinType1'].map(col_BsmtFinType1).fillna(4)
    
    col_BsmtExposure = {'No': 1, 'Av': 2, 'Mn': 2, 'Gd': 3}
    train_X['BsmtExposure'] = train_X['BsmtExposure'].map(col_BsmtExposure).fillna(4)
    test_X['BsmtExposure'] = test_X['BsmtExposure'].map(col_BsmtExposure).fillna(4)
    
    col_BsmtQual = {'TA': 1, 'Fa': 1, 'Gd': 2, 'Ex': 3}
    train_X['BsmtQual'] = train_X['BsmtQual'].map(col_BsmtQual).fillna(1)
    test_X['BsmtQual'] = test_X['BsmtQual'].map(col_BsmtQual).fillna(1)
    
    train_X['Exterior1st'] = train_X['Exterior1st'].apply(lambda x: x if x in ['VinylSd','MetalSd','Wd Sdng','HdBoard','Plywood','Stucco'] else 'others')
    test_X['Exterior1st'] = test_X['Exterior1st'].apply(lambda x: x if x in ['VinylSd','MetalSd','Wd Sdng','HdBoard','Plywood','Stucco'] else 'others')
    col_Exterior1st = {'VinylSd': 1, 'MetalSd': 2, 'Wd Sdng': 2, 'HdBoard': 2, 'Plywood': 2, 'Stucco': 2, 'others': 3}
    train_X['Exterior1st'] = train_X['Exterior1st'].map(col_Exterior1st).fillna(1)
    test_X['Exterior1st'] = test_X['Exterior1st'].map(col_Exterior1st).fillna(1)
    
    train_X['Exterior2nd'] = train_X['Exterior2nd'].apply(lambda x: x if x in ['VinylSd','MetalSd','HdBoard','Wd Sdng','Plywood'] else 'others')
    test_X['Exterior2nd'] = test_X['Exterior2nd'].apply(lambda x: x if x in ['VinylSd','MetalSd','HdBoard','Wd Sdng','Plywood'] else 'others')
    col_Exterior2nd = {'VinylSd': 1, 'MetalSd': 2, 'HdBoard': 3, 'Wd Sdng': 4, 'Plywood': 5, 'others': 6}
    train_X['Exterior2nd'] = train_X['Exterior2nd'].map(col_Exterior2nd)
    test_X['Exterior2nd'] = test_X['Exterior2nd'].map(col_Exterior2nd)
    
    train_X['ExterQual'] = train_X['ExterQual'].apply(lambda x: x if x in ['TA','Gd'] else 'others')
    test_X['ExterQual'] = test_X['ExterQual'].apply(lambda x: x if x in ['TA','Gd'] else 'others')
    col_ExterQual = {'TA': 1, 'Gd': 2, 'others': 3}
    train_X['ExterQual'] = train_X['ExterQual'].map(col_ExterQual)
    test_X['ExterQual'] = test_X['ExterQual'].map(col_ExterQual)
    
    train_X['Foundation'] = train_X['Foundation'].apply(lambda x: x if x in ['PConc','CBlock','BrkTil'] else 'others')
    test_X['Foundation'] = test_X['Foundation'].apply(lambda x: x if x in ['PConc','CBlock','BrkTil'] else 'others')
    col_Foundation = {'PConc': 1, 'CBlock': 2, 'BrkTil': 3, 'others': 4}
    train_X['Foundation'] = train_X['Foundation'].map(col_Foundation)
    test_X['Foundation'] = test_X['Foundation'].map(col_Foundation)
    
    train_X['GarageFinish'] = train_X['GarageFinish'].fillna('others')
    test_X['GarageFinish'] = test_X['GarageFinish'].fillna('others')
    col_GarageFinish = {'Unf': 1, 'RFn': 2, 'Fin': 3, 'others': 4}
    train_X['GarageFinish'] = train_X['GarageFinish'].map(col_GarageFinish)
    test_X['GarageFinish'] = test_X['GarageFinish'].map(col_GarageFinish)
    
    train_X['GarageType'] = train_X['GarageType'].apply(lambda x: x if x in ['Attchd','Detchd'] else 'others')
    test_X['GarageType'] = test_X['GarageType'].apply(lambda x: x if x in ['Attchd','Detchd'] else 'others')
    col_GarageType = {'Attchd': 1, 'Detchd': 2, 'others': 3}
    train_X['GarageType'] = train_X['GarageType'].map(col_GarageType)
    test_X['GarageType'] = test_X['GarageType'].map(col_GarageType)
    
    train_X['HeatingQC'] = train_X['HeatingQC'].apply(lambda x: x if x in ['Ex','TA','Gd'] else 'others')
    test_X['HeatingQC'] = test_X['HeatingQC'].apply(lambda x: x if x in ['Ex','TA','Gd'] else 'others')
    col_HeatingQC = {'Ex': 1, 'TA': 2, 'Gd': 3, 'others': 4}
    train_X['HeatingQC'] = train_X['HeatingQC'].map(col_HeatingQC)
    test_X['HeatingQC'] = test_X['HeatingQC'].map(col_HeatingQC)
    
    train_X['HouseStyle'] = train_X['HouseStyle'].apply(lambda x: x if x in ['1Story','2Story','1.5Fin'] else 'others')
    test_X['HouseStyle'] = test_X['HouseStyle'].apply(lambda x: x if x in ['1Story','2Story','1.5Fin'] else 'others')
    col_HouseStyle = {'1Story': 1, '2Story': 2, '1.5Fin': 3, 'others': 4}
    train_X['HouseStyle'] = train_X['HouseStyle'].map(col_HouseStyle)
    test_X['HouseStyle'] = test_X['HouseStyle'].map(col_HouseStyle)
    
    train_X['KitchenQual'] = train_X['KitchenQual'].apply(lambda x: x if x in ['TA','Gd','Ex'] else 'others')
    test_X['KitchenQual'] = test_X['KitchenQual'].apply(lambda x: x if x in ['TA','Gd','Ex'] else 'others')
    col_KitchenQual = {'TA': 1, 'Gd': 2, 'Ex': 3, 'others': 4}
    train_X['KitchenQual'] = train_X['KitchenQual'].map(col_KitchenQual)
    test_X['KitchenQual'] = test_X['KitchenQual'].map(col_KitchenQual)
    
    train_X = train_X.drop(columns=['LandSlope'])
    test_X = test_X.drop(columns=['LandSlope'])
    
    train_X['LotConfig'] = train_X['LotConfig'].apply(lambda x: x if x in ['Inside','Corner'] else 'others')
    test_X['LotConfig'] = test_X['LotConfig'].apply(lambda x: x if x in ['Inside','Corner'] else 'others')
    col_LotConfig = {'Inside': 1, 'Corner': 2, 'others': 3}
    train_X['LotConfig'] = train_X['LotConfig'].map(col_LotConfig)
    test_X['LotConfig'] = test_X['LotConfig'].map(col_LotConfig)
    
    train_X['LotShape'] = train_X['LotShape'].apply(lambda x: x if x in ['Reg','IR1'] else 'others')
    test_X['LotShape'] = test_X['LotShape'].apply(lambda x: x if x in ['Reg','IR1'] else 'others')
    col_LotShape = {'Reg': 1, 'IR1': 2, 'others': 3}
    train_X['LotShape'] = train_X['LotShape'].map(col_LotShape)
    test_X['LotShape'] = test_X['LotShape'].map(col_LotShape)
    
    train_X['MSZoning'] = train_X['MSZoning'].apply(lambda x: x if x in ['RL','RM'] else 'others')
    test_X['MSZoning'] = test_X['MSZoning'].apply(lambda x: x if x in ['RL','RM'] else 'others')
    col_MSZoning = {'RL': 1, 'RM': 2, 'others': 3}
    train_X['MSZoning'] = train_X['MSZoning'].map(col_MSZoning)
    test_X['MSZoning'] = test_X['MSZoning'].map(col_MSZoning)
    
    # Neighborhood - Target Encoding
    low_freq = train_X['Neighborhood'].value_counts()[train_X['Neighborhood'].value_counts() < 20].index
    train_X['Neighborhood'] = train_X['Neighborhood'].replace(low_freq, 'Other')
    low_freq1 = test_X['Neighborhood'].value_counts()[test_X['Neighborhood'].value_counts() < 20].index
    test_X['Neighborhood'] = test_X['Neighborhood'].replace(low_freq1, 'Other')
    
    te = TargetEncoder(cols=['Neighborhood'])
    train_X['Neighborhood'] = te.fit_transform(train_X['Neighborhood'], train_X[target_col])
    test_X['Neighborhood'] = te.transform(test_X['Neighborhood'])
    
    scaler_neighborhood = StandardScaler()
    train_X['Neighborhood'] = scaler_neighborhood.fit_transform(train_X[['Neighborhood']])
    test_X['Neighborhood'] = scaler_neighborhood.transform(test_X[['Neighborhood']])
    
    train_X['RoofStyle'] = train_X['RoofStyle'].apply(lambda x: x if x in ['Gable','Hip'] else 'others')
    test_X['RoofStyle'] = test_X['RoofStyle'].apply(lambda x: x if x in ['Gable','Hip'] else 'others')
    col_RoofStyle = {'Gable': 1, 'Hip': 2, 'others': 3}
    train_X['RoofStyle'] = train_X['RoofStyle'].map(col_RoofStyle)
    test_X['RoofStyle'] = test_X['RoofStyle'].map(col_RoofStyle)
    
    train_X['SaleCondition'] = train_X['SaleCondition'].apply(lambda x: x if x in ['Normal','Partial','Abnorml'] else 'others')
    test_X['SaleCondition'] = test_X['SaleCondition'].apply(lambda x: x if x in ['Normal','Partial','Abnorml'] else 'others')
    col_SaleCondition = {'Normal': 1, 'Partial': 2, 'Abnorml': 3, 'others': 4}
    train_X['SaleCondition'] = train_X['SaleCondition'].map(col_SaleCondition)
    test_X['SaleCondition'] = test_X['SaleCondition'].map(col_SaleCondition)
    
    # Feature Engineering
    train_X['HouseAge'] = train_X['YrSold'] - train_X['YearBuilt']
    test_X['HouseAge'] = test_X['YrSold'] - test_X['YearBuilt']
    scaler_age = StandardScaler()
    train_X['HouseAge'] = scaler_age.fit_transform(train_X[['HouseAge']])
    test_X['HouseAge'] = scaler_age.transform(test_X[['HouseAge']])
    
    train_X['IsRemodeled'] = (train_X['YearRemodAdd'] != train_X['YearBuilt']).astype(int)
    test_X['IsRemodeled'] = (test_X['YearRemodAdd'] != test_X['YearBuilt']).astype(int)
    
    scaler_bsmt = StandardScaler()
    train_X['TotalBsmtSF'] = scaler_bsmt.fit_transform(train_X[['TotalBsmtSF']])
    test_X['TotalBsmtSF'] = scaler_bsmt.transform(test_X[['TotalBsmtSF']])
    
    scaler_1st = StandardScaler()
    train_X['1stFlrSF'] = scaler_1st.fit_transform(train_X[['1stFlrSF']])
    test_X['1stFlrSF'] = scaler_1st.transform(test_X[['1stFlrSF']])
    
    scaler_grliv = StandardScaler()
    train_X['GrLivArea'] = scaler_grliv.fit_transform(train_X[['GrLivArea']])
    test_X['GrLivArea'] = scaler_grliv.transform(test_X[['GrLivArea']])
    
    train_X['Has3FullBath'] = (train_X['FullBath'] >= 3).astype(int)
    test_X['Has3FullBath'] = (test_X['FullBath'] >= 3).astype(int)
    
    bins = [0, 4, 7, 100]
    labels = ['small', 'medium', 'large']
    train_X['TotRms_group'] = pd.cut(train_X['TotRmsAbvGrd'], bins=bins, labels=labels)
    test_X['TotRms_group'] = pd.cut(test_X['TotRmsAbvGrd'], bins=bins, labels=labels)
    
    train_X = pd.get_dummies(train_X, columns=['TotRms_group'], drop_first=True)
    test_X = pd.get_dummies(test_X, columns=['TotRms_group'], drop_first=True)
    
    dummy_cols = [c for c in train_X.columns if 'TotRms_group' in c]
    train_X[dummy_cols] = train_X[dummy_cols].astype(int)
    test_X[dummy_cols] = test_X[dummy_cols].astype(int)
    
    train_X['has3Garage'] = (train_X['GarageCars'] == 3).astype(int)
    test_X['has3Garage'] = (test_X['GarageCars'] == 3).astype(int)
    
    train_X['GarageArea_per_car'] = (train_X['GarageArea'] / (train_X['GarageCars'] + 1))
    test_X['GarageArea_per_car'] = (test_X['GarageArea'] / (test_X['GarageCars'] + 1))
    
    scaler_garage = StandardScaler()
    train_X[['GarageArea', 'GarageArea_per_car']] = scaler_garage.fit_transform(train_X[['GarageArea', 'GarageArea_per_car']])
    test_X[['GarageArea', 'GarageArea_per_car']] = scaler_garage.transform(test_X[['GarageArea', 'GarageArea_per_car']])
    
    drop_cols = ['YearBuilt', 'YrSold', 'YearRemodAdd', 'TotRmsAbvGrd']
    train_X = train_X.drop(columns=drop_cols)
    test_X = test_X.drop(columns=drop_cols)
    
    return train_X, test_X

# ===== 3. APPLY FEATURE ENGINEERING =====
print("\n🔧 Applying feature engineering...")
train_X_fixed, test_X_fixed = feature_engineering(train_data, test_data, target_col='SalePrice')

print(f"✅ Train shape after FE: {train_X_fixed.shape}")
print(f"✅ Test shape after FE: {test_X_fixed.shape}")

# ===== 4. PREPARE DATA FOR TRAINING =====
X_train = train_X_fixed.drop(columns=['SalePrice'])
y_train_log = np.log1p(train_data['SalePrice'])

print(f"\n📊 Final training data shape: {X_train.shape}")
print(f"📊 Features: {X_train.columns.tolist()}")

# ===== 5. TRAIN MODELS =====
print("\n🤖 Training XGBoost model...")
xgb = XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    tree_method="hist"
)
xgb.fit(X_train, y_train_log)

print("✅ Training completed!")

# ===== 6. PREDICT & CREATE SUBMISSION =====
print("\n🔮 Making predictions...")
xgb_pred_log = xgb.predict(test_X_fixed)
xgb_pred = np.expm1(xgb_pred_log)

submission = pd.DataFrame({
    "Id": test_data["Id"],
    "SalePrice": xgb_pred
})

submission.to_csv("submission_final.csv", index=False)

print("\n✅ DONE! Created 'submission_final.csv'")
print(f"\n📈 Prediction stats:")
print(f"   Min: ${xgb_pred.min():,.0f}")
print(f"   Max: ${xgb_pred.max():,.0f}")
print(f"   Mean: ${xgb_pred.mean():,.0f}")
print(f"   Median: ${np.median(xgb_pred):,.0f}")
