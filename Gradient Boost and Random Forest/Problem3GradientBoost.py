from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import RandomizedSearchCV
#using random search instead of grid because grid was taking too long
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_svmlight_file
from scipy.stats import randint, uniform

#get test and training data
X_train, y_train = load_svmlight_file("a9a.txt")
X_test, y_test = load_svmlight_file("a9a.t")

#create the parameters
parameters = {
    'n_estimators': randint(100, 300),
    'learning_rate': uniform(0.01, 0.1),
    'max_depth': randint(3, 7),
    'subsample': uniform(0.0, 1.0)
}

#perform search and get best estimator
estimateSearch = RandomizedSearchCV(estimator=GradientBoostingClassifier(random_state=42), param_distributions=parameters, n_iter=10, cv=3, n_jobs=-1, random_state=42).fit(X_train, y_train)
bestEstimate = estimateSearch.best_estimator_
bestEstimate.fit(X_train, y_train)
finalPred = bestEstimate.predict(X_test)
bestEstimate.fit(X_train, y_train)
trainingPred = bestEstimate.predict(X_train)

#get and print training accuracy
trainAcc = accuracy_score(y_train, trainingPred)
print("Gradient Boosting Training Accuracy: {:.2f}%".format(trainAcc * 100))

#get and print accuracy
accuracy = accuracy_score(y_test, finalPred)
print("Gradient Boosting Test Accuracy: {:.2f}%".format(accuracy * 100))