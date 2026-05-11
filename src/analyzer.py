import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import os

# Step 1 — Data Load
print("📊 Loading dataset...")
df = pd.read_csv('data/commits.csv')

# Step 2 — Features fix
df['file_type_code'] = df['file_types'].map({
    'md': 0, 'txt': 0, 'readme': 0,
    'py': 1, 'js': 1, 'yml': 1, 'css': 1
}).fillna(1)

X = df[['changed_files', 'file_type_code', 'lines_changed', 'has_code']]
y = df['label']

# Step 3 — Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Step 4 — Model Train
print("🧠 Training model...")
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Step 5 — Accuracy Check
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"✅ Model Accuracy: {accuracy * 100:.2f}%")

# Step 6 — Model Save
os.makedirs('model', exist_ok=True)
with open('model/autoskip_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("💾 Model saved to model/autoskip_model.pkl")