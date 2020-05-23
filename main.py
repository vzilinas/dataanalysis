import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
import matplotlib.pyplot as plt
from matplotlib import rcParams
from sklearn_pandas import DataFrameMapper
import seaborn as sns
from sklearn.decomposition import PCA

scl_names = ["Revenue", "Expenses", "Profit", "Growth", "Employees"]
cat_names = ["Industry", "State"]
rcParams.update({'figure.autolayout': True})

# Reading
data = pd.read_csv("data.csv")
print(data.describe(include='all'))

# Converting to categorical data
data['Industry'] = data['Industry'].astype('category')
data['Name'] = data['Name'].astype('category')
data['Inception'] = data['Inception'].astype('category')
data['State'] = data['State'].astype('category')
data['City'] = data['City'].astype('category')
data['ID'] = data['ID'].astype('category')

# Cleaning Expenses
data['Expenses'] = data['Expenses'].str.replace("Dollars", "")
data['Expenses'] = data['Expenses'].str.replace(",", "")
data['Expenses'] = pd.to_numeric(
    data['Expenses'], errors='coerce', downcast='float')
# Cleaning Revenue
data['Revenue'] = data['Revenue'].str.replace("$", "")
data['Revenue'] = data['Revenue'].str.replace(",", "")
data['Revenue'] = pd.to_numeric(
    data['Revenue'], errors='coerce', downcast='float')

# Cleaning Growth
data['Growth'] = data['Growth'].str.replace("%", "")
data['Growth'] = pd.to_numeric(
    data['Growth'], errors='coerce', downcast='float') / 100

# Cleaning Profit
data['Profit'] = pd.to_numeric(
    data['Profit'], errors='coerce', downcast='float')

# Cleaning Employees
data['Employees'] = pd.to_numeric(
    data['Employees'], errors='coerce', downcast='float')

# Filling Revenue and Employees using median
data['Revenue'].fillna(data.groupby('Industry')[
                       'Revenue'].transform('median'), inplace=True)
data['Employees'].fillna(data.groupby('Industry')[
                         'Employees'].transform('median'), inplace=True)

# Filling Expenses, Profit using forumlas
data['Expenses'] = data['Expenses'].fillna(data['Revenue'] - data['Profit'])
data['Profit'] = data['Profit'].fillna(data['Revenue'] - data['Expenses'])

# Removing that which we could not fill using formulas
data = data[data['Revenue'].notna() & data['Expenses'].notna()
            & data['Profit'].notna() & data['Industry'].notna()]

# Assuming that missing growth is 0
data['Growth'] = data['Growth'].fillna(value=0)

print("\nTotal\n")

# Results with outliers
print(data.describe())


print("\nRemove outliers\n")
# Result without outliers

q_low = data["Revenue"].quantile(0.25)
q_hi = data["Revenue"].quantile(0.75)
q_dif = 3 * (q_hi - q_low)
df_filtered = data[(data["Revenue"] > (q_low - q_dif)) &
                   (data["Revenue"] < (q_hi + q_dif))]

s1 = pd.merge(data, df_filtered, how='inner')
print("\nRemove Revenue outliers\n")
print(df_filtered.describe())

q_low = data["Expenses"].quantile(0.25)
q_hi = data["Expenses"].quantile(0.75)
q_dif = 3 * (q_hi - q_low)
df_filtered = data[(data["Expenses"] > (q_low - q_dif)) &
                   (data["Expenses"] < (q_hi + q_dif))]

s1 = pd.merge(s1, df_filtered, how='inner')
print("\nRemove Expenses outliers\n")
print(df_filtered.describe())

q_low = data["Profit"].quantile(0.25)
q_hi = data["Profit"].quantile(0.75)
q_dif = 3 * (q_hi - q_low)
df_filtered = data[(data["Profit"] > (q_low - q_dif)) &
                   (data["Profit"] < (q_hi + q_dif))]

s1 = pd.merge(s1, df_filtered, how='inner')
print("\nRemove Profit outliers\n")
print(df_filtered.describe())

