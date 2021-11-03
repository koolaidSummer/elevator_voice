import requests
import speech_recognition as sr
import re
import pymysql

dbUrl = "elevator-db.cdpfvc1hzmbi.ap-northeast-2.rds.amazonaws.com"
dbPort = 3306
dbId = "admin"
dbPwd = "kongys11"

floorArr = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']


def FloorToDB(selectedFloor):
    con = pymysql.connect(host=dbUrl, port=dbPort, user=dbId, password=dbPwd, db="elevator")
    cursor = con.cursor()
    sql = "INSERT INTO CTL_FLOOR_WEB (CTL_FLOOR_WEB) VALUES (%s)"
    cursor.execute(sql, selectedFloor)

    cursor.close()
    con.commit()
    con.close()


print("----------------------")
print("Voice_Recognize Start")
print("----------------------")
r = sr.Recognizer()

while (1):

    with sr.Microphone() as source:
        print("say destination floor!")
        audio = r.listen(source)

    try:
        str = r.recognize_google(audio, language='ko')
        justNumber = re.sub(r'[^0-9]', '', str)

        if justNumber in floorArr:
            print("Destination : " + justNumber)
            if justNumber != "":
                FloorToDB(justNumber)
    except sr.UnknownValueError:
        print("unkown value error")
    except requests.RequestException as e:
        print(e)
    print("----------------------")

