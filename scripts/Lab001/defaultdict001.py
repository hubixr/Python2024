from collections import defaultdict

# dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
# print(dict['z'])

# dict = defaultdict(int)

# print('z' in dict)
# print(dict['z'])

dict = defaultdict(lambda: 5)

print('z' in dict)
print(dict['z'])