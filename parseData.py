
import csv
import datetime
import time
from pathlib import Path

from fit_tool.fit_file_builder import FitFileBuilder
from fit_tool.profile.messages.blood_pressure_message import BloodPressureMessage
from fit_tool.profile.messages.file_id_message import FileIdMessage
from fit_tool.profile.profile_type import FileType, HrType


def createFitFile(csvfilename,fields):

    builder = FitFileBuilder()

    message = FileIdMessage()
    message.type = FileType.BLOOD_PRESSURE
    message.timeCreated = round(datetime.datetime.now().timestamp() * 1000)

    builder.add(message)
    with open(csvfilename, 'r') as csvfile:
        # Create a reader object
        reader = csv.DictReader(csvfile)
        for line in reader:
            #print(line['Date'], line['Systolic'])

            message = BloodPressureMessage()
            message.systolic_pressure = int(line[fields['Systolic']])
            message.diastolic_pressure = int(line[fields['Diastolic']])
            timeString = line[fields['Time']]
            dateString = line[fields['Date']]
            message.heart_rate = int(line[fields['Pulse']])
            timeVar = time.mktime(
                datetime.datetime.strptime(dateString + " " + timeString, fields['DatePattern']+ " "+fields['TimePattern']).timetuple())

            message.timestamp = int(timeVar*1000)
            if fields['HeartRateIrregularityPattern'] in line[fields['HeartRateIrregularity']]:
                message.heart_rate_type = HrType.IRREGULAR
            else:
                message.heart_rate_type = HrType.NORMAL
            builder.add(message)
    fit_file = builder.build()

    filenameWithoutExtension= str(Path(csvfilename).with_suffix("")) + "_processed"
    out_path = filenameWithoutExtension+".fit"
    fit_file.to_file(str(out_path))
    csv_path = filenameWithoutExtension+".csv"
    fit_file.to_csv(str(csv_path))


fields= {
    "Systolic": "Systolic",
    "Diastolic": "Diastolic",
    "Date": "Date",
    "DatePattern": "%Y-%m-%d",
    "Time": "Time",
    "TimePattern": "%H:%M:%S",
    "HeartRateIrregularity": "Notes",
    "Pulse": "Pulse",
    "HeartRateIrregularityPattern": "Herzschlag festgestellt"
}

createFitFile("OmronRefactored.csv",fields)
