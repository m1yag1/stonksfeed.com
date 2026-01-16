# Stonksfeed

I need to figure out how to make local development on stonksfeed easier. Since I'm now using DynamoDB the database is in AWS which makes it little more difficult to run locally. There is however a project I can use that allows me run a docker container. SAM App allows me to run the lambda functions which is nice however it comes with its own scaffolding that is difficult to run with Terraform. This has me asking ... Do I reallly need SAM App? Can I get away with simply using the Stonksfeed package, DynamoDB local, and pytest? The AWS Lambda functions should be primarily constructed with functions contained in stonksfeed that are covered by tests.

What is the most ideal way to architect lambda functions that pull together news from RSS feeds?

I had created the RSS feeders separately but maybe I should put those in a loop.

OK, So i can have a CloudWatch event trigger my AWS lambda function like a cronjob.

I also need to update my Lambda function to check for any new articles and only update those.

I need a way to label an article as new.

In the future, I'd also like to pin articles or to delete them but those can wait for now.



```

rss_feeds = [
    {""},
]

```


```



This seems like a workable solution. Where should I start?

There are a few problems I need to work through.

AWS Lambda / SAM App

DynamoDB

Stonksfeed Python Package

Terraform

S3
