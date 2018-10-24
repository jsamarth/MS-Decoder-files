import glob, os
import numpy as np
import json
import pandas as pd
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn import svm
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




# Male dictionary of all key,value pairs
count_new=0
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
# print(len(sorted_var))
for i in sorted_var:
	# print(i)
	if i[0]>7:
		filtered_list.append(i[1])
print((filtered_list))




# making vectors to feed into the neural net
# 1) female
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

# Make dataframe of the vectors
df_fe = pd.DataFrame(vector_to_feed_female)
df_fe.to_csv('female_data.csv',index=False,header=False)
df_fe['Label'] = 0
# print("DF_FE")
# print (df_fe)


# male dataframe
count =0
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
# print(df_ma)



# Make the combined dataframe
frames=[df_ma,df_fe]
result_df = pd.concat(frames)
# print(result_df["Label"].value_counts(normalize=True))
# print(result_df)



#Create a dictionary to cumulate the importances and make a plot later
imp_dict = dict()
for i in result_df.columns:
	imp_dict[i] = 0
# print(imp_dict)


#Create lists to store the various attributes of random forests
d_trees = []
n_classes = []
n_features = []
importances = []
accuracy_plot = []
check_count =0
gnb_plot = []
bnb_plot = []
svm_plot = []
for i in range(50):
	X_train, X_test, y_train, y_test = train_test_split(result_df.iloc[:,1:42],result_df['Label'],test_size = 0.20, random_state=42)
	# print(X_train.shape)
	# print(X_test.shape)
	# print(y_train.shape)
	# print(y_test.shape)


	#Random forest classifier
	print("-"*10)
	rfc = RandomForestClassifier(n_estimators = 15, max_depth = 30)
	rfc.fit(X_train, y_train)
	predict_rfc = rfc.predict(X_train)
	n_features.append(rfc.n_features_)
	n_classes.append(rfc.n_classes_)
	count_rfc = 0
	for j in range(len(predict_rfc)):
		if predict_rfc[j] == y_train.iloc[j]:
			count_rfc = count_rfc + 1;
	accuracy_rfc = count_rfc/(len(predict_rfc))
	accuracy_plot.append(accuracy_rfc)
	d_trees.append(rfc.estimators_)
	# importances.append(rfc.feature_importances_)
	feature_importances = pd.DataFrame(rfc.feature_importances_,index = X_train.columns,columns=['importance']).sort_values('importance', ascending = False)
	index_list = (feature_importances.index.tolist())
	# if(i<5):
		# print(feature_importances)
	for j in index_list:
		if j in imp_dict:
			imp_dict[j] += (feature_importances.loc[j]["importance"])
	# print(feature_importances.loc["0",:]["importance"])
	# for i in feature_importances.index:
	# 	if i=="0":
	# 		check_dict["0"] += feature_importances.loc["0"]["importance"]
	# for j in feature_importances.index:
	# 	if j == "1":
	# 		check_dict["1"] += feature_importances.loc["1"]





	#Gaussian NB
	gnb = GaussianNB()
	gnb.fit(X_train, y_train)
	predict_gnb = gnb.predict(X_test)
	count_gnb = 0
	for k in range(len(predict_gnb)):
		if(predict_gnb[k] == y_test.iloc[k]):
			count_gnb = count_gnb + 1
	accuracy_gnb = count_gnb/len(predict_gnb)
	gnb_plot.append(accuracy_gnb)




	#Bernoulli NB
	bnb = BernoulliNB()
	bnb.fit(X_train, y_train)
	predict_bnb = bnb.predict(X_test)
	count_bnb = 0
	for k in range(len(predict_bnb)):
		if(predict_bnb[k] == y_test.iloc[k]):
			count_bnb = count_bnb + 1
	accuracy_bnb = count_bnb/len(predict_bnb)
	bnb_plot.append(accuracy_bnb)





	#svm
	clf = svm.SVC()
	clf.fit(X_train, y_train)
	predict_svm = clf.predict(X_test)
	count_svm = 0
	for k in range(len(predict_svm)):
		if(predict_svm[k] == y_test.iloc[k]):
			count_svm = count_svm+ 1
	accuracy_svm = count_svm/len(predict_svm)
	svm_plot.append(accuracy_svm)




