import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load the dataset
data_path = r'D:\Desktop\New folder 001\SLIIT\Year 03\SEM 02\SSS\assignment\APP\ML-train\data.xlsx'
df = pd.read_excel(data_path)

# Handle NaN values in the target variable 'strength'
df.dropna(subset=['strength'], inplace=True)

# Preprocess the data (extract features)
df['password_length'] = df['password'].astype(str).apply(len)  # Convert to string before applying len()
df['has_numbers'] = df['password'].apply(lambda x: int(any(char.isdigit() for char in str(x))))  # 1 if has numbers, 0 otherwise
df['has_uppercase'] = df['password'].apply(lambda x: int(any(char.isupper() for char in str(x))))  # 1 if has uppercase, 0 otherwise

# Split the data into features (X) and target (y)
X = df[['password_length', 'has_numbers', 'has_uppercase']]
y = df['strength']

# Print unique values in the target variable
print("Unique values in y_train:", y.unique())

# Split the data into training and testing sets with a specific random state for reproducibility
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Random Forest model
model = RandomForestClassifier(random_state=42)  # Set random_state for reproducibility
print("Fitting the model...")
model.fit(X_train, y_train)

# Evaluate the model
accuracy = model.score(X_test, y_test)
print("Model Accuracy:", accuracy)

# Save the trained model
model_save_path = r'D:\Desktop\New folder 001\SLIIT\Year 03\SEM 02\SSS\assignment\APP\ML-train\trained_model\password_strength_model.pkl'
joblib.dump(model, model_save_path)
print("Model saved successfully at:", model_save_path)
