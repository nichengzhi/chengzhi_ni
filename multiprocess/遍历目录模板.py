import os
path = "C:\\SDG_contain_sustainability_report\\"
for root, dirs, files in list(os.walk(path)) :
    for i in files :
        if i.endswith('.pdf') or i.endswith('.10w') :
            print(root + "\\" + i)