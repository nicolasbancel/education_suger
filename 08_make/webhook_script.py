import requests

webhook_url = "https://hook.eu2.make.com/th2zddpmb1lfg98838589nj7wwggpagj"

path_file2 = "/Users/nicolasbancel/git/education_suger/00_1ères_STD2A_maths/annales/STD2A_Metropole_19_juin_2018-DV.pdf"
path_file1 = "/Users/nicolasbancel/git/education_suger/00_1ères_STD2A_maths/annales/STD2A_Metropole_6_septembre_2018_DV.pdf"

files = [
    ("file1", open(path_file1, "rb")),
    ("file2", open(path_file2, "rb")),
]

response = requests.post(webhook_url, files=files)
print(response.status_code, response.text)
