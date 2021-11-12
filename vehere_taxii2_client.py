from cytaxii2 import cytaxii2
import logging
from linesout import *
from load_config import *
from utils import *

all_collections = [] # All collections in default api root
all_collection_ids = []  # All collection id in collection in default api root
all_objects = []
type_address = []

#Create and configure logger
logging.basicConfig(filename="taxiiclient.log",format='%(asctime)s :  %(message)s',filemode='a') 
#Creating an object
log=logging.getLogger()
#Setting the threshold of logger to DEBUG
log.setLevel(logging.DEBUG)


def connect_and_discover(url,username,password,version=VERSION):
    # Instantiate server and get API Root
    cytaxii_object = cytaxii2.cytaxii2(discovery_url=url,username=username, password=password, version=version)
    log.info("Created Cytaxii Object")
    discovery_response = cytaxii_object.discovery_request()
    debug_L2_print("====== Discovery Response =======")
    print_object(discovery_response)     # will print object if config, PRINT OBJECT is set to True.
    root_discovery_response = cytaxii_object.root_discovery()
    debug_L2_print("====== Root Discovery Response =======")
    print_object(root_discovery_response)  # will print object if config, PRINT OBJECT is set to True.
    log.info("Root discovered")
    debug_L2_print("==========  Connected and Discovered Successfully  ==========")
    log.info("Connected and Discovered Successfully")
    return cytaxii_object

# Getting list of collections form root api
def get_collections(cytaxii_object : cytaxii2.cytaxii2):
    collections = cytaxii_object.collection_request()
    log.info("Got list of collections from root API. ")
    print_object(collections)
    return collections['response']['collections']

# Get the Collection info by collection id
def get_collections_data(cytaxii_object : cytaxii2.cytaxii2,collection_id):
    collection_data = cytaxii_object.collection_data_request(collection_id=collection_id)
    print_object(collection_data)
    return collection_data

# Pull the data from the collection with Collection ID and filters including added_after, limit, object_id
def pull_data(cytaxii_object : cytaxii2.cytaxii2,collection_id,added_after=None, limit=None, object_id=None,next=None):
    poll_response = cytaxii_object.poll_request(collection_id=collection_id, added_after=added_after, next=next, limit=limit, object_id=object_id)
    print_object(poll_response)
    return poll_response


def main():
    log.info("Program started running")
    COLLECTION_IDs = []
    # Get added_after value 
    ADDED_AFTER = get_added_after()
    log.info("Got ADDED AFTER value : " + str(ADDED_AFTER))

    # Create an object, Connect to Taxii server & Discover 
    cytaxii_object = connect_and_discover(url=URL, username=USERNAME, password=PASSWORD)
    
    # This will get all the collections in default api root url.
    all_collections = get_collections(cytaxii_object)

    log.info("Number of collections got : " + str(len(all_collections)))

    # Get all the Collection ids in an arr
    for collection in all_collections:
        all_collection_ids.append(collection["id"])

    # iterate through all the collection_ids to get all the readable objects in an array (all_objects)
    for id in all_collection_ids:
        if get_collections_data(cytaxii_object,collection_id=id)['response']['can_read'] == True:
            polled_data = pull_data(cytaxii_object,collection_id=id,added_after=ADDED_AFTER)
            objects = polled_data["response"]['objects']
            for object in objects:
                all_objects.append(object)

            # Check for pagination by puting next vaules in filter 
            while polled_data['response']['more']:
                next = int(polled_data['response']['next'])
                polled_data = pull_data(cytaxii_object,collection_id=id,next=next,added_after=ADDED_AFTER)
                all_objects.extend(polled_data['response']['objects'])

    # parse all the objects we got and process
    for object in all_objects: 
        parse_object(object)
        store_data(object)  # store for backup, feedback, maintainance, experiment, improving, etc

    do_filter_csv()
    update_added_after()

main()