import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier  # You can choose any model you prefer

# Load your dataset
data = pd.read_csv('C:\\Users\\HM\\Desktop\\WeboMizer\\Data\\your_dataset.csv')  # Adjust the path as necessary

# Check the structure of the data
print(data.columns)  # This will print the column names to help you debug

# Preprocess data
# Assuming you have a 'Services' column for text data and a 'Industry' column for categories
X = data['Services']  # Text data
y = data['Industry']  # Corresponding categories

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorize the text data
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train the model
model = RandomForestClassifier()  # You can use other models like LogisticRegression, etc.
model.fit(X_train_vec, y_train)

# Save the model and vectorizer
joblib.dump(model, 'model/model.joblib')
joblib.dump(vectorizer, 'model/vectorizer.joblib')

print("Model and vectorizer saved successfully.")
