# This is the code for the IBM Cloud Function "post_review". 
# The function is part of a cloud-hosted API, so this code is not really part of
# the codebase for the Django website. I am mainly leaving it here for my own reference 
# and documentation's sake, as well as for any fellow learners who are curious about the 
# API and IBM Cloud Functions. 


# IBM Cloud-specific imports
from cloudant.client import Cloudant
from cloudant.error import CloudantException


# main() will be run automatically when this action is invoked in IBM Cloud
def main(dict):
    """
    Posts a review to the external Cloudant database
    """
    
    secret = {
        "URL": "https://ccc91333-2f9a-4d99-8cda-196eed3e9b7d-bluemix.cloudantnosqldb.appdomain.cloud",
        "IAM_API_KEY": "SJjRe-KM3VYSZ7HN9Ed1oZqozdRpcysb0C_6ZtOriBC0",
        "USER_NAME": "ccc91333-2f9a-4d99-8cda-196eed3e9b7d-bluemix",
    }

    client = Cloudant.iam(
        account_name=secret["USER_NAME"], 
        api_key=secret["IAM_API_KEY"],
        url=secret["URL"],
        connect=True, 
    )
    
    db = client["reviews"]
    new_review = db.create_document(dict["review"])   
    
    if new_review.exists():
        result = {
            "headers": {"Content-Type": "application/json"},
            "body": {"message": "Review published successfully."}
        }
    
        print(new_review)
        return result
        
    else: 
        error_json = {
            "statusCode": 500,
            "message": "Could not publish review due to internal server error."
        }
        return error_json