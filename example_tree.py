from sklearn.datasets import load_iris
from sklearn import tree
from sklearn.externals.six import StringIO
from subprocess import call, run
import pydot
iris = load_iris()
clf = tree.DecisionTreeClassifier()
# INFO: Iris.data is an array of samples [[x,y,z], [x,y,z]]
# INFO: Iris.target is an array of solutions (so in our case A,B,C)
clf = clf.fit(iris.data, iris.target)
with open("iris.dot", 'w') as f:
    f = tree.export_graphviz(clf, out_file=f)
# run("dir")
# run(["dot", "-Tpdf iris.dot -o iris2.pdf"])
run("dot -Tpdf iris.dot -o iris3.pdf")
# Command to convert: dot -Tpdf iris.dot -o iris.pdf
