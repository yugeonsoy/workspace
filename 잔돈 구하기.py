a=int(input('과자가격은?'))
b=int(input('낸돈?'))


c=b-a
print('잔돈',c)
print('1000원짜리',c//1000)


c=c%100

print('500원짜리',c//500)
print('100원짜리',c%100)
print('50원짜리',c//50)
print('10원짜리',c//10)
print('거래완료!')