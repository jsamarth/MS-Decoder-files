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

frames=[df_ma,df_fe]
result_df = pd.concat(frames)
# print(result_df["Label"].value_counts(normalize=True))





accuracy_plot = []
gnb_plot = []
bnb_plot = []
svm_plot = []
for i in range(30):
	X_train, X_test, y_train, y_test = train_test_split(result_df.iloc[:,1:42],result_df['Label'],test_size = 0.20, random_state=42)

	#Random forest classifier
	rfc = RandomForestClassifier(n_estimators = 10, max_depth = 30)
	rfc.fit(X_train, y_train)
	predict_rfc = rfc.predict(X_test)
	count_rfc = 0
	for j in range(len(predict_rfc)):
		if predict_rfc[j] == y_test.iloc[j]:
			count_rfc = count_rfc + 1;
	accuracy_rfc = count_rfc/(len(predict_rfc))
	accuracy_plot.append(accuracy_rfc)


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
plt.plot(plot_,svm_plot)
plt.plot(plot_, accuracy_plot)
plt.plot(plot_, gnb_plot)
plt.plot(plot_, bnb_plot)
plt.legend(loc = @)
plt.show()



print("Average is : " + str(np.mean(accuracy_plot)))
print("Max is : " + str(np.max(accuracy_plot)))
print("Min is : " + str(np.min(accuracy_plot)))
