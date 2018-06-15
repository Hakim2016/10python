import os
cookie_path = '../sessions/'

if os.path.exists(cookie_path):
    print('exist !')
    pass
else:
    print('this path need to create!')
    cookie_path = ''

print(cookie_path)