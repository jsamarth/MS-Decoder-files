import glob, os
import numpy as np
import json
vector_to_feed_female = []


#Female dataframe
parent_dir_female = r"C:\Users\Lakshya\Desktop\jsons\jsons\experiment_4_f"
for json_file in glob.glob(os.path.join(parent_dir_female, '*.json')):
	reads = json.loads(open(json_file).read())
	local_list = []
	for x in reads:
		local_list.append(reads[x])
	vector_to_feed_female.append(local_list)
# print vector_to_feed

import pandas as pd
df_fe = pd.DataFrame(vector_to_feed_female)
df_fe.to_csv('female_data.csv',index=False,header=False)
df_fe['Label'] = 0
# print df_fe


#male dataframe
vector_to_feed_male=[]
parent_dir_male = r"C:\Users\Lakshya\Desktop\jsons\jsons\experiment_4_m"
for json_file in glob.glob(os.path.join(parent_dir_male, '*.json')):
	reads = json.loads(open(json_file).read())
	local_list = []
	for x in reads:
		local_list.append(reads[x])
	vector_to_feed_male.append(local_list)
# print vector_to_feed

df_ma = pd.DataFrame(vector_to_feed_male)
df_ma.to_csv('male_data.csv',index=False,header=False)
df_ma['Label'] = 1
# print df_ma

# print (df_ma.shape)
# print df_fe.shape

frames=[df_ma,df_fe]
result_df = pd.concat(frames)
# print result_df

from sklearn.utils import shuffle
result_df = shuffle(result_df)
print (result_df)



from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(result_df.iloc[:,1:1805],result_df['Label'],test_size = 0.20, random_state=42)
print(X_train.shape)
print(".........................................")

print(X_test.shape)
print(".........................................")
print(y_train.shape)
# print(y_train)
print('------------------------------------------')
print(y_test.shape)
# print(y_test)


columns = result_df.columns[1:1805]
columns = [str(i) for i in columns]

import tensorflow as tf

feature_columns = [tf.feature_column.numeric_column("x", shape=[1804])]

classifier = tf.estimator.DNNClassifier(feature_columns=feature_columns, hidden_units=[10,10],n_classes=3)

train_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": np.array(X_train)},
      y=np.array(y_train),
      num_epochs=None,
      shuffle=True)

classifier.train(input_fn=train_input_fn, steps=2000)

test_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": np.array(X_test)},
      y=np.array(y_test),
      num_epochs=1,
      shuffle=False)

accuracy_score = classifier.evaluate(input_fn=test_input_fn)["accuracy"]
print("\nTest Accuracy: {0:f}\n".format(accuracy_score))
