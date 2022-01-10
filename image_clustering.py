import logging
import pickle
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

from config import OUTPUT_FILE, OUTPUT_LABEL_FOLDERS

logging.info("Loading encodings")
data = pickle.loads(open(OUTPUT_FILE, "rb").read())

df = pd.DataFrame(data)
df.drop(columns=["encoding"], inplace=True)

data = np.array(data)
encodings = [d["encoding"] for d in data]

logging.info("Clustering")
clt = DBSCAN(metric="euclidean", n_jobs=-1)
clt.fit(encodings)

label_ids = np.unique(clt.labels_)
n_unique_faces = len(np.where(label_ids > -1)[0])
logging.info(f"Found {n_unique_faces} unique faces")

df["label"] = clt.labels_

for label_id in label_ids:
    Path(f"{OUTPUT_LABEL_FOLDERS}/{label_id}").mkdir(parents=True, exist_ok=True)

groups = df.groupby("label")
for label_id, group in groups:
    for j, row in group.iterrows():
        image = cv2.imread(str(row["imagePath"]))
        (top, right, bottom, left) = row["loc"]
        face = image[top:bottom, left:right]

        face = cv2.resize(face, (96, 96))

        file_path = f"{OUTPUT_LABEL_FOLDERS}/{label_id}/{j}.jpg"

        cv2.imwrite(filename=file_path, img=face)
