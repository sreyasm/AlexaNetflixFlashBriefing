def lambda_handler(event, context):
    # USA Netflix
    usa_dict = get_content_for_region("usa")
    save_to_s3("usa", generate_json_from_dict("usa",usa_dict))

    # UK Netflix
    uk_dict = get_content_for_region("uk")
    save_to_s3("uk", generate_json_from_dict("uk", uk_dict))

    # ANZ Netflix
    anz_dict = get_content_for_region("anz")
    save_to_s3("anz", generate_json_from_dict("anz", anz_dict))

    # CAN Netflix
    can_dict = get_content_for_region("can")
    save_to_s3("can", generate_json_from_dict("can", can_dict))
    return "success"

# This function returns a dictionary of two lists of strings with keys: "added" and "removed"
# This contains the added and removed content for a given region.
def get_content_for_region(region):
    import requests
    from lxml import html

    html_raw = requests.get("https://" + region + ".newonnetflix.info/").content
    html_tree = html.fromstring(html_raw)

    removed_content = map(str.strip, html_tree.xpath("/html/body/div/section/a/span/text()"))
    added_content = map(str.strip, html_tree.xpath("/html/body/div/article/header/h1/a/text()"))

    # Some regions' websites do not have a hyperlink for the movie information
    if all(False for _ in added_content):
        added_content = map(str.strip, html_tree.xpath("/html/body/div/article/header/h1/text()"))

    return {
            "removed":list(removed_content),
            "added":list(added_content)
    }


# Returns the text that AVS should dictate given the dictionary returned from
# get_content_for_region(region)
def generate_speech_from_content(content):
    speech = "The TV shows and movies removed from Netflix this week are: "
    speech += speech_list_builder(content["removed"])
    """for movie in content["removed"][:-1]:
        speech += movie + ", "
    speech += "and " + content["removed"][-1] + "."
    """
    speech += " The TV shows and movies added to Netflix this week are: "
    speech += speech_list_builder(content["added"])
    return speech


# Helper function to convert a list of movies to a single speakable string.
def speech_list_builder(movies):
    speech = ""
    for movie in movies[:-1]:
        speech += movie + ", "
    speech += "and " + movies[-1] + "."
    return speech


# Generates the JSON payload that AVS needs given the region and dictionary
# returned from get_content_from_region
def generate_json_from_dict(region, source_dict):
    import json
    import uuid
    import datetime
    json_dict = {
        "uid": "urn:uuid:" + str(uuid.uuid4()),
        "updateDate": str(datetime.datetime.utcnow().isoformat()) + "Z",
        "titleText": "What's new on Netflix " + region.upper(),
        "mainText": generate_speech_from_content(source_dict),
        "redirectionUrl": "https://" + region + ".newonnetflix.info/"
    }
    return json.dumps(json_dict)


# Uploads the JSON document to an S3 bucket given the region
# and JSON data as a string
def save_to_s3(region, json_data):
    import boto3
    BUCKET_NAME = "new-on-netflix-feeds"
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(BUCKET_NAME)
    obj_name = "alexa-" + region + ".json"
    bucket.put_object(
        ACL="public-read",
        ContentType="application/json",
        Key=obj_name,
        Body=json_data,
    )
