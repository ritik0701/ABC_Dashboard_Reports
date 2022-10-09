import csv 

def read_CSV(path):
    try:

        with open(path,newline='') as file:
            reader = csv.reader(file,delimiter=',')
            header = next(reader)
            return reader
               

    except Exception as exception:
        print('exception in reading file')
        return exception.__str__()