import datetime
import dicttoxml
import xlrd
import sys
import copy
from feedgen.feed import FeedGenerator
from pymongo import MongoClient
import re
import requests
from flask import jsonify

from flask import request, render_template, Flask, redirect, url_for
app = Flask(__name__)

class reigon:
    def __init__(self, region):
        self.region = region

#get the xls form
#get the data by xlrd
class Entry:
     def __init__(self,id,title):
        self.id = id
        self.title = title
class Details:
     def __init__(self,name,record):
         self.name = name
         self.record = record
class para:
    def __init__(self,region,required):
        self.region = region
        self.required = required
def open_datafile(file_name):
    try:
        data = xlrd.open_workbook(file_name)
        return data
    except Exception:
        sys.exit()

def parse_the_data(file_name,region):
    data = open_datafile(file_name)
    table = data.sheets()[0]
    entry = {}
    record_all={}
    record = {}
    record_details = {}
    # only the 17 offence group is ok
    for i in range(7,24):
        value = table.row_values(i)
        year = 2012
        if i == 7:
            title = "Murder"
        else:
            title = value[1]
        for j in range(2,12,2):
            record_details['Num of incidents'] =  value[j]
            record_details['Rate per 100000 population'] =  value[j+1]
            record[str(year)] = copy.deepcopy(record_details)
            year +=1
        record_all[title] = record
    entry["name"] = region
    entry[region] = record_all
    return entry
def parse_xml(Meta):
    return dicttoxml.dicttoxml(Meta)

def feed_collection(region,local_url):
    fg = FeedGenerator()
    id_url = local_url + region
    fg.id(id_url)
    fg.title(region)
    fg.author({'name':'yujie'})
    fg.subtitle('atom format')
    fg.language('en')

    fe = fg.add_entry()
    fe.id(id_url)
    fe.title(region)
    fe.link(href = id_url)
    return fg

def feed_details(region,local_url,content):
    fg = FeedGenerator()
    id_url = local_url + region
    fg.id(id_url)
    fg.title(region)
    fg.author({'name': 'yujie'})
    fg.subtitle('atom format')
    fg.language('en')

    fe = fg.add_entry()
    fe.id(id_url)
    fe.title(region)
    fe.link(href=id_url)
    content_string = record_to_content(content)
    fe.content(content=content_string)
    return fg
def record_to_content(record):
    result = ''
    temp = ""
    temp_year = ""
    temp_name = " "
    for name in record:
        temp = ""
        for year in record[name]:
            temp = ""
            for item in record[name][year]:
                a = item+":"+str(int(record[name][year][item]))
                temp = temp +' '+ a
            c = name + ":" + year + ":" +temp
            result = result + c + "\n"
    return result


def getRECORD(name):
    records = user_records.find_one({"name":name})
    return records

def pushRECORD(record):
    user_records.insert_one(record)

def get_post_code_list(file_name):
    data = open_datafile(file_name)
    table = data.sheets()[0]
    nrows = table.nrows
    pos_set = []
    for i in range(1,nrows):
        value = table.row_values(i)
        postcode = str(int(value[2]))
        states = value[0]
        region = value[1]
        region = re.sub(r'[\s+"]', '', region)
        region = region.lower()
        if states ==  "New South Wales":
            pos_set.append(region)
    return set(pos_set)

@app.route('/test', methods=["POST", "GET"])
def add_entry():
    lganame = request.values.get("lgaName")
    postcode = request.values.get("postcode")
    region_name = request.values.get("Regionname")
    typeformat = request.values.get("requiredtype")
    delete_name = request.values.get("Deletename")
    if (delete_name is not None):
        delete_name = re.sub(r'[\s+"]', '', delete_name)
        delete_name = delete_name.lower()
        return redirect(url_for("delete_an_entry",name=delete_name))
    elif region_name is not None and  request.method == 'GET':
        region_name = re.sub(r'[\s+"]', '', region_name)
        region_name = region_name.lower()
        para.region = region_name
        para.required = typeformat
        return redirect(url_for("get_detail_entry", name=region_name))
    elif request.method == 'GET' and region_name is None:
        return render_template("test.html")
    else:
        if postcode is not None:
            #get the name
            pos_dict = getRECORD("Postcode")
            if postcode in pos_dict["pos"]:
                region_list = pos_dict["pos"][postcode]
                pos_result = []
                for i in range(len(region_list)):
                    lganame = region_list[i]
                    lganame = re.sub(r'[\s+"]', '', lganame)
                    lganame = lganame.lower()
                    all_states = getRECORD("region")
                    all_region = all_states["region"]
                    if lganame in all_region:
                        record = getRECORD(lganame)
                        if record is not None:
                            feed1 = feed_collection(lganame, local_url)
                            result = feed1.atom_str(pretty=True).decode("utf-8")
                            # print(result)
                            pos_result.append([result,200])
                        else:
                            download_url = host_url + lganame + "lga.xlsx"
                            download_file = lganame + "lga.xlsx"
                            file = requests.get(download_url)
                            with open(download_file, "wb") as code:
                                code.write(file.content)
                            new_entry = parse_the_data(download_file, lganame)
                            pushRECORD(new_entry)
                            feed_new = feed_collection(lganame, local_url)
                            result = feed_new.atom_str(pretty=True).decode("utf-8")

                            pos_result.append([result,201])
                    else:
                        return "the poscode does not meet the demand", 404
                pos_string = []
                pos_status = []
                for i in range(len(pos_result)):
                    pos_status.append(pos_result[i][1])
                    pos_string.append(pos_result[i][0])
                all_result = "\n".join(pos_string)
                if 201 in pos_status:
                    return all_result, 201
                else:
                    return all_result,200
            else:
                return "wrong number",400
