from keras.regularizers import l1, l2
from matplotlib import pyplot as plt
from numpy import loadtxt
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Dense, Normalization, Input, PReLU
from sklearn.metrics import roc_curve, roc_auc_score, accuracy_score, precision_score, recall_score, f1_score, \
    confusion_matrix

dataset_train = loadtxt('../Data/prepared_data_train.csv', delimiter=',')
dataset_test = loadtxt('../Data/prepared_data_test.csv', delimiter=',')
dataset_val = loadtxt('../Data/prepared_data_val.csv', delimiter=',')

dataset_train_values = dataset_train[:, 0:13]
dataset_train_win = dataset_train[:, 13]

dataset_test_values = dataset_test[:, 0:13]
dataset_test_win = dataset_test[:, 13]

dataset_val_values = dataset_val[:, 0:13]
dataset_val_win = dataset_val[:, 13]

# Input layer
input_layer = Input(shape=(13,))

# Normalization layer
norm_layer = Normalization()
norm_layer.adapt(dataset_train_values)

# Define the keras model 77.01%
model = Sequential()
model.add(input_layer)
model.add(norm_layer)
model.add(Dense(7, input_shape=(13,), activation='elu',activity_regularizer=l2(0.0001)))
model.add(PReLU())
model.add(Dense(7, activation='elu', activity_regularizer=l2(0.0001)))
model.add(Dense(7, activation='elu', activity_regularizer=l2(0.0001)))
model.add(Dense(1, activation='sigmoid', activity_regularizer=l2(0.0001)))

new_learning_rate = 0.001

# Prepare optimizer
optimizer = Adam(learning_rate=new_learning_rate)

# Compile the keras model
model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])

# Fit the keras model on the dataset
model.fit(x=dataset_train_values, y=dataset_train_win, epochs=300, batch_size=1024,
          validation_data=(dataset_val_values, dataset_val_win))

# Make class predictions with the model
predictions = (model.predict(dataset_test_values))

# Accuracy
accuracy = accuracy_score(dataset_test_win, predictions.round())

# Precision
precision = precision_score(dataset_test_win, predictions.round())

# Recall
recall = recall_score(dataset_test_win, predictions.round())

# F1-score
f1 = f1_score(dataset_test_win, predictions.round())

# Confusion matrix
conf_matrix = confusion_matrix(dataset_test_win, predictions.round())

# ROC curve
fpr, tpr, thresholds = roc_curve(dataset_test_win, predictions)
auc_score = roc_auc_score(dataset_test_win, predictions)

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
