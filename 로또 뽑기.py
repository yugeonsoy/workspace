import random

for i in range(10):
    a=list(map(int,input('구입한 번호?').split()))

    print(a)

    b=random.sample(range(46),6)
    print('당첨번호:',b)
    c=0
    for i in range(6):
        if a[i] in b:
            c=c+1
    print('맞은 갯수:',c)

    if c==6:
        print('1등')
    elif c==5:
        print('2등')
    elif c==4:
        print('3등')

    else:
        print('꽝')