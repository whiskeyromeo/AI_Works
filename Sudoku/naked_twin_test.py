from solution_test import TestNakedTwins
from solution import *

values = TestNakedTwins.before_naked_twins_1

testVals = naked_twins(values)

set1 = set(values.items())
set2 = set(testVals.items())
 
print('******************\n\n')
print('difference before test: ')
print( set1 ^ set2 )

reqVals = TestNakedTwins.possible_solutions_1[1]
set3 = set(reqVals.items())


reqVals = TestNakedTwins.possible_solutions_1[0]
set4 = set(reqVals.items())


print('difference after test - solutions1: ')
print( set2 ^ set3 )
print('******************\n\n')


print('difference after test - solutions2: ')
print( set2 ^ set4 )
print('******************\n\n')

print(testVals)
