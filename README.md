# Loan Default Detection
This report is a coursework project that employs different algorithms to detect individual loan defaults. Curious about how lenders decide whether to approve loans, I chose this topic to leverage my knowledge and skills and explore this question through real-world applications.

# Introduction
- Datasource: https://www.kaggle.com/datasets/nanditapore/credit-risk-analysis/data
- Column Descriptions:
* ID: Unique identifier for each loan applicant.
* Age: Age of the loan applicant.
* Income: Income of the loan applicant.
* Home: Home ownership status (Own, Mortgage, Rent).
* Emp_Length: Employment length in years.
* Intent: Purpose of the loan (e.g., education, home improvement, medical, etc.).
* Amount: Loan amount applied for.
* Rate: Interest rate on the loan.
* Status: Loan approval status (Fully Paid, Charged Off, Current).
* Percent_Income: Loan amount as a percentage of income.
* Default: Whether the applicant has defaulted on a loan previously (Yes, No).
* Cred_Length: Length of the applicant's credit history.
<img width="816" alt="image" src="https://github.com/wenchitseng/loan_default_detection/assets/145182368/b7100421-f502-4b1d-9121-8d96c9b3e641">

# Data Transformation and Resampling
- I split data into 80% training (26,064) and 20% testing (6,517).
- Due to the high imbalance of default class, I used SMOTE to resample data in the training set to avoid bias toward the majority class.
<img width="874" alt="image" src="https://github.com/wenchitseng/loan_default_detection/assets/145182368/eaabe6d6-de18-45c8-8684-613fe06df78e">

# Trained Benchmark Models with Preprocessing
- Logistic Regression 
* Adding LASSO regularization to minimize the impact of variables that have little influence on the model.
<img width="563" alt="image" src="https://github.com/wenchitseng/loan_default_detection/assets/145182368/b6697ec8-9e92-4fae-b156-a06d9d197856">

- Random Forest
* Using GridSearch to find out the optimal parameters, including 'n_estimators', 'max_depth', 'min_samples_split', etc.
<img width="570" alt="image" src="https://github.com/wenchitseng/loan_default_detection/assets/145182368/e3b7ef69-0891-4c15-a62a-d52926d7cdb5">
  
- XGBoost
* Adding learning rate and max_depth. I did not adjust too many hyperparameters because I wanted to compare the difference between this model and the improved Random Forest model.
 <img width="563" alt="image" src="https://github.com/wenchitseng/loan_default_detection/assets/145182368/a4f882a9-3372-4e08-b497-b4ec736d3002">

<img width="500" alt="image" src="https://github.com/wenchitseng/loan_default_detection/assets/145182368/3000d17d-8f86-43c9-a650-34c2e2eab110"> <img width="500" alt="image" src="https://github.com/wenchitseng/loan_default_detection/assets/145182368/e76d0751-55c6-4a3a-bac1-3fe9ec53892b">

- Ensemble Model 
* Combined the 3 models above with the voting method.
<img width="581" alt="image" src="https://github.com/wenchitseng/loan_default_detection/assets/145182368/fa14c4ab-c45c-47cd-95bf-1a52749b29ff">

# Conclusion
<img width="933" alt="image" src="https://github.com/wenchitseng/loan_default_detection/assets/145182368/2d28f553-0cac-401c-988e-6f76a2b02ced">
If we only focus on testing accuracy, all five models perform similarly. However, in predicting loan defaults, it is more important to prioritize recall since the cost of missing an actual default is usually higher than the cost of incorrectly predicting a loan default.

XGBoost has the highest recall and F1 score. This is reasonable because logistic regression models the relationship between the features and the log odds of the target variable as a linear combination of features, limiting its performance when the relationship is not linear. This limitation is reflected in the table's low recall and F1-score of the logistic regression model. The Random Forest model, also based on decision trees, builds trees independently in parallel. However, XGBoost improves on this by boosting the training process to correct the errors of previous trees.

In conclusion, although building an ensemble model usually results in better performance than individual models, in this case, XGBoost outperforms the others and is likely the most suitable model. This practice leverages the knowledge and skills I acquired in the UCI BANA273 Machine Learning class, providing me with a more comprehensive understanding of real-world applications.






