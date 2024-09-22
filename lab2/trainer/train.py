from os import getcwd
from os.path import exists, join

import joblib
from sklearn.datasets import fetch_california_housing
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.svm import SVR

# Fetch the California housing dataset
data = fetch_california_housing()

# Extract feature names and data
features = data.feature_names
X = data.data
y = data.target

# Print feature names
print(f"features: {features}")

# Print first 5 examples of the dataset
for i in range(5):
    print(f"Example {i}:\n {X[i]}, {y[i]}")

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42
)

# Get the number of samples and features
n_samples, n_features = X.shape

# Create a pipeline with imputation, scaling, and SVR model
processing_pipeline = make_pipeline(SimpleImputer(), RobustScaler(), SVR())

# Define hyperparameters for grid search
params = {
    "simpleimputer__strategy": ["mean", "median"],
    "robustscaler__quantile_range": [(25.0, 75.0), (30.0, 70.0)],
    "svr__C": [0.1, 1.0],
    "svr__gamma": ["auto", 0.1],
}

# Initialize GridSearchCV with the pipeline and hyperparameters
grid = GridSearchCV(processing_pipeline, param_grid=params, n_jobs=-1, cv=5, verbose=3)

# Define the path to save the trained model
model_filename = "model_pipeline.pkl"
model_path = join(getcwd(), model_filename)
print(model_path)

# Check if the model already exists
if not exists(model_path):
    # Fit the model using grid search
    grid.fit(X_train, y_train)

    # Print training and testing scores
    print(f"Train R^2 Score : {grid.best_estimator_.score(X_train, y_train):.3f}")
    print(f"Test R^2 Score : {grid.best_estimator_.score(X_test, y_test):.3f}")
    print(f"Best R^2 Score Through Grid Search : {grid.best_score_:.3f}")
    print(f"Best Parameters : {grid.best_params_}")

    # Save the best model to a file
    joblib.dump(grid.best_estimator_, model_path)
else:
    # If the model already exists, print a message
    print("Model has already been trained, no need to rerun")