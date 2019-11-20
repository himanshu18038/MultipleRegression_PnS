"""
Name-Himanshu Raj
Roll No-2018038
Section-A
Group-6
Branch-CSE
Assignment-2
"""
from csv import reader,writer,QUOTE_ALL
import numpy as np

def combo(xtrain,xtest,s):							#to make the input list as per combination
	indices=[0]
	for i in range(len(s)):
		if(s[i]=='1'):
			indices.append(i+1)
	a,b=[[0]*len(indices)]*len(xtrain),[[0]*len(indices)]*len(xtest)
	for i in range(len(xtrain)):
		k=0
		for j in range(len(xtrain[0])):
			if(j in indices):
				a[i][k]=xtrain[i][j]
				k+=1
	for i in range(len(xtest)):
		k=0
		for j in range(len(xtest[0])):
			if(j in indices):
				b[i][k]=xtest[i][j]
				k+=1
	return a,b

def comboname(s):									#To set the combinations name
	r=''
	if(s[0]=='1'):
		r+='SJR+'
	if(s[1]=='1'):
		r+='H-Index+'
	if(s[2]=='1'):
		r+='Total Docs(2017)+'
	if(s[3]=='1'):
		r+='Total Docs(3years)+'
	if(s[4]=='1'):
		r+='Total Refs+'
	if(s[5]=='1'):
		r+='Total Cites(3years)+'
	if(s[6]=='1'):
		r+='Citable Docs(3years)+'
	if(s[7]=='1'):
		r+='Cites/Docs(2years)+'
	if(s[8]=='1'):
		r+='Ref/Doc+'
	return r[:-1]

def error(coeff,xtest,ytest):						#to find the errors
	m=np.matmul(xtest,coeff).tolist()
	mse,mae=0,0
	for i in range(len(m)):
		mse+=((m[i][0]-ytest[i][0])**2)
		mae+=(abs(m[i][0]-ytest[i][0]))
	return [mae/len(m),mse/len(m)]

def reg_eqn(x,y,comb):
	lentrain=int(0.8*len(x))						#defining the size of train and test set
	xtrain=x[:lentrain]
	ytrain=y[:lentrain]
	xtest=x[lentrain:]
	ytest=y[lentrain:]
	xtrain,xtest=combo(xtrain,xtest,comb)
	xtrain=np.array(xtrain)
	ytrain=np.matrix(ytrain)
	xt=np.transpose(xtrain)
	mat = np.dot(xt,xtrain).tolist()
	a = np.array(mat)
	matinv=np.linalg.inv(a).tolist()
	res=np.dot(matinv,xt).tolist()
	coeff=np.dot(res,ytrain).tolist()
	# coeff=np.matmul(np.matmul(np.linalg.inv(np.matmul(np.transpose(xtrain),xtrain)),np.transpose(xtrain)),ytrain)
	# coeff=np.linalg.solve(np.matmul(xt,xtrain),np.matmul(xt,ytrain)).tolist()
	# print(coeff)
	return [comboname(comb)]+error(coeff,xtest,ytest)

jour=open('found.txt','r')							#opening the data file in read mode
l=[]
j=0

for i in reader(jour,quotechar='"', delimiter=';',quoting=QUOTE_ALL):		#reading the input file
	if(j==0):
		j=1
		continue
	l.append([i[0],i[1],i[2]])

f1=open('WebData.csv','r')							#Opened ConferenceData file in read mode for input
k=0
sjr=[]
h_index=[]
docs17=[]
docs3=[]
refs=[]
cites3=[]
citesdoc3=[]
citesdoc2=[]
refdoc=[]
impfac=[]
x=[]
k=0
for i in reader(f1, quotechar='"', delimiter=';',quoting=QUOTE_ALL):
	if(k==0):
		k=1
		continue
	for j in range(len(l)):
		if(i[2].replace(',','')==l[j][0].replace("-",": ") or i[2]==l[j][0] or i[2].replace(',','')==l[j][0].replace("-"," : ") or i[2].replace(',','')==l[j][0].replace("-"," - ")):
			if(i[5]!='' and citesdoc3!=0):
				sjr.append(float(i[5].replace(',','.')))
			else:
				continue
			h_index.append(float(i[7]))
			docs17.append(float(i[8]))
			docs3.append(float(i[9]))
			refs.append(float(i[10]))
			cites3.append(float(i[11]))
			citesdoc3.append(float(i[12]))
			citesdoc2.append(float(i[13].replace(',','.')))
			refdoc.append(float(i[14].replace(',','.')))
			x.append([1,sjr[-1],h_index[-1],docs17[-1],docs3[-1],refs[-1],cites3[-1],citesdoc3[-1],citesdoc2[-1],refdoc[-1]])
			impfac.append([float(l[j][2])])
# print(len(x))
y=impfac[:]
l3=[]
k=1
mse=[]
mae=[]
for i in range(1,512):
	try:
		s=bin(i)[2:]
		s='0'*(9-len(s))+s
		l3.append([k]+reg_eqn(x,y,s))
		mae.append(l3[-1][2])
		mse.append(l3[-1][3])
		k+=1
	except:
		continue
# print(len(l3))

min_mae=min(mae)
min_mse=min(mse)
for i in range(len(l3)):
	if(l3[i][2]==min_mae):
		print("Minimum Mean Absolute Error on data set "+l3[i][1]+" vs Impact Factor")
		print("Minimum Mean Absolute Error=",l3[i][2],"\n")
		break
for i in range(len(l3)):
	if(l3[i][3]==min_mse):
		print("Minimum Mean Squared Error on data set "+l3[i][1]+" vs Impact Factor")
		print("Minimum Mean Squared Error=",l3[i][3],"\n")
		break

l3=[["S.No.","Combination","Mean Absolute Error","Mean Squared Error"]]+l3

f2=open('Error.csv', 'w', newline='')												#Opening a new file
writer(f2).writerows(l3)															#Writing data-set in Output file

print('Open Error.csv file to see all the combinations of errors')
