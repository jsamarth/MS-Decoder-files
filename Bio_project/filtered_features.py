import glob, os
import numpy as np
import json
import pandas as pd
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import tensorflow as tf
import matplotlib.pyplot as plt

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
for m in female_dict:
	if female_dict[m] <= 150 and female_dict[m]>=50:
		count+=1
# print(count)
# print(female_dict)

count_new=0
# Male dictionary of all key,value pairs
parent_dir_male = r"C:\Users\llaho\jsons\jsons\male_g"
for json_file in glob.glob(os.path.join(parent_dir_male, '*.json')):
	reads = json.loads(open(json_file).read())
	for y in reads:
		if y not in male_dict:
			male_dict[y] = reads[y]
		else:
			male_dict[y]+=reads[y]
for l in male_dict:
	if male_dict[l]<=150 and male_dict[l] >= 50:
		count_new+=1
# print(count_new)
# print((male_dict))


# new_features is the list containing new columns.
new_features = []
new_features_dict = dict()

# for i in female_dict:
# 	if i in male_dict:
# 		if greater_than_65	(male_dict[i],female_dict[i]) == True:
# 			new_features.append(i)
count_1=0
var_female = []
for j in female_dict:
	if female_dict[j]<=150 and female_dict[j]>=50:
		count_1+=1
		new_features_dict[j]=female_dict[j]
		new_features.append(j)
# print(count_1)
# print(len(new_features_dict))


count_2=0
for k in male_dict:
	if male_dict[k]<=150 and male_dict[k]>=50 and k not in new_features_dict:
		count_2+=1
		new_features_dict[k] = male_dict[j]
		new_features.append(k)
	elif male_dict[k]<=150 and male_dict[k]>=50 and k in new_features_dict:
		new_features_dict[k]+=male_dict[k]
		new_features.append(k)


# print((new_features_dict))

#The following code tells us that there are 30 overlapping features
# num=0
# for l in female_dict:
# 	if female_dict[l]<=150 and female_dict[l]>=50:
# 		if male_dict[l]<=150 and male_dict[l]>=50:
# 			print(l)
# 			num+=1
# print(num)
# print(count_2)


# Error checking
# for n in female_dict:
# 	if n=='40':
# 		print(female_dict[n])
# for j in male_dict:
# 	if j == '40':
# 		print(male_dict[j])









#To find the keys of new_features_dict in our samples:
#1) On the female set:
tot_var = dict()
num=0
for i in new_features_dict.keys():
	# print(i)
	parent_dir_female = r"C:\Users\llaho\jsons\jsons\female_g"
	new_list = []
	for json_file in glob.glob(os.path.join(parent_dir_female, '*.json')):
		reads = json.loads(open(json_file).read())
		# print(reads)
		for x in reads:
			if x==i:
				new_list.append(reads[x])
			# print(new_list)
	parent_dir_male = r"C:\Users\llaho\jsons\jsons\male_g"
	for json_file in glob.glob(os.path.join(parent_dir_male, '*.json')):
		reads = json.loads(open(json_file).read())
		for y in reads:
			if y==i:
				new_list.append(reads[y])
	tot_var[i] = new_list
# print(tot_var)

#tot_var has values for all 250 files in a list
#Now need to compute variances of each list and assign it back to the taxon
for i in tot_var:
	variance = np.var(tot_var[i])
	tot_var[i] = variance
# print(tot_var)

filtered_list =[]
sorted_var = sorted((value, key) for (key,value) in tot_var.items())
# print(sorted_var)
print(len(sorted_var))
for i in sorted_var:
	# print(i)
	if i[0]>7:
		filtered_list.append(i[1])
#
# print(filtered_list)




answer = []

parent_dir_female = r"C:\Users\llaho\jsons\jsons\female_g"
for json_file in glob.glob(os.path.join(parent_dir_female, '*.json')):
	# print(json_file)
	reads = json.loads(open(json_file).read())
	local_list = []
	for x in reads:
		if x in filtered_list:
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
		if x in filtered_list:
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
frames=[df_ma,df_fe]
result_df = pd.concat(frames)
	# print result_df
result_df = shuffle(result_df)
for i in range(50):

	print (result_df)



	X_train, X_test, y_train, y_test = train_test_split(result_df.iloc[:,1:42],result_df['Label'],test_size = 0.20, random_state=42)
	print(X_train.shape)
	print(".........................................")

	print(X_test.shape)
	print(".........................................")
	print(y_train.shape)
	# print(y_train)
	print('------------------------------------------')
	print(y_test.shape)
	# print(y_test)


	columns = result_df.columns[1:42]
	columns = [str(i) for i in columns]


	feature_columns = [tf.feature_column.numeric_column("x", shape=[41])]


	classifier = tf.estimator.DNNClassifier(feature_columns=feature_columns, hidden_units=[10,2],n_classes=2)

	train_input_fn = tf.estimator.inputs.numpy_input_fn(x={"x": np.array(X_train)},y=np.array(y_train),num_epochs=None,shuffle=True)

	classifier.train(input_fn=train_input_fn, steps=3000)

	test_input_fn = tf.estimator.inputs.numpy_input_fn(x={"x": np.array(X_test)},y=np.array(y_test),num_epochs=1,shuffle=False)

	accuracy_score = classifier.evaluate(input_fn=test_input_fn)["accuracy"]

	answer.append(accuracy_score)
	print("\nTest Accuracy: {0:f}\n".format(accuracy_score))
	print(answer)


axis_val = [x for x in range(len(answer))]
plt.plot(axis_val,answer)
plt.show()


print("Average is : " + str(np.mean(answer)))
print("Max is : " + str(np.max(answer)))
print("Min is : " + str(np.min(answer)))
