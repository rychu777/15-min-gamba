import matplotlib.pyplot as plt
from numpy import loadtxt
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, recall_score, precision_score, roc_auc_score, \
    roc_curve
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

clf = SVC(kernel='linear')
# LINEAR -> 76.33% (ACC)
# RBF -> 76.09% (ACC)
# POLY -> 75.51% (ACC)
sc = StandardScaler()

dataset_train = loadtxt('../Data/prepared_data_train.csv', delimiter=',')
dataset_test = loadtxt('../Data/prepared_data_test.csv', delimiter=',')

dataset_train_values = dataset_train[:, 0:13]
Y_train = dataset_train[:, 13]

dataset_test_values = dataset_test[:, 0:13]
Y_test = dataset_test[:, 13]

sc.fit(dataset_train_values)

X_train_sc = sc.transform(dataset_train_values)
X_test_sc = sc.transform(dataset_test_values)

clf.fit(X_train_sc, Y_train)
Y_pred = clf.predict(X_test_sc)

# Accuracy
accuracy = accuracy_score(Y_test, Y_pred)

# Precision
precision = precision_score(Y_test, Y_pred)

# Recall
recall = recall_score(Y_test, Y_pred)

# F1-score
f1 = f1_score(Y_test, Y_pred)

# Confusion matrix
conf_matrix = confusion_matrix(Y_test, Y_pred)

# ROC curve
fpr, tpr, thresholds = roc_curve(Y_test, Y_pred)
auc_score = roc_auc_score(Y_test, Y_pred)

# Plot ROC curve
plt.figure().canvas.manager.set_window_title("ROC Curve")
plt.plot(fpr, tpr, label='AUC-Score: ' + str(round(auc_score, 2)), color='#1260CC')
plt.plot([0, 1], [0, 1], 'r--', label='Random: 0.5')
plt.axis((0, 1, 0, 1))
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc='best')
plt.show()

# Print additional evaluation metrics
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)
print("Confusion Matrix:\n", conf_matrix)
