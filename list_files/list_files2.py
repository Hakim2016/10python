import os
import os.path
def print_dir(sPath):
 for sChild in os.listdir(sPath):
  sChildPath = os.path.join(sPath,sChild)
  if os.path.isdir(sChildPath):
   print_dir(sChildPath)
  else:
   print(sChildPath)

def Test():
	path = r'F:\GITSVN\040_SCM\050_User Manual\020_HEA\GSCM User Manual'
	print_dir(path)

Test()