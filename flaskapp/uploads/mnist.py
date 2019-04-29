from sklearn import svm, metrics
import pandas as pd
from sklearn.externals import joblib
from pathlib import Path

def readCsv(file, maxcnt):
    labels = []
    images = []
    with open(file, "r") as f:
        for i, line in enumerate(f):
            if i >= maxcnt:
                break
            cols = line.split(",")
            labels.append(int(cols.pop(0)))     
            images.append(list(map(lambda b: int(b) / 256, cols)))  
    return {"labels": labels, "images": images}


test = readCsv('./data/t10k.csv', 10000)

pklFile = "./data/mnist.pkl"
clf = None
if Path(pklFile).exists():              
    print("File Exists!!")
    clf = joblib.load(pklFile)

# training ---------------------------
if not clf:
    train = readCsv('./data/train.csv', 60000) 
    clf = svm.SVC(gamma='auto')
    clf.fit(train['images'], train['labels'])
    joblib.dump(clf, pklFile)

# test -------------------------
pred = clf.predict(test['images'])

score = metrics.accuracy_score(test['labels'], pred)
print("\n\nscore=", score)

print("-----------------------------------------")
report = metrics.classification_report(test['labels'], pred)
print(report)


