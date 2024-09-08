# -*- coding: utf-8 -*-
"""Group_Project_Code_With Demo and Cost Matrix.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1y0SKVQKdIoZmCPpIYa3AHzo1utVpPPn4

# 1. Credit Risk Dataset

Dataset from Kaggle: https://www.kaggle.com/datasets/nanditapore/credit-risk-analysis/data

This is a credit risk analysis dataset we found on Kaggle. This dataset provides essential information about loan applicants and their characteristics, including their loan rate, income, age, credit length, etc.
This dataset provides a simplified view of the factors contributing to credit risk, presenting an excellent opportunity for us to apply our machine learning analysis in determining whether a loan applicant is likely to default.


Column Descriptions:
    
* ID: Unique identifier for each loan applicant.
* Age: Age of the loan applicant.
* Income: Income of the loan applicant.
* Home: Home ownership status (Own, Mortgage, Rent).
* Emp_Length: Employment length in years.
* Intent: Purpose of the loan (e.g., education, home improvement).
* Amount: Loan amount applied for.
* Rate: Interest rate on the loan.
* Status: Loan approval status (Fully Paid, Charged Off, Current).
* Percent_Income: Loan amount as a percentage of income.
* Default: Whether the applicant has defaulted on a loan previously (Yes, No).
* Cred_Length: Length of the applicant's credit history.

# 2. Loading Dataset
"""

import pandas as pd
import numpy as np

df = pd.read_csv("credit_risk.csv")

"""# 3. Dataset Summary"""

df.info()

df.describe()

df.head()

df.Status.value_counts()

"""# 4. Neccessary Data Preprocessing
These are the bare minimum data preprocessing requirements in order to run our benchmark models.

### Transforming categorical variables
"""

# We use pd.get_dummies function to transform our categorical columns using dummy variables

df_encoded = pd.get_dummies(df, columns=["Home", "Intent"], drop_first=True)
df_encoded['Default'] = [1 if i == "Y" else 0 for i in df['Default']]

df_encoded.head()

"""### Replacing missing values"""

df_encoded.isnull().sum()

#We use SimpleImputer to fill in the missing values with mean
from sklearn.impute import SimpleImputer

imputer = SimpleImputer(strategy='mean')
df_imputed = pd.DataFrame(imputer.fit_transform(df_encoded), columns=df_encoded.columns)

df_imputed.isnull().sum()

"""### Duplicate values"""

# There is no duplicates so no action needed here
df_imputed.duplicated().sum()

"""### Dropping Id column"""

# Id column does not provide any useful information so we drop it
# df_cleaned will be our initial model dataset from this point
df_cleaned = df_imputed.drop(["Id"], axis=1)

"""# 5. Data Visualization"""

# Commented out IPython magic to ensure Python compatibility.
# Importing our visualization packages
# %matplotlib inline
import matplotlib
import matplotlib.pyplot as plt

import seaborn as sns

import warnings
warnings.filterwarnings("ignore")

"""### Numerical Columns"""

fig, axes = plt.subplots(3, 2, figsize=(12, 10))

sns.boxplot(data = df, x="Default", y="Income", ax=axes[0,0])
axes[0,0].set_title("Default by Income")
axes[0,0].ticklabel_format(style='plain', axis='y')

sns.boxplot(data = df, x="Default", y="Age", ax=axes[0,1])
axes[0,1].set_title("Default by Age")

sns.boxplot(data = df, x="Default", y="Emp_length", ax=axes[1,1])
axes[1,1].set_title("Default by Employment Length")

sns.boxplot(data = df, x="Default", y="Rate", ax=axes[1,0])
axes[1,0].set_title("Default by Loan Rate")

sns.boxplot(data = df, x="Default", y="Amount", ax=axes[2,1])
axes[2,1].set_title("Default by Loan Amount")

sns.boxplot(data = df, x="Default", y="Cred_length", ax=axes[2,0])
axes[2,0].set_title("Default by Credit Length")

plt.tight_layout()

"""### Categorical columns"""

# We are using df because it contains the un-transformed categorical data
fig, axes = plt.subplots(4,1, figsize=(10,15))
sns.countplot(x=df["Home"], hue=df['Default'], ax=axes[0])
axes[0].set_title("Defaults by Home Category Countplot")

sns.countplot(x=df["Intent"], hue=df['Default'], ax=axes[1])
axes[1].set_title("Defaults by Intent Category Countplot")

sns.countplot(x=df["Status"], hue=df['Default'], ax=axes[2])
axes[2].set_title("Defaults by Status Category Countplot")

