import os
from datetime import datetime, timedelta
import csv
from linesout import *
from load_config import *


# This algorithm is used to parse the object and add the required values to our local list
def parse_object(object):
    pattern_status = True
    if object['type'] == 'indicator':
        try:
            valid_until = object['valid_until']
            valid = check_validity(valid_until)
            if not valid:
                return
        except:
            pass

        pattern_value = object['pattern']

        debug_L1_print("Pattern value type : " + str(type(pattern_value)))
        debug_L1_print(pattern_value)

        pattern_type_value = pattern_value.split(":")[0][1:]
        indicator_value = pattern_value.split("'")[-2]

        # debug_L1_print(pattern_type_value,indicator_value)

        if pattern_type_value in pattern_value:
            temp_path = PATH + 'indicators/' + str(pattern_type_value) + '.txt'

            debug_L1_print(temp_path)

            if check_list(temp_path,indicator_value):
                try:
                    valid_until = object['valid_until']
                    update_csv(indicator_value,valid_until,temp_path)
                except:
                    update_list(temp_path,indicator_value)

        if pattern_status == False:
            debug_L2_print("Handle different pattern status here.")
    else:
        debug_L2_print("Handle different Object type here , Object Type : " + object['type'])
        object_type = object['type']
        try:
            pattern_value = object['pattern']
        except:
            debug_L2_print("Can't find pattern field in the object ; ")
            return

        debug_L1_print("Pattern value type : " + str(type(pattern_value)))
        debug_L1_print(pattern_value)

        pattern_type_value = pattern_value.split(":")[0][1:]
        indicator_value = pattern_value.split("'")[-2]

        debug_L1_print(pattern_type_value,indicator_value)

        if pattern_type_value in pattern_value:
            pattern_type_value = pattern_type_value.replace('.','_').replace("'",'')
            temp_path = PATH + object_type + '/' + str(pattern_type_value) + '.txt'

            debug_L1_print(temp_path)

            if check_list(temp_path,indicator_value):
                update_list(temp_path,indicator_value)

        if pattern_status == False:
            debug_L2_print("Handle different pattern status here.")


# This function is used to check and avoid repeated values in our local list.
def check_list(path,value):
    if not os.path.exists(path):
        try:
            with open(path, 'w') as fp:
                pass   
        except FileNotFoundError:
            dir_name = path.split('/')[-2]
            try:
                os.mkdir(PATH + dir_name)
            except:
                pass
            with open(path, 'w') as fp:
                pass
    else:
        with open(path, 'r') as f:
            data = f.read().split('\n')
            if value in data:
                return False
            else:
                return True
        return True


# This function is used to update our local list for ruleengine 
def update_list(path,value):
    with open(path,'a') as f:
        f.write(value)
        f.write('\n')


def get_added_after():
    filename = 'added_after.txt'
    res = ''
    # mins = 60  # 1 hour
    # seconds = 60 * mins
    # time_to_cut = timedelta(seconds=seconds)

    if not os.path.exists(filename):
        with open(filename, 'w') as fp:
            pass   
        return None
    else:
        with open(filename, 'r') as f:
            res = f.read()
            # with open(filename, 'w') as f:
            #     f.write(str(curr_time - time_to_cut))
            debug_L1_print("Get Added after value: " + res)
            return res


def get_list(path,value=None):
    if not os.path.exists(path):
        try:
            with open(path, 'w') as fp:
                pass   
        except FileNotFoundError:
            dir_name = path.split('/')[-2]
            os.mkdir(PATH + dir_name)
            with open(path, 'w') as fp:
                pass
    else:
        with open(path, 'r') as f:
            data = f.read().split('\n')
            return data


def store_data(object):
    path = 'all_objects/all_objects.json'
    if not os.path.exists(path):
        try:
            with open(path, 'w') as fp:
                pass   
        except FileNotFoundError:
            dir_name = 'all_objects'
            try:
                os.mkdir(dir_name)
            except:
                pass
            with open(path, 'w') as fp:
                pass
    with open(path, 'a') as f:
            f.write(json.dumps(object,indent=4))
            f.write('\n')

def update_added_after():
    filename = 'added_after.txt'
    curr_time = datetime.now()
    # mins = 60  # 1 hour
    # seconds = 60 * mins
    # time_to_cut = timedelta(seconds=seconds)
    days = 1
    time_to_cut = timedelta(days=days)
    with open(filename, 'w') as f:
        f.write(str(curr_time - time_to_cut))

def check_validity(valid_until):
    valid_until = valid_until[:-1]
    valid_time_obj = datetime.strptime(valid_until, '%Y-%m-%dT%H:%M:%S')
    now_time = datetime.now()
    if valid_time_obj < now_time:
        return False
    else:
        return True

# def get_last_expired(filename = 'last_expired.txt'):
#     with open(filename, 'r') as f:
#         return f.read()

# def update_last_expired(filename = 'last_expired.txt'):
#     with open(filename, 'w') as f:
#         f.write(str(datetime.now()))

# def remove_expired_values():
#     last_expired_time = get_last_expired()

def update_csv(value,valid_until,temp_path):
    valid_until = valid_until[:-1]
    valid_until = valid_until.replace("T",' ')
    with open(temp_path[:-4] + "_value_and_validity.csv",'a') as f:
        data_line = csv.writer(f)
        data_line.writerow([value,valid_until])


def do_filter_csv(path=(PATH + 'indicators/')):
    filename="_value_and_validity.csv"
    all_files = os.listdir(path)
    temp_csv = []
    for file in all_files:
        if filename in file:
            temp_csv.append(file)
        
    for file in temp_csv:
        new_list = []
        update_csv_valid_until = []
        with open(path + file,'r') as f:
            data_lines = csv.reader(f)
            for data in data_lines:
                value = data[0]
                valid_until = data[1]
                valid_until = datetime.strptime(valid_until,'%Y-%m-%d %H:%M:%S')
                if datetime.now() > valid_until:
                    continue
                else:
                    new_list.append(value)
                    update_csv_valid_until.append(valid_until)

        filename = file.replace('_value_and_validity','_with_validity')
        with open(path + filename,'w') as f:
            data_lines = csv.writer(f)
            for value in new_list:
                data_lines.writerow([value])
        
        with open(path + file,'w') as f:
            data_lines = csv.writer(f)
            for i in range(len(new_list)-1):
                # data_lines.writerow([value,valid_until])
                data_lines.writerow([new_list[i],update_csv_valid_until[i]])

# 1  DONE
# make history added after file.
# from datetime import datetime, timedelta
# curr_datetime = datetime.now()
# time_to_cut = 60*60 (60 seconds * 60 mintues)
# write(str(curr_datetime - time_to_cut))
# 

# 2 
# dont read the file every time for checking,
# (a) if got the value in the returned objects, 
# (b) load once and 
# (c) check from there 
# (d) at the end overwrite all those to respective files

# 3  DONE
# while updating our list(database) replace the '.', "'", with '_' and '' respt.

# 4  DONE
# for feedback and improving and experimenting, store & append all the objects in a json file,

# 5 NOT NECESSARY , EVERY THING WILLL BE ADDED TO DEFAULT ONE, ELSE THE LIBRARY WILL BE UPDATED
# Explore all the API Roots not only default one

# 6  DONE
# check value of 'more' for 'true', if true, explore(poll) again with filter value next