#            return redirect(url_for("entry"))
        elif lganame is not None:
#            return redirect(url_for("entry"))
            lganame = re.sub(r'[\s+"]','', lganame)
            lganame = lganame.lower()
            all_states = getRECORD("region")
            all_region = all_states["region"]
            if lganame in all_region :
                record = getRECORD(lganame)
                if record is not None:
                    feed1 = feed_collection(lganame,local_url)
                    result = feed1.atom_str(pretty= True).decode("utf-8")
                    #print(result)

                    return result,200
                else:
                    download_url = host_url + lganame + "lga.xlsx"
                    download_file = lganame+"lga.xlsx"
                    file = requests.get(download_url)
                    with open(download_file, "wb") as code:
                        code.write(file.content)
                    new_entry =parse_the_data(download_file,lganame)
                    pushRECORD(new_entry)
                    feed_new = feed_collection(lganame,local_url)
                    result = feed_new.atom_str(pretty=True).decode("utf-8")
                    return result, 201
            else:
                return "the url does not exist", 404

@app.route('/test/collection',methods = ['GET'])
def get_all_entry():
    data_type = request.values.get("Type")
    database = []
    if data_type == "JSON":
        for post in user_records.find():
            if (post['name'] !=  'region' )and (post['name'] != 'Postcode'):
                title = post['name']
                id = local_url + post["name"]
                database.append(Entry(id,title))
        return jsonify([st.__dict__ for st in database]), 200
    else:
        for post in user_records.find():
            if (post['name'] !='region')and (post['name'] != 'Postcode'):
                lganame = post['name']
                feed_new = feed_collection(lganame, local_url)
                result = feed_new.atom_str(pretty=True).decode("utf-8")
                database.append(result)
        all_result = "\n".join(database)
        return  all_result,200


@app.route('/test/<name>',methods =['GET'])
def get_detail_entry(name):
    data_type = para.required
    database = []

    if data_type == "JSON":
        record_total = getRECORD(name)
        if record_total is not None:
            record = record_total[name]
            record_name =  record_total["name"]
            database.append(Details(name,record))
            para.required = None
            return jsonify([st.__dict__ for st in database]), 200
        else:
            return "The entry is not in the database",400
    else:
        record_total = getRECORD(name)
        if record_total is not None:
            record = record_total[name]
            record_name = record_total["name"]
            feed1 = feed_details(record_name,local_url,record)

            result = feed1.atom_str(pretty=True).decode("utf-8")
            return result,200
        else:
            return "the entry is not in the database",400
@app.route('/delete/<name>',methods = ['GET','POST','DELETE'])
def delete_an_entry(name):
    if request.method == "DELETE":
        record = getRECORD(name)
        if record is not None:
            user_records.remove(record)
            return "the required is removed", 200
        else:
            return "the name is not in the database", 400
    else:
        record = getRECORD(name)
        if record is not None:
            user_records.remove(record)
            return redirect(url_for("add_entry")) ,200
        else:
            return  "the name is not in the database",400
@app.route('/',methods=['GET'])
def main_page():
    return redirect(url_for('add_entry'))



if __name__ == "__main__":
    MONGODB_URI = "mongodb://reggie:reggie@ds261929.mlab.com:61929/crime"
    client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
    db = client.get_database("crime")
    user_records = db.user_records
    host_url = "http://www.bocsar.nsw.gov.au/Documents/RCS-Annual/"
    local_url = "http://localhost:5000/"
    para.region=""
    para.required = None
#    file = "bluemountainslga.xlsx"

#    feed_1 = feed_collection("bluemountains",local_url)
#    print(feed_1.atom_str(pretty=True))
#    feed_1.atom_file("1.xml")

#    poc = get_post_code_list(file)
#    record = {}
#    record["name"] = "region"
#    record["region"] = list(poc)
#    pushRECORD(record)
#    print(poc)
#    feed = feed("bluemountain")
 #   print(feed.atom_str(pretty=True))
    app.run()
