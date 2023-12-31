import argparse
import os
from datetime import datetime
import pandas as pd
import logging
import csv

class CustomArgumentParser(argparse.ArgumentParser):
    def __init__(self):
        super(CustomArgumentParser, self).__init__()
        self.add_argument('--inputFile', type=str, help='Enter File name and file must exist e.g: example.csv')
        self.add_argument('--range', type=str, help='Enter range of date "YYYY-MM-DD to YYYY-MM-DD"')
        self.add_argument('--output', type=str, help='Enter export file name only .csv and .txt extensions is allowed ')
        self.add_argument('--max', type=str, help='Enter column name which you want to get maximum occurance example: Station.City(s)')
        self.add_argument('--getLocation', type = str, help='It will return location of maximum average temprature(s)')
        self.add_argument('--explain', type = str, help='It will expain all information about the given file')
        self.add_argument('--averageData', nargs='*', type = str, help='It will print state, year, month and day of maximum temprature')

    def validate_args(self, args):

        if args.range and not Validate.validate_date_range(args.range):
            logging.info("Invalid date range format. Please provide a valid range.")
            return

        if args.output and not Validate.validate_file_format(args.output, allowed_extensions=[".csv", ".txt"]):
            logging.info("Invalid file format. Please provide a valid format.")
            return

        if args.inputFile and not os.path.isfile(args.inputFile):
            logging.info("File not found. Please provide a valid file.")
            return

        if args.range and args.inputFile and not Validate.validate_date_in_csv(args.inputFile, args.range):
            logging.info("date not found")
            return

        if args.range and not Validate.validate_date_range(args.range):
            logging.info("date can't be grater")
            return

        if args.max and args.inputFile:
            logging.info(f"Maximum is {fileFunctions.find_state_with_maximum_occurrence(args.max, args.inputFile)}")

        if args.output and args.inputFile and args.range:
            export(args)
        
        if args.explain:
            fileFunctions.explain(args.explain)

        if args.averageData==[] and args.range:
            result = analyzeState(args)
            logging.info(f"State is {result[0]}")
            logging.info(f"Year is {result[1]}")
            logging.info(f"Month is {result[2]}")
            logging.info(f"Day is {result[3]}")

        if args.getLocation and args.range:
            fileFunctions.location_range(args.getLocation,args.range)
        elif args.getLocation:
            fileFunctions.location(args.getLocation)


class Validate:
    def validate_date(date_range):
        date_format = '%Y-%m-%d'
        date_range = date_range.split(' to ')

        try:
            datetime.strptime(date_range[0], date_format)
            datetime.strptime(date_range[1], date_format)
        except ValueError:
            logging.info('Invalid date format. Please use YYYY-MM-DD.')
            return False
        
        return True

    def validate_file_format(file_path, allowed_extensions=None):
        _, file_extension = os.path.splitext(file_path)
        if allowed_extensions and file_extension.lower() not in allowed_extensions:
            logging.info(f"Error: Invalid file extension. Allowed extensions are {allowed_extensions}. Detected extension: {file_extension}.")
            return False

        return True

    def validate_date_in_csv(file_path, given_date):
        date_range = given_date.split(' to ')
        df = pd.read_csv(file_path)
        column_name = 'Date.Full'
        if date_range[0] not in df[column_name].values:
            logging.info(f"Date '{date_range[0]}' not found in the file '{file_path}'")
            return False

        if date_range[1] not in df[column_name].values:
            logging.info(f"Date '{date_range[1]}' not found in the file '{file_path}'")
            return False

        return True

    def validate_date_range(date_given):
        date_range = date_given.split(' to ')
        start_date = date_range[0]
        end_date = date_range[1]

        if datetime.strptime(start_date, '%Y-%m-%d') > datetime.strptime(end_date, '%Y-%m-%d'):
            logging.info("Start date cannot be greater than end date.")
            return False

        return True
