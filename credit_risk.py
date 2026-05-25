#import  data manipulation libraries
import numpy as np
import pandas as pd
import joblib 

#import filter warning librar
import warnings
warnings.filterwarnings("ignore")

#customize descriptive stats
from collections import OrderedDict

#converting data into numeric
from sklearn.preprocessing import OneHotEncoder,LabelEncoder,StandardScaler

#import data visulization library
import matplotlib.pyplot as plt
import seaborn as sns
#split data
from sklearn.model_selection import train_test_split
#model traing
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
df = pd.read_csv("german_credit_data.csv")
df = df.drop(columns=['Unnamed: 0'])
df.sample(20)
# Shape of dataset
print(df.shape)
# understand the dataset
df.info()
# checking missing value
df.isnull().sum()
# filling missing value
cat_cols = ['Saving accounts', 'Checking account']
df[cat_cols]= df[cat_cols].fillna('Unkwn')
df.sample(8)
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
le_array = le.fit_transform(df["Sex"])
df["Sex"]= pd.DataFrame(le_array)
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
le_array= le.fit_transform(df["Housing"])
df["Housing"]= pd.DataFrame(le_array)
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
le_array= le.fit_transform(df["Saving accounts"])
df["Saving accounts"]= pd.DataFrame(le_array)
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
le_array= le.fit_transform(df["Checking account"])
df["Checking account"]= pd.DataFrame(le_array)
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
le_array= le.fit_transform(df["Purpose"])
df["Purpose"]= pd.DataFrame(le_array)
df_numeric = df.drop(columns=['Purpose'])
# statistic
from collections import OrderedDict
numeric_cols = df.select_dtypes(include=['number']).columns

stats = []
for i in numeric_cols:
  numerical_stats = OrderedDict({
      "Feature": i,
      "max": df[i].max(),
      "mean": df[i].mean(),
      "median": df[i].median(),
      "standard deviation": df[i].std(),
      "variance": df[i].var(),
      "skewness": df[i].skew(),
      "kurtosis": df[i].kurt(),
      "25%": df[i].quantile(0.25),
      "75%": df[i].quantile(0.75),
      "IQR": df[i].quantile(0.75) - df[i].quantile(0.25)
    })
stats.append(numerical_stats)

# Create DataFrame report
report = pd.DataFrame(stats)
print(report.T)
numeric_cols = df.select_dtypes(include =['number']).columns

plt.figure(figsize=(15,15))
plot= 0
for col in numeric_cols:
  plot += 1
  plt.subplot(4, 3, plot) # Adjusted subplot grid to 4x3
  sns.histplot(df[col], kde=True)
  plt.title(col)

plt.tight_layout()
plt.show()
numeric_cols = df.select_dtypes(include=['number']).columns
plt.figure(figsize=(15,15))
plot = 0
for col in numeric_cols:
  plot += 1
  plt.subplot(4, 3, plot)
  sns.boxenplot(x = df[col])
  plt.title(col)

  plt.tight_layout()
  plt.show()
  def remove_outliers(df, column, threshold=1.5):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

for col in ["Age", "Credit amount", "Duration"]:
  df = remove_outliers(df, col) 
  # Define Features (X) and Target (y)
# Let's assume credit worthiness = "Good" if Credit amount < 4000 else "Bad"
# (since dataset does not have explicit target column for CIBIL or default)
df['Credit_Worthiness'] = np.where(df['Credit amount'] < 4000, 1, 0)

X = df.drop(columns=['Credit_Worthiness'])
Y = df['Credit_Worthiness']
# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X_scaled, Y, test_size= 0.3, random_state=42)
# Create and train model
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
# Logistic Regression Model
log_reg = LogisticRegression(max_iter=1000)
log_reg.fit(X_train, y_train)
y_pred_log = log_reg.predict(X_test)
dtree = DecisionTreeClassifier(max_depth=5, random_state=42)
dtree.fit(X_train, y_train)
y_pred_tree = dtree.predict(X_test)
print("code run successfully")
joblib.dump(dtree, "decision_tree_model.pkl")
joblib.dump(log_reg, "log_reg_model.pkl")
joblib.dump(scaler, "scaler.pkl")
print ("runs success")

# Evaluation
print("📌 Logistic Regression Results")
print("Accuracy:", accuracy_score(y_test, y_pred_log))
print(confusion_matrix(y_test, y_pred_log))
print(classification_report(y_test, y_pred_log))

print("\n📌 Decision Tree Results")
print("Accuracy:", accuracy_score(y_test, y_pred_tree))
print(confusion_matrix(y_test, y_pred_tree))
print(classification_report(y_test, y_pred_tree))

y_pred = model.predict(X_test)

comparison = pd.DataFrame({
    "Application_ID": range(len(y_test)),
    "Actual": y_test,
    "Predicted": y_pred
})

comparison["Eligibility"] = comparison["Predicted"].map({
    1 : "Eligible(Good Credit)",
    0 : "Not Eligible(Bad Credict)"
})

print(comparison.head(10))

