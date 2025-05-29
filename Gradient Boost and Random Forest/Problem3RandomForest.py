from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
# using random because grid was taking far too long to run on my laptop
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_svmlight_file
from scipy.stats import randint

#training and test data load
X_train, y_train = load_svmlight_file("a9a.txt")
X_test, y_test = load_svmlight_file("a9a.t")

#set the parameters
parameters = {
    'n_estimators': randint(100, 300),
    'max_depth': randint(5, 15),
    'min_samples_split': randint(2, 10),
    'min_samples_leaf': randint(1, 4)
}

#perform search and get best estimator then use test dataset
performedSearch = RandomizedSearchCV(estimator=RandomForestClassifier(random_state=42), param_distributions=parameters, n_iter=10, cv=3, n_jobs=-1, random_state=42).fit(X_train, y_train)
bestEstimate = performedSearch.best_estimator_
bestEstimate.fit(X_train, y_train)
finalPrediction = bestEstimate.predict(X_test)
bestEstimate.fit(X_train, y_train)
trainingPred = bestEstimate.predict(X_train)

#get and print training accuracy
trainAcc = accuracy_score(y_train, trainingPred)
print("Random Forest Training Accuracy: {:.2f}%".format(trainAcc * 100))

#get and print accuracy
accuracy = accuracy_score(y_test, finalPrediction)
print("Random Forest Test Accuracy: {:.2f}%".format(accuracy * 100))