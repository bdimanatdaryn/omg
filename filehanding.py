#1
with open("Daryn","w") as f:
    f.write("The Earth is really big")


with open("Daryn") as f:
  print(f.read())

#2
with open("Daryn","r") as f:
   print(f.read(3))

#3
with open("Daryn","a") as f:
   f.write(" Now we have more lines")

with open("Daryn") as f:
   print(f.read())

#4
import shutil

shutil.copyfile("Daryn","work")

#5
import os

os.remove("Daryn")