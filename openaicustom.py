from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import logging
import json

key_vault_url = f"https://one-leiaws-kv.vault.azure.net"
secret_name = "AZURE-OPEN-AI-API-KEY"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=key_vault_url, credential=credential)
retrieved_secret = client.get_secret(secret_name)
api_key = retrieved_secret.value

client = AzureOpenAI(
  azure_endpoint = "https://one-leiaws-openai.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview", 
  api_key=api_key,
  api_version="2024-02-01"
)

def get_tweet_from_assistant(data,tweetLanguage):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI assistant that helps me to create post on Twitter. You should provide Tweet for me like a SEO expert."},
            {"role": "user", "content": messageToAssistantForTwitter(data,tweetLanguage)}]
        )
    logging.info(response)
    tweetJsonText=response.choices[0].message.content.replace("```json", "").replace("```", "").strip()
    dataObj={
        'tweet': json.loads(tweetJsonText),
        'url': data['url'],
        'name': data['name'],
        'description': data['description'],
        'error': None
    }
    return dataObj

def messageToAssistantForTwitter(data, tweetLanguage="English") :
    jsonRequirement='{"instrToImageAI": "str","tweet": "str", "suggestHashtag": ["str"]}'
    message= f"Suggest a Tweet for me as a SEO expert so the tweet should attract readers. Help me to prepare a twitter tweet with proper emoji which is in {tweetLanguage} and at least 200 but not more than 280 characters for sharing this url and no need to say 'Read more:'.'. Always include the url after hashtags and at the end of the Tweet. {data['url']} "
    message+="Please also provide the instruction for generating a good image for the tweet base on the content of page by Image Gen AI. " 
    message+="Answer in json object with following schema: "+jsonRequirement
    logging.info(message)
    return message

def get_summary_from_assistant(data,summaryLanguage):
    try:
        response = client.chat.completions.create(
            model="gpt-4o", # model = "deployment_name".
            messages=[
                {"role": "system", "content": "You are an AI assistant that helps me to research and then share to my peers. You should provide summary of webpage or news for me like a professional assistant."},
                {"role": "user", "content": messageToAssistantForSummary(data,summaryLanguage)}]
            )
        logging.info(response)
        infoJsonText=response.choices[0].message.content.replace("```json\\n", "").replace("\\n```", "").replace("```json", "").replace("```", "").strip()
        dataObj={
            'info':json.loads(infoJsonText)
        }
        return dataObj
    except Exception as e:
        logging.error(e)
        dataObj={
            'info':{
                'summary': ['Summary is not be available'],
                'newInsight': []
            }
        }
        return dataObj
    

def messageToAssistantForSummary(data, summaryLanguage="English") :
    jsonRequirement='{"summary": "[str]","newInsight": "[str]"}'
    message= f"You should provide a summary (with 4 paragarphs and around 150-300 words, put each paragraphs in the string array) and new insight (2 paragraphs and around 80 words, put each paragraphs in the string array) from the page. Write in {summaryLanguage} for sharing the URL. {data['url']} "
    message+="Answer in json object with following schema: "+jsonRequirement
    logging.info(message)
    return message