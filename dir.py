import os
import shutil

# 1
os.makedirs("project/data/files")
print("Nested directories created.")

with open("project/data/files/test.txt", "w") as f:
    f.write("Hello Ramazan!")

# 2
print("\nFiles and folders in project directory:")
for item in os.listdir("project"):
    print(item)

# 3
print("\nFinding .txt files:")

for root, dirs, files in os.walk("project"):
    for file in files:
        if file.endswith(".txt"):
            print(os.path.join(root, file))

# 4
os.makedirs("backup")

shutil.copy("project/data/files/test.txt", "backup/test_copy.txt")
print("\nFile copied to backup.")

shutil.move("backup/test_copy.txt", "project/test_moved.txt")
print("File moved to project folder.")