plot_ = [x for x in range(len(accuracy_plot))]
# plt.plot(plot_,svm_plot)
# plt.plot(plot_, accuracy_plot)
# plt.plot(plot_, gnb_plot)
# plt.plot(plot_, bnb_plot)


#Get the decision tree using .estimators
d_trees.append(rfc.estimators_)
# print(d_trees)
# for i in d_trees:
# 	print(i.n_classes_)
n_classes.append(rfc.n_classes_)
# print(n_classes)

feature_index = imp_dict.keys()
feature_values = imp_dict.values()
# print(feature_values)
sorted_feature_values = sorted(feature_values, reverse=True)[:20]
# print(sorted_feature_values)

top_20_keys = []
for i,j in imp_dict.items():
	if j in sorted_feature_values:
		top_20_keys.append(i)

# print(top_20_keys)
top_20_ids = []
for i in ((top_20_keys)):
	top_20_ids.append(filtered_list[i])
print(top_20_ids)

new_df = result_df["Label"]

for k in result_df.columns:
	if k not in top_20_keys:
		result_df = result_df.drop(columns = k , axis = 1)
result_df['Label'] = new_df
# print(result_df)
################################# JUST FOR TESTING #############################
# for i in range(500):
# 	X_train, X_test, y_train, y_test = train_test_split(result_df.iloc[:,1:20],result_df['Label'],test_size = 0.20, random_state=42)
# 	# print(X_train.shape)
# 	# print(X_test.shape)
# 	# print(y_train.shape)
# 	# print(y_test.shape)
#
#
# 	#Random forest classifier
# 	print("-"*10)
# 	rfc = RandomForestClassifier(n_estimators = 30, max_depth = 30)
# 	rfc.fit(X_train, y_train)
# 	predict_rfc = rfc.predict(X_test)
# 	n_features.append(rfc.n_features_)
# 	n_classes.append(rfc.n_classes_)
# 	count_rfc = 0
# 	for j in range(len(predict_rfc)):
# 		if predict_rfc[j] == y_test.iloc[j]:
# 			count_rfc = count_rfc + 1;
# 	accuracy_rfc = count_rfc/(len(predict_rfc))
# 	accuracy_plot.append(accuracy_rfc)
# new_ax = [i for i in range(len(accuracy_plot))]
# plt.plot(new_ax,accuracy_plot)
# plt.show()
# print(np.mean(accuracy_plot))

for i in range(100):
	# frames=[df_ma,df_fe]
	# result_df = pd.concat(frames)
	# print result_df
	result_df = shuffle(result_df)
	print (result_df)



	X_train, X_test, y_train, y_test = train_test_split(result_df.iloc[:,1:20],result_df['Label'],test_size = 0.20, random_state=42)
	print(X_train.shape)
	print(".........................................")

	print(X_test.shape)
	print(".........................................")
	print(y_train.shape)
	# print(y_train)
	print('------------------------------------------')
	print(y_test.shape)
	# print(y_test)


	columns = result_df.columns[1:20]
	columns = [str(i) for i in columns]


	feature_columns = [tf.feature_column.numeric_column("x", shape=[19])]

	# Added dropout and l1 regularization in the optimizer, and batch norm
	classifier = tf.estimator.DNNClassifier(feature_columns=feature_columns, hidden_units=[10,2],n_classes=3, dropout=0.5, optimizer=tf.train.ProximalAdagradOptimizer(
      learning_rate=0.1,
      l1_regularization_strength=0.001
    ), batch_norm=True)

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

#################################################################################3






# {str(k): str(v) for k, v in imp_dict.items()}
# # print((imp_dict.keys()))
# x_axis = []
# for i in imp_dict.keys():
# 	if(i != 'Label'):
# 		i = str(i)
# 		x_axis.append(i)
# y_axis =[]
# for j in range(len(imp_dict.values())-1):
# 	t = float(imp_dict[j])
# 	y_axis.append(t)
#
# plt.figure(figsize=(11,8))
# # print(len(x_axis))
# # print(len(y_axis))
# plt.bar(x_axis, y_axis)
# # for i in enumerate(y_axis):
# #     plt.annotate(i, x_axis)
# # print(enumerate(y_axis))
# plt.xlabel("Index of various ID's")
# plt.ylabel("Importance")
# plt.show()


# print("Average is : " + str(np.mean(accuracy_plot)))
# print("Max is : " + str(np.max(accuracy_plot)))
# print("Min is : " + str(np.min(accuracy_plot)))
