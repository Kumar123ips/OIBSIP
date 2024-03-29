# -*- coding: utf-8 -*-
"""OASISINFOBYTE.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18_YuQ-5IKKsuCSMtg3ADE7yGCb-0yddM

### *3. dea:  Autocomplete and Autocorrect Data Analytics *

Link: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

To address the problem of detecting fraudulent credit card transactions using the provided dataset, we can follow these steps:

1. Data Exploration: Understand the structure and characteristics of the dataset, including the distribution of the target variable ('Class') and the distribution of numerical features.

2. Data Preprocessing: Handle any missing values, scale numerical features if necessary, and split the dataset into training and testing sets.

3. Model Selection: Choose appropriate machine learning algorithms for binary classification tasks. Given the highly imbalanced nature of the dataset, consider using techniques such as oversampling, undersampling, or algorithmic approaches like Random Forest, Gradient Boosting, or XGBoost which handle class imbalance well.

4. Model Evaluation: Evaluate the selected models using appropriate evaluation metrics, such as AUPRC (Area Under the Precision-Recall Curve), ROC-AUC (Receiver Operating Characteristic Area Under the Curve), precision, recall, and F1-score.

5. Hyperparameter Tuning: Fine-tune the hyperparameters of the selected models using techniques like Grid Search or Random Search to improve their performance.

6. Model Interpretation: Interpret the trained models to understand which features contribute the most to the prediction of fraudulent transactions.

7. Deployment and Monitoring: Deploy the best-performing model into production and continuously monitor its performance to ensure it remains effective over time.
"""

from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
import numpy as np # linear algebra
import os # accessing directory structure
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

df = pd.read_csv("/content/creditcard.csv")

# Distribution graphs (histogram/bar graph) of column data
def plotPerColumnDistribution(df, nGraphShown, nGraphPerRow):
    nunique = df.nunique()
    df = df[[col for col in df if nunique[col] > 1 and nunique[col] < 50]] # For displaying purposes, pick columns that have between 1 and 50 unique values
    nRow, nCol = df.shape
    columnNames = list(df)
    nGraphRow = (nCol + nGraphPerRow - 1) / nGraphPerRow
    plt.figure(num = None, figsize = (6 * nGraphPerRow, 8 * nGraphRow), dpi = 80, facecolor = 'w', edgecolor = 'k')
    for i in range(min(nCol, nGraphShown)):
        plt.subplot(nGraphRow, nGraphPerRow, i + 1)
        columnDf = df.iloc[:, i]
        if (not np.issubdtype(type(columnDf.iloc[0]), np.number)):
            valueCounts = columnDf.value_counts()
            valueCounts.plot.bar()
        else:
            columnDf.hist()
        plt.ylabel('counts')
        plt.xticks(rotation = 90)
        plt.title(f'{columnNames[i]} (column {i})')
    plt.tight_layout(pad = 1.0, w_pad = 1.0, h_pad = 1.0)
    plt.show()

# Correlation matrix
def plotCorrelationMatrix(df, graphWidth):
    filename = df.dataframeName
    df = df.dropna('columns') # drop columns with NaN
    df = df[[col for col in df if df[col].nunique() > 1]] # keep columns where there are more than 1 unique values
    if df.shape[1] < 2:
        print(f'No correlation plots shown: The number of non-NaN or constant columns ({df.shape[1]}) is less than 2')
        return
    corr = df.corr()
    plt.figure(num=None, figsize=(graphWidth, graphWidth), dpi=80, facecolor='w', edgecolor='k')
    corrMat = plt.matshow(corr, fignum = 1)
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.gca().xaxis.tick_bottom()
    plt.colorbar(corrMat)
    plt.title(f'Correlation Matrix for {filename}', fontsize=15)
    plt.show()

# Scatter and density plots
def plotScatterMatrix(df, plotSize, textSize):
    df = df.select_dtypes(include =[np.number]) # keep only numerical columns
    # Remove rows and columns that would lead to df being singular
    df = df.dropna('columns')
    df = df[[col for col in df if df[col].nunique() > 1]] # keep columns where there are more than 1 unique values
    columnNames = list(df)
    if len(columnNames) > 10: # reduce the number of columns for matrix inversion of kernel density plots
        columnNames = columnNames[:10]
    df = df[columnNames]
    ax = pd.plotting.scatter_matrix(df, alpha=0.75, figsize=[plotSize, plotSize], diagonal='kde')
    corrs = df.corr().values
    for i, j in zip(*plt.np.triu_indices_from(ax, k = 1)):
        ax[i, j].annotate('Corr. coef = %.3f' % corrs[i, j], (0.8, 0.2), xycoords='axes fraction', ha='center', va='center', size=textSize)
    plt.suptitle('Scatter and Density Plot')
    plt.show()

nRowsRead = 1000 # specify 'None' if want to read whole file
# creditcard.csv has 284807 rows in reality, but we are only loading/previewing the first 1000 rows
df1 = pd.read_csv('/content/creditcard.csv')
df1.dataframeName = 'creditcard.csv'
nRow, nCol = df1.shape
print(f'There are {nRow} rows and {nCol} columns')

df1.head()

#print last 5 rows of the data
df.tail()

plotCorrelationMatrix(df1, 8)

plotScatterMatrix(df1, 20, 10)

#Get some information about dataset
df.info()

#Checking the number of missingvalues in each column
df.isnull().sum()

#Distribution of lgit transaction and fraudulent transaction
df["Class"].value_counts()

#Seprating the data for analysis
# 0 --> Normal Transection
# 1 --> Fraudlend Transection

legit = df[df.Class == 0]
fraud = df[df.Class == 1]

legit.shape

fraud.shape

legit

fraud

legit.Amount.describe()

fraud.Amount.describe()

#Compaire the values for both transactions
df.groupby("Class").mean()

# Under sampling
# Builed a sample dataset containing similar distribution of normal transaction and fraudlend transaction
# Number of Fraudlent Transaction --> 492

legit_sample = legit.sample(n = 492)

new_data = pd.concat([legit_sample,fraud],axis=0)

new_data.head(5)

new_data.shape

new_data["Class"].value_counts()

new_data.groupby("Class").mean()

X = new_data.drop(columns="Class",axis = 1)
X

y = new_data["Class"]
y

X_train,X_test,y_train,y_test = train_test_split(X,y,stratify=y,test_size=0.2,random_state=2)

print(X.shape,X_train.shape,X_test.shape)

model = LogisticRegression(max_iter=100000)

#Training the LogisticRegression model with training data

model.fit(X_train,y_train)

#Accuracy score on training data
X_train_prediction = model.predict(X_train)
accuracy_score_on_training_data = accuracy_score(y_train,X_train_prediction)
print("Accuracy score on training data: ",accuracy_score_on_training_data)

#Accuracy score on test data
X_test_prediction = model.predict(X_test)
accuracy_score_on_test_data = accuracy_score(y_test,X_test_prediction)
print("Accuracy score on test data: ",accuracy_score_on_test_data)