sns.countplot(x=df["Default"], ax=axes[3])
axes[3].set_title("Total Default Countplot")

plt.tight_layout()
plt.show()

"""### Visualization of our cleaned dataset"""

df_cleaned.hist(bins=50, figsize=(12,12))
plt.show()

"""### Target Feature Visualization"""

# Pie chart for Loan Default Status with a closer view
plt.figure(figsize=(6, 6))
df['Default'].value_counts().plot.pie(autopct='%1.1f%%', colors=['green', 'lightgreen'])

plt.title('Distribution of Default')
plt.ylabel('')  # To remove the 'Default' label on the y-axis
plt.show()

"""### Correlation of features"""

corr = df_encoded.corr()
plt.figure(figsize=(20, 15), dpi=200)
sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation of Variables')
plt.show()

"""# 6. Benchmark Models

We are running our model on the data with the minimum amount of pre-processing required, as we are unable to run the model without filling in missing values and transforming the categorical variables.

### Importing packages
"""

# Import necessary machine learning packages
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_curve,
    auc,
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

"""### Training and testing data"""

#Split data into x (features) and y (target)
X = df_cleaned.drop(columns=['Default'])
y = df_cleaned['Default']

# Create training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

"""# Benchmark 1: Random Forest Classifier

### Building the model
"""

# Fitting our Random Forest model on our training data
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# Getting our prediction
rf_pred = rf_model.predict(X_test)

"""### Classification report"""

# Classification report
print(f"Classification Report:\n{classification_report(y_test, rf_pred)}")
print(f"Accuracy: {accuracy_score(y_test, rf_pred)}")

"""### Confusion matrix"""

# Confusion matrix
ConfusionMatrixDisplay.from_predictions(y_test, rf_pred, cmap = plt.cm.Oranges, normalize = None, display_labels = ['0', '1'])

"""### Feature Importance"""

# Plot feature importances
rf_feature_importances = rf_model.feature_importances_
rf_feature_names = X.columns
sorted_idx = np.argsort(rf_feature_importances)

plt.figure(figsize=(10, 6))
plt.barh(range(len(sorted_idx)), rf_feature_importances[sorted_idx], align="center")
plt.yticks(range(len(sorted_idx)), [rf_feature_names[i] for i in sorted_idx])
plt.xlabel("Feature Importance")
plt.title("Benchmark Random Forest Feature Importances")
plt.tight_layout()
plt.show()

"""# Benchmark 2: Logistic Regression

### Building the model
"""

# Apply logistic regression model to training data
logreg_model = LogisticRegression(solver='liblinear', random_state=42)
logreg_model.fit(X_train, y_train)

# Getting our prediction
logreg_pred = logreg_model.predict(X_test)

"""### Classification report"""

# Classification report
print(f"Classification Report:\n{classification_report(y_test, logreg_pred)}")
print(f"Accuracy: {accuracy_score(y_test, logreg_pred)}")

"""### Confusion matrix"""

# Confusion matrix
ConfusionMatrixDisplay.from_predictions(y_test, logreg_pred, cmap = plt.cm.Oranges, normalize = None, display_labels = ['0', '1'])

"""# Benchmark 3: Naive Bayes

### Building the model
"""

from sklearn.naive_bayes import MultinomialNB
import matplotlib.pyplot as plt

# Build Naive Bayes Classifier model and fit to our training data
nb_model = MultinomialNB()
nb_model.fit(X_train, y_train)

# Getting our prediction
nb_pred = nb_model.predict(X_test)

"""### Classification report"""

print(f"Classification Report:\n{classification_report(y_test, nb_pred)}")
print(f"Accuracy: {accuracy_score(y_test, nb_pred)}")

"""### Confusion matrix"""

# Confusion matrix
ConfusionMatrixDisplay.from_predictions(y_test, nb_pred, cmap = plt.cm.Oranges, normalize = None, display_labels = ['0', '1'])

"""# Benchmark 4: XGBoost

### Building the model
"""

# Installing and importing xgboost
!pip install xgboost
import xgboost as xgb

# Fitting our model on our initial training data
xgb_model = xgb.XGBClassifier(random_state=42)
xgb_model.fit(X_train, y_train)

# Getting our predication
xgb_pred = xgb_model.predict(X_test)

"""### Confusion matrix"""

# Confusion matrix
ConfusionMatrixDisplay.from_predictions(y_test, xgb_pred, cmap = plt.cm.Oranges, normalize = None, display_labels = ['0', '1'])

