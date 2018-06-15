__author__ = 'AlbertS'

import os
import os.path

def dfs_showdir(path, depth):
    if depth == 0:
        print("root:[" + path + "]")

    for item in os.listdir(path):
        if '.git' not in item:
            print("|      " * depth + "+--" + item)

            newitem = path +'/'+ item
            if os.path.isdir(newitem):
                dfs_showdir(newitem, depth +1)

if __name__ == '__main__':
	path = r'F:\GITSVN\040_SCM\050_User Manual\020_HEA\GSCM User Manual'
	# print_dir(path)
	dfs_showdir(path, 0)