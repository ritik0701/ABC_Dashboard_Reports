import csv 

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