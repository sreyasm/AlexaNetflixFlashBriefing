def lambda_handler(event, context):
    usa_dict = get_content_for_region("usa")
    print(usa_dict)
    save_to_s3("usa",generate_json_from_dict("usa",usa_dict))


def get_content_for_region(region):
    import requests
    from lxml import html

    html_raw = requests.get("https://" + region + ".newonnetflix.info/").content
    html_tree = html.fromstring(html_raw)

    removed_content = map(str.strip, html_tree.xpath("/html/body/div[1]/section/a/span/text()"))
    added_content = map(str.strip, html_tree.xpath("/html/body/div[1]/article/header/h1/a/text()"))

    return {
            "removed":list(removed_content),
            "added":list(added_content)
    }


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


def speech_list_builder(movies):
    speech = ""
    for movie in movies[:-1]:
        speech += movie + ", "
    speech += "and " + movies[-1] + "."
    return speech


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
