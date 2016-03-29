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
# from sklearn import tree
import sqlite3

conn = sqlite3.connect('glove.db3')
c = conn.cursor()

c.execute("""SELECT * FROM Data""")
results = c.fetchall()
data_arr = []
target_arr = []
for x in results:
    data_arr.append(list(x[3:]))
    target_arr.append(x[2])
print(data_arr)
