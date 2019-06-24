import boto3
import argparse
import json


# for command line usage
ap = argparse.ArgumentParser()
ap.add_argument("-k", "--access_key", type=str,
                help="AWS Access Key ID")
ap.add_argument("-s", "--secret_key", type=str,
                help="AWS Secret Access Key")
ap.add_argument("-i", "--image_names", type=str, 
				default="image_urls_to_id_name.txt",
				help="Text file with names of images to send to mturk " + 
				"for labeling")
ap.add_argument("-d", "--deploy", type=str, default="False",
				help="enter true, y, or 1 if you are deploying. false, " + 
				"n, or 0 to test")
ap.add_argument("-l", "--layout_id", type=str, 
				help="enter the layout id available by clicking on the" +
				     "project name in your requester account")
ap.add_argument("-t", "--type_id", type=str, 
				help="enter the type id available by clicking on the" +
				     "project name in your requester account")
args = vars(ap.parse_args())


# parse command line arguments
access_key = args["access_key"]
secret_key = args["secret_key"]
file_name = args["image_names"]
layout_id = args["layout_id"]
type_id = args["type_id"]
testing = args["deploy"]

# generate list of image_urls (hosted on an AWS s3 bucket)
def get_naming_dictionary():
	f = open(file_name, "r")
	json_string = f.read().replace("'","\"")
	json_string = json_string.replace("(", "[")
	json_string = json_string.replace(")", "]")
	#print(json_string)
	f.close()
	return json.loads(json_string)
naming_dictionary = get_naming_dictionary()
image_urls = []
for key in naming_dictionary:
	image_urls.append(key)

	
# determines endpoint_url
if testing.lower() in ["true", "y", "yes", "1", "yeah", "t"]:
	endpoint_url = ""
elif testing.lower() in ["false", "n", "no", "0", "nope", "f"]:
	endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
else:
	raise argparse.ArgumentTypeError("please provide a boolean " + 
	                                 "value for '--testing'")
	

# Create your connection to MTurk
mtc = boto3.client('mturk', aws_access_key_id=access_key,
aws_secret_access_key=secret_key,
region_name='us-east-1', 
endpoint_url = endpoint_url)


# Create an HIT for each image url
for image in image_urls:
	response = mtc.create_hit_with_hit_type(
	  HITLayoutId    = layout_id,
	  HITLayoutParameters = [ {'Name': 'image_url', 'Value': image } ],
	  HITTypeId      = type_id,
	  LifetimeInSeconds = 600
	)

