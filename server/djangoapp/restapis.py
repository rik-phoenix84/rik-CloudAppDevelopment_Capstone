import requests
import json
import os
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

# Function for making HTTP GET requests
def get_request(url, api_key=False, **kwargs):
    print(f"GET from {url}")
    if api_key:
        # Basic authentication GET
        try:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        except:
            print("An error occurred while making GET request. ")
    else:
        # No authentication GET
        try:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
        except:
            print("An error occurred while making GET request. ")

    # Retrieving the response status code and content
    status_code = response.status_code
    print(f"With status {status_code}")
    json_data = json.loads(response.text)

    return json_data

# Gets all dealers from the Cloudant DB with the Cloud Function get-dealerships
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    print(json_result)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
            full_name=dealer_doc["full_name"], id=dealer_doc["id"], lat=dealer_doc["lat"],
            long=dealer_doc["long"], short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Function to make post requests
def post_request(url, json_payload, **kwargs):
    print(f"POST to {url}") 
    try:
        response = requests.post(url, params = kwargs, payload=json_payload)
    except:
        print("An error occurred with your POST request")
        
    status_code = response.status_code
    print(f"With status code {status_code}")

    return response

# Gets a single dealer from the Cloudant DB with the Cloud Function get-dealerships
# Requires the dealer_id parameter with only a single value
def get_dealer_by_id(url, dealer_id):
    # Call get_request with the dealer_id param
    json_result = get_request(url, dealerId=dealer_id)
    # Create a CarDealer object from response
    dealer = json_result
    dealer_details = dealer[0]
    dealer_obj = CarDealer(address=dealer_details["address"], city=dealer_details["city"], full_name=dealer_details["full_name"],
                           id=dealer_details["id"], lat=dealer_details["lat"], long=dealer_details["long"],
                           short_name=dealer_details["short_name"],
                           st=dealer_details["st"], zip=dealer_details["zip"])

    return dealer_obj

# Gets all dealer reviews for a specified dealer from the Cloudant DB
# Uses the Cloud Function get_reviews
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Perform a GET request with the specified dealer id
    json_result = get_request(url, dealerId=dealer_id)
    print("line 82", json_result)

    if json_result:
        # Get all review data from the response
        reviews = json_result
        # For every review in the response
        for review in reviews:
            # Create a DealerReview object from the data
            # These values must be present
            review_content = review["review"]
            id = review["_id"]
            name = review["name"]
            purchase = review["purchase"]
            dealership = review["dealership"]

            try:
                # These values may be missing
                car_make = review["car_make"]
                car_model = review["car_model"]
                car_year = review["car_year"]
                purchase_date = review["purchase_date"]

                # Creating a review object
                review_obj = DealerReview(dealership=dealership, id=id, name=name, 
                                          purchase=purchase, review=review_content, car_make=car_make, 
                                          car_model=car_model, car_year=car_year, purchase_date=purchase_date
                                          )

            except KeyError:
                print("Something is missing from this review. Using default values.")
                # Creating a review object with some default values
                review_obj = DealerReview(
                    dealership=dealership, id=id, name=name, purchase=purchase, review=review_content)

            # Analysing the sentiment of the review object's review text and saving it to the object attribute "sentiment"
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            print(f"sentiment: {review_obj.sentiment}")

            # Saving the review object to the list of results
            results.append(review_obj)

    return results


# Calls the Watson NLU API and analyses the sentiment of a review
def analyze_review_sentiments(review_text):
    # Watson NLU configuration
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/37913300-cd75-4515-9fba-6454c1654ffa"
    api_key = "x7EoJhfYq2uYc_hYUGI4we0H-uZmJzgTJXrpIGhPyrtd"
    
    version = '2021-08-01'
    authenticator = IAMAuthenticator(api_key)
    nlu = NaturalLanguageUnderstandingV1(
        version=version, authenticator=authenticator)
    nlu.set_service_url(url)

    # get sentiment of the review
    try:
        response = nlu.analyze(text=review_text, features=Features(
            sentiment=SentimentOptions())).get_result()
        print(json.dumps(response))
        # sentiment_score = str(response["sentiment"]["document"]["score"])
        sentiment_label = response["sentiment"]["document"]["label"]
    except:
        print("Review is too short for sentiment analysis. Assigning default sentiment value 'neutral' instead")
        sentiment_label = "neutral"

    # print(sentiment_score)
    print(sentiment_label)

    return sentiment_label