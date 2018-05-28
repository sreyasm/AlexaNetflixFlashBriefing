def lambda_handler(event, context):
    usa_dict = get_content_for_region("usa")
    uk_dict = get_content_for_region("uk")
    print(usa_dict)
    print(uk_dict)


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


def generate_json_from_dict(source_dict):
    pass


def save_to_s3(region, json_data):
    pass
