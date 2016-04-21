# from sklearn.datasets import load_iris
# from sklearn import tree
# iris = load_iris()
# clf = tree.DecisionTreeClassifier()
# INFO: Iris.data is an array of samples [[x,y,z], [x,y,z]]
# INFO: Iris.target is an array of solutions (so in our case A,B,C)
# clf = clf.fit(iris.data, iris.target)

######################
### CODE STARTS HERE
######################
from sklearn import tree
import sqlite3
from subprocess import call, run

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
    target_arr.append(x[2])
# print(data_arr)
clf = tree.DecisionTreeClassifier()
clf.fit(data_arr, target_arr)
with open("ours.dot", 'w') as f:
    f = tree.export_graphviz(clf, out_file=f)
print(clf.predict(results[6][3:]))
run("dot -Tpdf ours.dot -o ours4.pdf")