"""### Classification report"""

print(f"Classification Report: \n{classification_report(y_test, xgb_pred)}")
print(f"Accuracy: {accuracy_score(y_test, xgb_pred)}")

"""## Models Performance Visualization

### AUROC graph
"""

pred1 = rf_model.predict_proba(X_test)
pred2 = logreg_model.predict_proba(X_test)
pred3 = nb_model.predict_proba(X_test)
pred4 = xgb_model.predict_proba(X_test)

#Plot AUC-ROC
false_positive_rate_1, true_positive_rate_1, thresholds_1 = roc_curve(y_test, pred1[:,1])
roc_auc_1 = auc(false_positive_rate_1, true_positive_rate_1)

false_positive_rate_2, true_positive_rate_2, thresholds_2 = roc_curve(y_test, pred2[:,1])
roc_auc_2 = auc(false_positive_rate_2, true_positive_rate_2)

false_positive_rate_3, true_positive_rate_3, thresholds_3 = roc_curve(y_test, pred3[:,1])
roc_auc_3 = auc(false_positive_rate_3, true_positive_rate_3)

false_positive_rate_4, true_positive_rate_4, thresholds_4 = roc_curve(y_test, pred4[:,1])
roc_auc_4 = auc(false_positive_rate_4, true_positive_rate_4)

plt.figure(figsize=(7,7))
plt.title('AUROC of Benchmark Models')
plt.plot(false_positive_rate_1, true_positive_rate_1, 'b', label = 'Random Forest'  % roc_auc_1)
plt.plot(false_positive_rate_2, true_positive_rate_2, 'y', label = 'Logit Model'  % roc_auc_2)
plt.plot(false_positive_rate_3, true_positive_rate_3, 'g', label = 'Naive Bayes'  % roc_auc_3)
plt.plot(false_positive_rate_4, true_positive_rate_4, 'orange', label = 'XGBoost'  % roc_auc_4)

plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()

"""# 7. Improving XGBoost Model

Since our XGBoost produced the best accuracy out of the 4 models we tried, we will proceed with improving our XGBoost model and turning it into a prediction model that can handle real-world inputs.

## XGBoost Model Result from Adjusting Class Weights, Resampling, and Scaling

### Adjusting class weights
"""

# This makes it so the "1" class is more weighted than the 0 since our model
# has trouble predicting the "1" class
scale_pos_weight = (len(y_train) - sum(y_train)) / sum(y_train)

"""### Resampling using SMOTE and scaling data"""

# Introduce new resampled training data
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

# Scale the data, including test data after resampling it to see if it further improves the model
scaler = StandardScaler()
X_resampled_scaled = scaler.fit_transform(X_resampled)
X_test_scaled = scaler.transform(X_test)

# Implementing our new model on the resampled and scaled data
new_xgb_model = xgb.XGBClassifier(scale_pos_weight=3, random_state=42)
new_xgb_model.fit(X_resampled_scaled, y_resampled)

# Getting our new prediction
new_xgb_pred = new_xgb_model.predict(X_test_scaled)

# Classification report
print(f"Classification Report: \n{classification_report(y_test, new_xgb_pred)}")
print(f"Accuracy: {accuracy_score(y_test, new_xgb_pred)}")
ConfusionMatrixDisplay.from_predictions(y_test, new_xgb_pred, cmap = plt.cm.Oranges, normalize = None, display_labels = ['0', '1'])

"""This is our adjusted model after addressing class imbalance issues. Because our positive class "1" is underrepresented, we increase the value of "scale_post_weight" to 3 from its default value of 1. As shown, we increased our predication accuracy of the "1" class.

## Cost Matrix Comparison of Models

### Cost Matrix Before Improvement
"""

avg_amount = df["Amount"].mean()
avg_rate = df["Rate"].mean()
fn_cost = avg_amount*(1+avg_rate*0.01)
fp_cost = avg_amount*(avg_rate*0.01)

conf_matrix = confusion_matrix(y_test, xgb_pred)

# Define the cost matrix based on your context
cost_matrix = [[0, fp_cost],
               [fn_cost, 0]]

# Calculate the cost for each element in the confusion matrix
costs = [[conf_matrix[i][j] * cost_matrix[i][j] for j in range(2)] for i in range(2)]

plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=costs, fmt=',.0f', cmap='Oranges', annot_kws={'size': 14})
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix with Costs')
plt.show()

costs = np.array([[conf_matrix[i][j] * cost_matrix[i][j] for j in range(2)] for i in range(2)])