q_low = data["Growth"].quantile(0.25)
q_hi = data["Growth"].quantile(0.75)
q_dif = 3 * (q_hi - q_low)
df_filtered = data[(data["Growth"] > (q_low - q_dif)) &
                   (data["Growth"] < (q_hi + q_dif))]

s1 = pd.merge(s1, df_filtered, how='inner')
print("\nRemove Growth outliers\n")
print(df_filtered.describe())

q_low = data["Employees"].quantile(0.25)
q_hi = data["Employees"].quantile(0.75)
q_dif = 3 * (q_hi - q_low)
df_filtered = data[(data["Employees"] > (q_low - q_dif)) &
                   (data["Employees"] < (q_hi + q_dif))]

s1 = pd.merge(s1, df_filtered, how='inner')
print("\nRemove Employees outliers\n")
print(df_filtered.describe())


print("\nRemove All of the above outliers\n")
print(s1.describe())


# MinMax scaling
scaler = MinMaxScaler()
minmax_scaled = s1.copy()
minmax_scaled[["Revenue", "Expenses", "Profit", "Growth", "Employees"]] = scaler.fit_transform(
    s1[["Revenue", "Expenses", "Profit", "Growth", "Employees"]])

print("\nMin Max scaled\n")
print(minmax_scaled.describe())


# Standard scaling

x = s1.loc[:, scl_names].values
x = StandardScaler().fit_transform(x)  # normalizing the features

act_data = s1[["Revenue", "Expenses", "Profit", "Growth", "Employees"]]
mapper = DataFrameMapper([(act_data.columns, StandardScaler())])
scaled_features = mapper.fit_transform(act_data.copy(), 4)
scaled_features_df = pd.DataFrame(scaled_features, index=act_data.index, columns=act_data.columns)
std_scaled = s1.copy()
std_scaled[["Revenue", "Expenses", "Profit", "Growth", "Employees"]] = scaled_features_df[["Revenue", "Expenses", "Profit", "Growth", "Employees"]]

print("\nStandard scaled\n")
print(std_scaled.describe())

# PCA
# pca = PCA(n_components=2)
# principalComponents = pca.fit_transform(x)
# principal_Df = pd.DataFrame(data=principalComponents, columns=['principal component 1', 'principal component 2'])
# plt.scatter(principal_Df['principal component 1'], principal_Df['principal component 2'])
# plt.title('PCA')
# plt.savefig('gfx/pca/Scaled_pca.png')
# plt.clf()

# Correlation

print("\nCorrelation\n")
print(minmax_scaled.corr(method='pearson'))

# #Bar charts
# for cat in cat_names:
#     for name in scl_names:
#         plt.bar(minmax_scaled[cat], minmax_scaled[name])
#         plt.title(f'{cat}/{name}')
#         plt.xticks(rotation=90)
#         plt.savefig(f'gfx/bar/MinMax_{cat}_{name}.png')
#         plt.clf()

# for cat in cat_names:
#     for name in scl_names:
#         plt.bar(std_scaled[cat], std_scaled[name])
#         plt.title(f'{cat}/{name}')
#         plt.xticks(rotation=90)
#         plt.savefig(f'gfx/bar/Scaled_{cat}_{name}.png')
#         plt.clf()

# #Scatter charts
# for cat in scl_names:
#     for name in scl_names:
#         plt.scatter(s1[cat], s1[name])
#         plt.title(f'{cat}/{name}')
#         plt.xticks(rotation=90)
#         plt.savefig(f'gfx/scatter/General_{cat}_{name}.png')
#         plt.clf()

# #Frequency charts
# for cat in cat_names:
#     plt.bar(s1[cat].value_counts().index, s1[cat].value_counts())
#     plt.title(f'{cat} frequency')
#     plt.xticks(rotation=90)
#     plt.savefig(f'gfx/frequency/General_{cat}.png')
#     plt.clf()

# #Colorful scatter
# sns.pairplot(x_vars=["Revenue"], y_vars=["Profit"], data=s1, hue="Industry", height=5)
# plt.tight_layout()
# plt.show()


# df_scaled['Growth'].plot()
