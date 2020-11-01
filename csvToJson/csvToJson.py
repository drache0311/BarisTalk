# 중복되는 단어 제거된 csv파일로 json 단어 2000개 이하로 나눠 생성하기 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import csv
import pandas as pd

lines_seen = set()


#중복제거 된 csv 파일
print('파일열기시작')
f = open('./one_line.csv','r',encoding='utf-8')
rdr = csv.reader(f)


#json 파일생성및 열기
i=0 # 2000개씩 나눌 때 쓸 카운트
a=1
f2 = open ('chatting_usersays_ko.json','w',encoding='utf-8')
f2.write("[")

for line in rdr:
    for text in line:
        if i == 1999:
            f2.write("]")
            f2.close()
            f2 = open('chatting_usersays_ko'+str(a)+'.json','w',encoding='utf-8')
            f2.write("[")
            i=1
            a=a+1
        i=i+1
        
        #파일에 유저입력 intent 데이터 json  삽입
        f2.write('{ "id": "3330d5a3-f38e-48fd-a3e6-000000000001", "data": [ { "text": "' + text + '", "userDefined": false } ], "isTemplate": false, "count": 0, "lang": "ko", "updated": 0 },')
f2.write("]")
f.close()
f2.close()

#    print(line)


#f.close()


