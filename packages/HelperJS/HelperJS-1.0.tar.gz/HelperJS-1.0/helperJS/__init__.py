import json
import random
import re 

#Loading to json file.
def loadjson(filepath): 
    try:
        with open(filepath, 'r', encoding='utf-8') as jsonfile:
            return json.load(jsonfile)
    except Exception as e: return None

#Write to json file.
def dumpjson(data, filepath):
    try: 
        datas = loadjson(filepath)
        pop = 0
        for result in datas:
            if result['id'] == data['id']:
                datas[pop] = data
            else: pop=pop+1
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(datas, file, indent=4, ensure_ascii=False)
    except Exception as e: return None

#Adding a new dictionary to json.
def push(filepath, data):
    try:
        json_data = loadjson(filepath)
        json_data.append(data)
        with open(filepath, 'w', encoding='utf-8') as outfile:
            json.dump(json_data, outfile, indent=4, ensure_ascii=False)
    except Exception as e: return None

#Delete to json file.
def delete(filepath, id):
    try:
        data = loadjson(filepath)
        minimal = 0
        for person in data:
            if person["id"] == id:
                data.pop(minimal)
            else:
                minimal = minimal + 1
        with open(filepath, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)
            return True
    except Exception as e: return None
        
#Beautiful numbers.
def task(intenger):
    try:
        return re.sub(r'(?<!^)(?=(\d{3})+$)', r'.', f"{intenger}")
    except Exception as e: return None

#Maximum id.
def maxuId(filepath):
    try:
        data = loadjson(filepath)
        max_item = max(data, key = lambda item: int(item['uid']))
        return int(max_item['uid'])+1
    except Exception as e: return 0

#Random by chance.
def chance(chance, x=bool):
    status = random.choices([True, False], weights=[chance,100-chance], k=1)[0]
    if x is True:
        if status is True: x = [1, 2, 2.5, 5, 10]
        else: x = [0, 0.5, 0.25, 0.75]
        totalx = random.choice(x)
        return {"status": status, "bet": totalx}
    return {"status": status}

#Replace string to intenger.
def replace(string):
    try:
        text = string.replace('к', '000')
        text = text.replace('k', '000')
        return int(text)
    except Exception as e: return 0

#Find to user by id.
def find(object, id, filepath):
    try: return list(filter(lambda x: x[object]==id, loadjson(filepath)))[0]
    except Exception as e: return None