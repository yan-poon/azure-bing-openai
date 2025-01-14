import azure.functions as func
import logging
import json
import bingsearch
import openaicustom

app = func.FunctionApp(http_auth_level=func.AuthLevel.ADMIN)

@app.function_name(name="bing-news-search")
@app.route(route="bing-news-search", methods=[func.HttpMethod.GET])
def bing_search(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('bing-news-search HTTP trigger function processed a request.')
    q = req.params.get('q')
    mkt= req.params.get('mkt')
    count = req.params.get('count')
    offset = req.params.get('offset')
    if not q:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Please provide 'q'",
            status_code=400
        )
    
    news_feed = bingsearch.generate_news_feed(q, mkt,count, offset)
    response_body = {
        "count": len(news_feed),
        "news_feed": news_feed
    }
    return func.HttpResponse(
        body=json.dumps(response_body),
        status_code=200,
        headers={
            "Content-Type": "application/json"
        }
    )

@app.function_name(name="openai-tweet")
@app.route(route="openai-tweet", methods=[func.HttpMethod.POST])
def bing_search(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('openai-assist HTTP trigger function processed a request.')
    tweetLanguage = req.params.get('tweetLanguage',"english")
    req_body = req.get_json()
    if not req_body:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Please provide request body",
            status_code=400
        )
    try:
        dataObj = openaicustom.get_tweet_from_assistant(req_body,tweetLanguage)
        return func.HttpResponse(
            body=json.dumps(dataObj),
            status_code=200,
            headers={
                "Content-Type": "application/json"
            }
        )
    except Exception as e:
        logging.error(e)
        dataObj={
            'tweet': None,
            'url': req_body['url'],
            'name': req_body['name'],
            'description': req_body['description'],
            'error': e
        }
        return func.HttpResponse(
            body=json.dumps(dataObj),
            status_code=400,
            headers={
                "Content-Type": "application/json"
            }
        )

@app.function_name(name="openai-summary")
@app.route(route="openai-summary", methods=[func.HttpMethod.POST])
def bing_search(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('openai-summary HTTP trigger function processed a request.')
    summaryLanguage = req.params.get('summaryLanguage',"english")
    req_body = req.get_json()
    if not req_body:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Please provide request body",
            status_code=400
        )
    try:
        dataObj = openaicustom.get_summary_from_assistant(req_body,summaryLanguage)
        return func.HttpResponse(
            body=json.dumps(dataObj),
            status_code=200,
            headers={
                "Content-Type": "application/json"
            }
        )
    except Exception as e:
        logging.error(e)
        dataObj={
            'info': {
                'summary': None,
                'newInsight': None
            },
            'error': e
        }
        return func.HttpResponse(
            body=dataObj,
            status_code=400,
            headers={
                "Content-Type": "application/json"
            }
        )