import joblib

# Load the trained model and vectorizer
model = joblib.load('model/model.joblib')
vectorizer = joblib.load('model/vectorizer.joblib')

def predict_service_category(service_description):
    # Transform the input service description
    service_vec = vectorizer.transform([service_description])
    predicted_category = model.predict(service_vec)
    predicted_probabilities = model.predict_proba(service_vec)

    return predicted_category[0], predicted_probabilities

if __name__ == "__main__":
    new_service = "plumbing"
    category, probabilities = predict_service_category(new_service)
    print(f"The predicted category for the service '{new_service}' is: {category}")
    print(f"Probabilities: {probabilities}")
