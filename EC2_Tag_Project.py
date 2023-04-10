import subprocess
import json



#PART1
#執行AWS CLI指令-Tag有Project
Tag_Project_ALL_Byte = subprocess.check_output(['aws', 'ec2', 'describe-tags', '--filters', 'Name=tag:Project,Values=*','Name=resource-type,Values=instance', '--profile', 'for_EC2'])


#將byte資料轉為Dictionary
Tag_Project_ALL_DIC = json.loads(Tag_Project_ALL_Byte)

#print(Tag_Project_ALL_DIC)

#計算有Tag是Project的EC2數量(任何state)
Tag_Project_ALL_Length = len(Tag_Project_ALL_DIC['Tags'])
print(Tag_Project_ALL_Length)


#產生Tag_Project_ALL.json
with open('Tag_Project_ALL.json', 'w') as f:
    f.write(json.dumps(Tag_Project_ALL_DIC, indent=4))


#把Instance ID append到新的list
Tag_Project_List = []
for i in Tag_Project_ALL_DIC['Tags']:
    Tag_Project_List.append(i['ResourceId'])
# print(Tag_Project_List)



#PART2
#執行AWS CLI指令-在VPC(YCVPN)的所有EC2資訊
EC2_ALL_Byte = subprocess.check_output(['aws', 'ec2', 'describe-instances', '--filters', 'Name=vpc-id,Values=vpc-fea7129b', '--profile', 'for_EC2'])

#將byte資料轉為Dictionary
EC2_ALL_DIC = json.loads(EC2_ALL_Byte)


#計算EC2數量(在YCVPN的數量)
EC2_ALL_Length = len(EC2_ALL_DIC['Reservations'])
print(EC2_ALL_Length)


#產生EC2_ALL.json
with open('EC2_ALL.json', 'w') as f:
    f.write(json.dumps(EC2_ALL_DIC, indent=4))

#把Instance ID append到新的list
EC2_List = []
EC2_List2 = []
for i in EC2_ALL_DIC['Reservations']:
    EC2_List.append(i['Instances'])


#產生EC2_ALL2.json
with open('EC2_ALL2.json', 'w') as f:
    f.write(json.dumps(EC2_List, indent=4))

for k in EC2_List:
 
    EC2_List2.append(k[0]['InstanceId'])






#Part3
#兩個list的差異(沒有tag，包含所有狀態的EC2)

difference_all_state = set(EC2_List2) - set(Tag_Project_List)
difference_all_state = list(difference_all_state)
print(len(difference_all_state))
print(difference_all_state)



#Part4
#沒有Key為Project的EC2

def result():
        global resultList 
        resultList = [] 

        for x in difference_all_state:
            No_Tag_Project_EC2_Byte = subprocess.check_output(['aws', 'ec2', 'describe-instances', '--instance-ids', x, '--profile', 'for_EC2'])
            No_Tag_Project_EC2_DIC = json.loads(No_Tag_Project_EC2_Byte)
            #找出Hostname
            list_ob_objects = No_Tag_Project_EC2_DIC['Reservations'][0]['Instances'][0]['Tags']
            Hostname = None
            
            for obj in list_ob_objects:
                if obj["Key"] == 'Name':
                    Hostname = obj["Value"]
                    break

            if No_Tag_Project_EC2_DIC['Reservations'][0]['Instances'][0]['State']['Code'] == 16:

                    resultList.append(f"a{Hostname}({x})-需要新增Tag-Project(使用中 EC2)")

            elif No_Tag_Project_EC2_DIC['Reservations'][0]['Instances'][0]['State']['Code'] == 80:
            
                    resultList.append(f"b{Hostname}({x})-無Tag-Project(關機中 EC2)")      
       
        resultList.sort()

 
result()