# Calculate the total cost
total_cost = costs.sum()
print("Total Costs:", f"${total_cost:,.0f}")

"""### Cost Matrix After Improvement"""

conf_matrix = confusion_matrix(y_test, new_xgb_pred)

# Define the cost matrix based on your context
cost_matrix = [[0, fp_cost],
               [fn_cost, 0]]

# Calculate the cost for each element in the confusion matrix
costs = [[conf_matrix[i][j] * cost_matrix[i][j] for j in range(2)] for i in range(2)]

plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=costs, fmt=',.0f', cmap='Oranges', annot_kws={'size': 14})
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix with Costs')
plt.show()

costs = np.array([[conf_matrix[i][j] * cost_matrix[i][j] for j in range(2)] for i in range(2)])

# Calculate the total cost
total_cost = costs.sum()
print("Total Costs:", f"${total_cost:,.0f}")

"""# 8. Conclusion

After implementing several improvement methods, such as SMOTE, standardizing, and parameter tuning, we were able to increase the overall accuracy of our model and decrease the amount of false negative predictions. This can be beneficial because falsely predicting "not default" can be more costly than predicting "yes default." In the case of a False Negative prediction, we simplified the costs to be the average amount of the loan plus its interest in one year. In the case of a False Positive prediction, we simplified the costs to be the lender losing out on one year's worth of interest on the average loan amount. As shown in our cost matrix comparison, by minimizing our False Negative predictions, we were able to drastically reduce our potential costs by $5 million.

# 9. Demo
Below is our final prediction model that will take a set of values based off our dataset and generate the probability of default.
"""

# Import necessary libraries
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, KBinsDiscretizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report, accuracy_score, ConfusionMatrixDisplay
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt

# Load the data
file_path = 'credit_risk.csv'
credit_data = pd.read_csv(file_path)

# Convert 'Default' column to binary format
credit_data['Default'] = credit_data['Default'].map({'Y': 1, 'N': 0})

# Impute missing values in 'Rate' column
rate_imputer = SimpleImputer(strategy='median')
credit_data['Rate'] = rate_imputer.fit_transform(credit_data[['Rate']])

# Transform interest rate into categorical bins
bins = KBinsDiscretizer(n_bins=3, encode='ordinal', strategy='quantile')
credit_data['Rate'] = bins.fit_transform(credit_data[['Rate']])

# Define categorical and numerical features (excluding removed columns)
categorical_features = ['Home', 'Rate']  # 'Rate' is now categorical
numerical_features = ['Age', 'Income', 'Emp_length', 'Amount']

# Preprocessing pipeline
numerical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_pipeline, numerical_features),
        ('cat', categorical_pipeline, categorical_features)
    ])

# Split the data
X = credit_data.drop(['Default', 'Intent', 'Status', 'Percent_income', 'Cred_length'], axis=1)
y = credit_data['Default']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Apply preprocessing to the training and test data
X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)

# Resampling with SMOTE on the processed training data
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train_processed, y_train)

# Train the XGBoost model on the resampled data
scale_pos_weight = (len(y_train) - sum(y_train)) / sum(y_train)
new_xgb_model = xgb.XGBClassifier(scale_pos_weight=3, random_state=42)
new_xgb_model.fit(X_resampled, y_resampled)

# Classification report on the processed test data
new_xgb_pred = new_xgb_model.predict(X_test_processed)

# Function for prediction
def predict_default(input_data):
    # Apply the same imputation and binning to input rate
    input_data['Rate'] = rate_imputer.transform([[input_data['Rate']]])[0, 0]
    input_data['Rate'] = bins.transform([[input_data['Rate']]])[0, 0]
    input_df = pd.DataFrame([input_data])
    processed_input = preprocessor.transform(input_df)
    probability_of_default = new_xgb_model.predict_proba(processed_input)[0][1]
    return probability_of_default

# Collecting all inputs in a single cell
print("Enter the following details:")
age = input("Age: ")
income = input("Income: ")
home = input("Home (RENT/OWN/MORTGAGE/OTHER): ")
emp_length = input("Employment Length (in years): ")
amount = input("Loan Amount: ")
rate = float(input("Interest Rate: "))

input_data = {
    'Age': int(age),
    'Income': int(income),
    'Home': home,
    'Emp_length': float(emp_length),
    'Amount': int(amount),
   'Rate': rate
}

# Displaying the probability of default
probability = predict_default(input_data)
print("\nProbability of Default: ", probability)

