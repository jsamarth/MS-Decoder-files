import glob, os
import numpy as np
import json
import pandas as pd
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import tensorflow as tf

vector_to_feed_male =[]
vector_to_feed_female=[]
count =0
female_dict = {}
male_dict={}

#The function to check if difference is greater than 50 percent
def greater_than_65(val1,val2):
	if (val1 >= (val2 + 0.65*val2)) or (val2 >= (val1 + 0.65*val1)):
		return True
	else:
		return False

# Female dictionary containing values of all key,value pairs.
parent_dir_female = r"C:\Users\llaho\jsons\jsons\female_g"
for json_file in glob.glob(os.path.join(parent_dir_female, '*.json')):
	reads = json.loads(open(json_file).read())
	# print(reads)
	for x in reads:
		if x not in female_dict:
			female_dict[x] = reads[x]
		else:
			female_dict[x]+=reads[x]
# print(len(female_dict))
# for m in female_dict:
# 	if female_dict[m] < 10:
# 		count+=1
# print(count)
# print(female_dict)


# Male dictionary of all key,value pairs
parent_dir_male = r"C:\Users\llaho\jsons\jsons\male_g"
for json_file in glob.glob(os.path.join(parent_dir_male, '*.json')):
	reads = json.loads(open(json_file).read())
	for y in reads:
		if y not in male_dict:
			male_dict[y] = reads[y]
		else:
			male_dict[y]+=reads[y]
# print((male_dict))


# new_features is the list containing new columns.
new_features = []

# for i in female_dict:
# 	if i in male_dict:
# 		if greater_than_65	(male_dict[i],female_dict[i]) == True:
# 			new_features.append(i)
count_1=0
for j in female_dict:
	if female_dict[j]<10 and (j not in new_features):
		count_1+=1
		new_features.append(j)
# print(count_1)

count_2=0
for k in male_dict:
	if male_dict[k]<10 and (k not in new_features):
		count_2+=1
		new_features.append(k)
# print(count_2)
print(len(new_features))




# Error checking
# for n in female_dict:
# 	if n=='40':
# 		print(female_dict[n])
# for j in male_dict:
# 	if j == '40':
# 		print(male_dict[j])


answer = []

parent_dir_female = r"C:\Users\llaho\jsons\jsons\female_g"
for json_file in glob.glob(os.path.join(parent_dir_female, '*.json')):
	# print(json_file)
	reads = json.loads(open(json_file).read())
	local_list = []
	for x in reads:
		if x in new_features:
			local_list.append(reads[x])
	vector_to_feed_female.append(local_list)
print("---------------------")
# print (vector_to_feed_female)


df_fe = pd.DataFrame(vector_to_feed_female)
df_fe.to_csv('female_data.csv',index=False,header=False)
df_fe['Label'] = 0
# print("DF_FE")
# print (df_fe)

count =0
#male dataframe
vector_to_feed_male=[]
parent_dir_male = r"C:\Users\llaho\jsons\jsons\male_g"
for json_file in glob.glob(os.path.join(parent_dir_male, '*.json')):
	reads = json.loads(open(json_file).read())
	local_list = []
	for x in reads:
		if x in new_features:
			local_list.append(reads[x])
	vector_to_feed_male.append(local_list)
# print(count)
# print (vector_to_feed_male)

df_ma = pd.DataFrame(vector_to_feed_male)
df_ma.to_csv('male_data.csv',index=False,header=False)
df_ma['Label'] = 1
	# print(df_ma.columns)
	# print df_ma

	# print (df_ma.shape)
	# print df_fe.shape
for i in range(1):
	frames=[df_ma,df_fe]
	result_df = pd.concat(frames)
	# print result_df
	result_df = shuffle(result_df)
	print (result_df)



	X_train, X_test, y_train, y_test = train_test_split(result_df.iloc[:,1:888],result_df['Label'],test_size = 0.20, random_state=42)
	print(X_train.shape)
	print(".........................................")

	print(X_test.shape)
	print(".........................................")
	print(y_train.shape)
	# print(y_train)
	print('------------------------------------------')
	print(y_test.shape)
	# print(y_test)


	columns = result_df.columns[1:888]
	columns = [str(i) for i in columns]


	feature_columns = [tf.feature_column.numeric_column("x", shape=[887])]


	classifier = tf.estimator.DNNClassifier(feature_columns=feature_columns, hidden_units=[10,2],n_classes=3)

	train_input_fn = tf.estimator.inputs.numpy_input_fn(x={"x": np.array(X_train)},y=np.array(y_train),num_epochs=None,shuffle=True)

	classifier.train(input_fn=train_input_fn, steps=2000)

	test_input_fn = tf.estimator.inputs.numpy_input_fn(x={"x": np.array(X_test)},y=np.array(y_test),num_epochs=1,shuffle=False)

	accuracy_score = classifier.evaluate(input_fn=test_input_fn)["accuracy"]

	answer.append(accuracy_score)
	print("\nTest Accuracy: {0:f}\n".format(accuracy_score))
	print(answer)
print("Average is : " + str(np.mean(answer)))
print("Max is : " + str(np.max(answer)))
print("Min is : " + str(np.min(answer)))
