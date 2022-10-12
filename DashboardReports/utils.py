import csv 
import dateutil.parser as parser

def read_CSV(path):
    try:

        data = []
        with open(path,newline='') as file:
            reader = csv.reader(file,delimiter=',')
            header = next(reader)
            for i in reader:
                data.append(i)
            return data

               

    except Exception as exception:
        print('exception in reading file')
        return exception.__str__()


def validate_date(date_string):
    date_time = parser.parse(date_string)
    return(date_time)
