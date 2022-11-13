import json


file = open("tests.json", "r", encoding="utf-8")
test_data = json.load(file)

file = open("videos.json", "r", encoding="utf-8")
videos = json.load(file)