# AlexaNetflixFlashBriefing
An Amazon Alexa "flash briefing" skill that provides a summary of the content that was removed or added to Netflix that week.

This repository only contains source code for the AWS Lambda function needed to retrieve the relavant information and upload it to AWS S3 for hosting the JSON feed that the Alexa Voice Service will use.

## Data source for the script
All data for this skill comes from https://newonnetflix.com. I do not own this site but it's owner has graciously let me utilize the data from there.

## Needed libraries for running locally
The requests, lxml, and boto3 libraries are needed for setting up a local virtualenv to test the code in.
Run: `pip install -r local-requirements.txt`

## Building for AWS Lambda
An AWS Lambda deployment package can be generated by running:
`bash zip-for-lambda.sh`
