import boto3


def delete_article(dynamodb_client, table_name, item):
    resp = dynamodb_client.delete_item(
        TableName=table_name,
        Key={
            "headline": item["headline"],
            "pubdate": item["pubdate"]
        }
    )
    if resp["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise Exception(f"Error deleting item from {table_name}: {resp}")
    return resp


def insert_article(dynamodb_client, table_name, item):
    resp = dynamodb_client.put_item(
        TableName=table_name,
        Item=item)
    if resp["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise Exception(f"Error inserting item into {table_name}: {resp}")
    return resp


def get_articles(dynamodb_client, table_name):
    resp = dynamodb_client.scan(TableName=table_name)
    if resp["ResponseMetadata"]["HTTPStatusCode"] != 200:
        Exception(f"Error getting items from {table_name}: {resp}")
    return resp


def test_insert_get_and_delete_dynamodb():
    dynamodb = boto3.client('dynamodb', endpoint_url='http://localhost:8000')

    table = "stonk_articles_prod_table"

    article_item = {
            "headline": {"S": "headline"},
            "pubdate": {"N": "12345"},
            "feed_title": {"S": "feed_title"},
            "link": {"S": "link"},
            "source_type": {"S": "source_type"},
            "author": {"S": "author"},
            "publisher": {"S": "publisher"}
            }

    insert_article(dynamodb, table, article_item)

    articles = get_articles(dynamodb, table)
    assert articles["Count"] > 0

    for item in articles["Items"]:
        if item["headline"]["S"] == "headline":
            assert item["pubdate"]["N"] == "12345"

    for item in articles["Items"]:
        delete_article(dynamodb, table, item)

    articles = get_articles(dynamodb, table)
    assert articles["Count"] == 0
