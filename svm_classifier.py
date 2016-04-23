
# Standard scientific Python imports
import matplotlib.pyplot as plt

# Import datasets, classifiers and performance metrics
from sklearn import datasets, svm, metrics, tree
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC
import numpy as np
import sqlite3

# The digits dataset
digits = datasets.load_digits()

# The data that we are interested in is made of 8x8 images of digits, let's
# have a look at the first 3 images, stored in the `images` attribute of the
# dataset.  If we were working from image files, we could load them using
# pylab.imread.  Note that each image must have the same size. For these
# images, we know which digit they represent: it is given in the 'target' of
# the dataset.
conn = sqlite3.connect('glove.db3')
c = conn.cursor()

c.execute("""SELECT * FROM Data""")
results = c.fetchall()
data_arr = []
target_arr = []
# print(len(results[:6]))
# for x in results[:6]:
#     data_arr.append(list(x[3:]))
#     target_arr.append(x[2])
print(len(results))
for x in results:
    data_arr.append(list(x[3:]))
    # data_arr.append(list(x[3:-3]))
    target_arr.append(x[2])

# To apply a classifier on this data, we need to flatten the image, to
# turn the data in a (samples, feature) matrix:
n_samples = len(data_arr)
# ata = digits.images.reshape((n_samples, -1))

# Create a classifier: a support vector classifier
# classifier = svm.SVC(gamma=0.03, C=2.0) .65
# classifier = svm.SVC(gamma=0.01, C=4.9) .68
# classifier = svm.SVC(gamma=0.02, C=2.75)
# technically higher
classifier = svm.SVC(gamma=0.01, C=4.65)
# We learn the digits on the first half of the digits
#classifier.fit(data[:n_samples / 2], digits.target[:n_samples / 2])
classifier.fit(data_arr, target_arr)
# svm1 = svm.SVC(gamma=0.1)
# svm1.fit(data_arr, target_arr)
# svm2 = svm.SVC(gamma=0.2)
# svm2.fit(data_arr, target_arr)
# svm3 = svm.SVC(gamma=0.05)
# svm3.fit(data_arr, target_arr)
clf1 = tree.DecisionTreeClassifier()
clf1.fit(data_arr, target_arr)

# C_range = np.logspace(-2, 10, 13)
# gamma_range = np.logspace(-9, 3, 13)
# param_grid = dict(gamma=gamma_range, C=C_range)
# cv = StratifiedShuffleSplit(target_arr, n_iter=5, test_size=0.2, random_state=42)
# grid = GridSearchCV(SVC(), param_grid=param_grid, cv=cv)
# grid.fit(data_arr, target_arr)
#
# print("The best parameters are %s with a score of %0.2f"
#       % (grid.best_params_, grid.best_score_))


# Now predict the value of the digit on the second half:
# expected = digits.target[n_samples / 2:]
# predicted = classifier.predict(data[n_samples / 2:])
conn2 = sqlite3.connect('glove_training.db3')
c2 = conn2.cursor()

c2.execute("""SELECT * FROM Data""")
results2 = c2.fetchall()
training_arr = []
training_target_arr = []
for x in results2[3:]:
    training_arr.append(list(x[3:]))
    # data_arr.append(list(x[3:-3]))
    training_target_arr.append(x[2])
# expected = data_arr
# print(training_arr)
gamma_junk = np.arange(0.005, 0.25, .005)
c_junk = np.arange(0.05, 5.00, .05)

# predicted = classifier.predict(training_arr)
# max_acc = 0
# max_gamma = 0
# max_c = 0
# for gamma in gamma_junk:
#     for c in c_junk:
#         classifier = svm.SVC(gamma=gamma, C=c)
#         classifier.fit(data_arr, target_arr)
#         predicted = classifier.predict(training_arr)
#         acc = metrics.accuracy_score(predicted, training_target_arr)
#         print(acc)
#         if acc > max_acc:
#             max_acc = acc
#             max_gamma = gamma
#             max_c = c
# print("Max Acc: {0} \n Max Gamma: {1} \n Max C: {2} \n".format(max_acc, max_gamma, max_c))

predicted = classifier.predict(training_arr)
print(metrics.accuracy_score(predicted, training_target_arr))
print("Classification report for classifier %s:\n%s\n"
       % (classifier, metrics.classification_report(predicted, training_target_arr)))
# predicted = svm1.predict(training_arr)
# print("Classification report for classifier %s:\n%s\n"
#        % (svm1, metrics.classification_report(predicted, training_target_arr)))
# predicted = svm2.predict(training_arr)
# print("Classification report for classifier %s:\n%s\n"
#        % (svm2, metrics.classification_report(predicted, training_target_arr)))
# predicted = svm3.predict(training_arr)
# print("Classification report for classifier %s:\n%s\n"
#       % (svm3, metrics.classification_report(predicted, training_target_arr)))
predicted = clf1.predict(training_arr)
print(metrics.accuracy_score(predicted, training_target_arr))
print("Classification report for classifier %s:\n%s\n"
       % (clf1, metrics.classification_report(predicted, training_target_arr)))
# print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))
#
# images_and_predictions = list(zip(digits.images[n_samples / 2:], predicted))
# for index, (image, prediction) in enumerate(images_and_predictions[:4]):
#     plt.subplot(2, 4, index + 5)
#     plt.axis('off')
#     plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
#     plt.title('Prediction: %i' % prediction)
#
# plt.show()
