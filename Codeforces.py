import requests
from bs4 import BeautifulSoup

user = input("Enter user handle : ")
prob = input("Enter problemID in format {ContestId+ProblemCode} e.g 1256C : ")

# JSON format --------------
# {'status': 'OK', 'result': [{'id': 72681187, 'contestId': 1238, 
# 'creationTimeSeconds': 1583602017, 'relativeTimeSeconds': 2147483647, 
# 'problem': {'contestId': 1238, 'index': 'A', 'name': 'Prime Subtraction', 
# 'type': 'PROGRAMMING', 'rating': 900, 'tags': ['math', 'number theory']}, 
# 'author': {'contestId': 1238, 'members': [{'handle': 'Nareshhhh'}], 
# 'participantType': 'PRACTICE', 'ghost': False, 'startTimeSeconds': 1570545300}, 
# 'programmingLanguage': 'GNU C++14', 'verdict': 'COMPILATION_ERROR', 
# 'testset': 'TESTS', 'passedTestCount': 0, 'timeConsumedMillis': 0, 
# 'memoryConsumedBytes': 0}]}

req = requests.get('https://codeforces.com/api/user.status?handle='+str(user))
f=False
requrl = 'none'
subID = ''
print()
for subs in req.json()['result']:
    pID = str(subs['problem']['contestId'])+str(subs['problem']['index'])
    if(pID==prob):
        if(f==False): 
            print('Submission found : ')
            print('----------------------------------------------------------------')
        print('SubmissionID - ' + str(subs['id']))
        subID = str(subs['id'])
        print('ProblemName - ' + str(subs['problem']['name']))
        print('Submission type - ' + str(subs['author']['participantType']))
        print('Tests passed - ' + str(subs['passedTestCount']))
        print('Verdict - ' + str(subs['verdict']))
        requrl = 'https://codeforces.com/contest/' + str(subs['contestId']) + '/submission/' + str(subs['id'])
        print()
        f=True
        break

if(f==False): 
    print('No submission found.')

if(requrl!='none'):
    print()
    req2 = requests.get(requrl)
    soup = BeautifulSoup(req2.content, 'html5lib')
    code = soup.find('pre', attrs = {'id':'program-source-text'})
    print(code.text)
    with open(str(subID)+'.txt','w') as f:
        f.write(code.text)
