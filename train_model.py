
import pandas as pd
import joblib
import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load dataset
df = pd.read_csv("german_credit_data2.csv")

# Rename column
df.rename(columns={"Risk": "Creditworthy"}, inplace=True)
#df[["Saving accounts", "Checking account"]].isna().any(axis=1).sum()
# Replace values
df["Creditworthy"] = df["Creditworthy"].map({
    "good": 1,
    "bad": 0
})
df["Saving accounts"].fillna("unknown", inplace=True)
df["Checking account"].fillna("unknown", inplace=True)

# Save updated dataset
df.to_csv("updated_dataset.csv", index=False)

print("✅ Column renamed and values updated successfully!")

# Drop unnecessary column
if "Unnamed: 0" in df.columns:
    df.drop(columns=["Unnamed: 0"], inplace=True)


# Handle Missing Values

df["Saving accounts"].fillna("unknown", inplace=True)
df["Checking account"].fillna("unknown", inplace=True)

# Target & Features

X = df.drop(columns=["Creditworthy"])
y = df["Creditworthy"]


# =====================================
# Column Types
# =====================================
categorical_cols = [
    "Sex", "Housing", "Saving accounts",
    "Checking account", "Purpose"
]

numeric_cols = [
    "Age", "Credit amount", "Duration"
]

# Preprocessing

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", StandardScaler(), numeric_cols)
    ]
)

# Model

model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=500,
        max_depth=12,
        random_state=5
    ))
])


# Train-Test Split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.25,
    random_state=42,
    stratify=y
)


# Train Model

model.fit(X_train, y_train)

# =====================================
# Evaluation
# =====================================
y_pred = model.predict(X_test)

print("\n📊 MODEL PERFORMANCE")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))


# Save Model
joblib.dump(model, "credit_risk_model.pkl")

print("\n✅ Model saved as credit_risk_model.pkl")