class fileFunctions:

    def find_state_with_maximum_occurrence(column,file_path):
        df = pd.read_csv(file_path)
        state_counts = df[column].value_counts()

        max_occurrence_state = state_counts.idxmax()

        return max_occurrence_state
    
    def explain(file_path):
        df = pd.read_csv(file_path)
        df['Date.Full'] = pd.to_datetime(df['Date.Full'])
        df['Date.Full'] = df['Date.Full'].dt.date
        df['Data.Temperature.Avg Temp'] = pd.to_numeric(df['Data.Temperature.Avg Temp'])
        df['Data.Temperature.Max Temp'] = pd.to_numeric(df['Data.Temperature.Max Temp'])
        df['Data.Temperature.Min Temp'] = pd.to_numeric(df['Data.Temperature.Min Temp'])
        df['Data.Wind.Direction'] = pd.to_numeric(df['Data.Wind.Direction'])
        df['Data.Wind.Speed'] = pd.to_numeric(df['Data.Wind.Speed'])
        min_date = df['Date.Full'].min()
        min_temp = df['Data.Temperature.Avg Temp'].min()
        min_max_temp = df['Data.Temperature.Max Temp'].min()
        min_min_temp = df['Data.Temperature.Min Temp'].min()
        min_wind_direction = df['Data.Wind.Direction'].min()
        min_wind_speed = df['Data.Wind.Speed'].min()
        max_temp = df['Data.Temperature.Avg Temp'].max()
        max_max_temp = df['Data.Temperature.Max Temp'].max()
        max_min_temp = df['Data.Temperature.Min Temp'].max()
        max_wind_direction = df['Data.Wind.Direction'].max()
        max_wind_speed = df['Data.Wind.Speed'].max()
        max_date = df['Date.Full'].max()
        empty_entries=[]
        empty_entries.append(df['Data.Precipitation'].isnull().sum())
        empty_entries.append(df['Date.Full'].isnull().sum())
        empty_entries.append(df['Date.Month'].isnull().sum())
        empty_entries.append(df['Date.Week of'].isnull().sum())
        empty_entries.append(df['Date.Year'].isnull().sum())
        empty_entries.append(df['Station.City'].isnull().sum())
        empty_entries.append(df['Station.Code'].isnull().sum())
        empty_entries.append(df['Station.Location'].isnull().sum())
        empty_entries.append(df['Station.State'].isnull().sum())
        empty_entries.append(df['Data.Temperature.Avg Temp'].isnull().sum())
        empty_entries.append(df['Data.Temperature.Max Temp'].isnull().sum())
        empty_entries.append(df['Data.Temperature.Min Temp'].isnull().sum())
        empty_entries.append(df['Data.Wind.Direction'].isnull().sum())
        empty_entries.append(df['Data.Wind.Speed'].isnull().sum())
        print(empty_entries)
        logging.info(f'''      Minimum date is {min_date}  
                  Maximum date is {max_date}
                  Minimum average temprate is {min_temp} 
                  Minimum max_temprate is {min_max_temp}''')
        logging.info(f'''      Minimum min temprate is {min_min_temp}
                  Minimum wind direction is {min_wind_direction}
                  Minimum wind speed is {min_wind_speed} 
                  Max_temprate is {max_temp}''')
        logging.info(f'''Maximum max temprate is {max_max_temp}
                  Maximum min temprature is {max_min_temp} 
                  Maximum wind direction is {max_wind_direction} 
                  Max wind speed is {max_wind_speed}''')


    def import_data(file_path):
        data_list = [] 
        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data_entry = {
                        'perception': row['Data.Precipitation'],
                        'date_full': row['Date.Full'],
                        'date_month': row['Date.Month'],
                        'date_week': row['Date.Week of'],
                        'date_year': row['Date.Year'],
                        'station': row['Station.City'],
                        'station_code': row['Station.Code'],
                        'station_location': row['Station.Location'],
                        'station_state': row['Station.State'],
                        'avg_temp': row['Data.Temperature.Avg Temp'],
                        'max_temp': row['Data.Temperature.Max Temp'],
                        'min_temp': row['Data.Temperature.Min Temp'],
                        'wind_direction': row['Data.Wind.Direction'],
                        'wind_speed': row['Data.Wind.Speed']
                    }
                    data_list.append(data_entry)
            logging.info(f"Imported data from {file_path}")
        except Exception as e:
            logging.error(f"Error importing data: {str(e)}")
        return data_list

    def analyze_data(start, end,dataaa):
        try:
            start_Date = datetime.strptime(start, "%Y-%m-%d")
            end_Date = datetime.strptime(end, "%Y-%m-%d")
            filtered_data = [entry for entry in dataaa if start_Date <= datetime.strptime(entry.get('date_full'), "%Y-%m-%d") <= end_Date]
            list = ([entry.get('avg_temp') for entry in filtered_data])
            max_temp = ([entry.get('max_temp') for entry in filtered_data])
            min_temp = ([entry.get('min_temp') for entry in filtered_data])
            wind_direction = ([entry.get('wind_direction') for entry in filtered_data])
            wind_speed = ([entry.get('wind_speed') for entry in filtered_data])
            average_temperature = sum(int(num) for num in list)/len(list)
            average_max_temperature = sum(int(num) for num in max_temp)/len(max_temp)
            average_min_temperature = sum(int(num) for num in min_temp)/len(min_temp)
            average_wind_direction = sum(int(num) for num in wind_direction)/len(wind_direction)
            average_wind_speed = sum(float(num) for num in wind_speed)/len(wind_speed)
            min_temperature = min(int(num) for num in list)
            max_temperature = max(int(num) for num in list)
            logging.info("Data is validating")
            return average_temperature, min_temperature, max_temperature,average_max_temperature,average_min_temperature,average_wind_speed,average_wind_direction
            
        except Exception as e:
            logging.error(f"Error analyzing data: {str(e)}")

    def state(start, end,dataaa):
        try:
            start_Date = datetime.strptime(start, "%Y-%m-%d")
            end_Date = datetime.strptime(end, "%Y-%m-%d")
            filtered_data = [entry for entry in dataaa if start_Date <= datetime.strptime(entry.get('date_full'), "%Y-%m-%d") <= end_Date]
            list = ([entry.get('avg_temp') for entry in filtered_data])
            min_temperature = min(int(num) for num in list)
            max_temperature = max(int(num) for num in list)
            state = ([entry.get('station_location','station_state') for entry in filtered_data if int(entry.get('avg_temp'))==max_temperature])
            month = ([entry.get('date_month') for entry in filtered_data if max_temperature==int(entry.get('avg_temp'))])
            year = ([entry.get('date_year') for entry in filtered_data if int(entry.get('avg_temp'))==min_temperature])
            day = ([entry.get('date_full') for entry in filtered_data if int(entry.get('avg_temp'))==min_temperature])
            logging.info("Data is validating")
            return state, year, month, day
            
        except Exception as e:
            logging.error(f"Error analyzing data: {str(e)}")

    def write_to_csv(file_name, data):
        try:
            with open(file_name, 'a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['Average Temprature is ' + str(data[0])])
                csv_writer.writerow(['Minimum Temprature is ' + str(data[1])])
                csv_writer.writerow(['Maximum temprature is ' + str(data[2])])
                csv_writer.writerow(['Average Maximum temprature is ' + str(data[3])])
                csv_writer.writerow(['Average Minimum temprature is ' + str(data[4])])
                csv_writer.writerow(['Avereage wind speed is ' + str(data[5])])
                csv_writer.writerow(['Average wind direction is ' + str(data[6])])
            logging.info(f'Data successfully written to {file_name}')
            return True
        except Exception as e:
            print(file_name)
            logging.info(f'Error writing to {file_name}: {e}')

    def location_range(file_path, date_range):
        dataa = fileFunctions.import_data(file_path)
        date_range = date_range.split(' to ')
        start_Date = datetime.strptime(date_range[0], "%Y-%m-%d")
        end_Date = datetime.strptime(date_range[1], "%Y-%m-%d")
        filtered_data = [entry for entry in dataa if start_Date <= datetime.strptime(entry.get('date_full'), "%Y-%m-%d") <= end_Date]
        list = ([entry.get('avg_temp') for entry in filtered_data])
        max_temperature = max(int(num) for num in list)
        state = ([entry.get('station','station_code') for entry in filtered_data if int(entry.get('avg_temp'))==max_temperature])
        location = ([entry.get('station_location','station_state') for entry in filtered_data if int(entry.get('avg_temp'))==max_temperature])
        print(state,location)

    def location(file_path):
        dataa = fileFunctions.import_data(file_path)
        list = ([entry.get('avg_temp') for entry in dataa])
        max_temperature = max(int(num) for num in list)
        state = ([entry.get('station','station_code') for entry in dataa if int(entry.get('avg_temp'))==max_temperature])
        location = ([entry.get('station_location','station_state') for entry in dataa if int(entry.get('avg_temp'))==max_temperature])
        print(state,location)

def calc(args):
    data = fileFunctions.import_data(args.inputFile)
    return data

def analyze(args):
    data = calc(args)
    date_range = args.range.split(' to ')
    result =fileFunctions.analyze_data(date_range[0], date_range[1], data)
    return result

def analyzeState(args):
    data = calc(args)
    date_range = args.range.split(' to ')
    result =fileFunctions.state(date_range[0], date_range[1], data)
    return result

def export(args):
    values = analyze(args)
    if values == None:
        logging.error("Doesnot found any data")
        return
    fileFunctions.write_to_csv(args.output, values)
