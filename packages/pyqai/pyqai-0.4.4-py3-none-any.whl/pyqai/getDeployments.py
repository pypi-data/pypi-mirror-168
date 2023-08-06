import requests
import json
import yaml
import argparse
import os

# NOTE: returns a list of deployment names.
# TODO: consider sending back the entire yaml? Maybe someone wants that? No status update here.
# TODO: make this error handling not shit.
def getDeployments(model_name):
    try:
        homeDir = os.path.expanduser( '~' )
        f = open(f"{homeDir}/pyqai.config")
        configObj = json.load(f)
        api_token = configObj["api_token"]
        account_name = configObj["account_name"]
        account_id = configObj["account_id"]
    except Exception as e:
        print("ERROR. Unable to verify credentials; re-run pyqai-init to reset user credentials.")
        return 

    get_deployments_json = {"model_name":model_name,"account_id":account_id,"api_token":api_token,"account_name":account_name}
    get_deployments = requests.post('https://get-deployments-fgkue36c2q-uc.a.run.app', json = get_deployments_json, headers={'Authorization':api_token})

    try:
        get_deployments_response = json.loads(get_deployments.text)

        get_deployments_content = get_deployments_response["response"]

        return get_deployments_content
    except Exception as e:
        print(f"ERROR. Unable to get deployment names with exception: {e}")
        return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", help="The name of your deployed model", required=True)
    args = parser.parse_args()

    print(getDeployments(args.model_name))

    # python3 getDeployments.py --api_token d6d988ed-f2e5-4bfc-a813-c55f58c9b4e7 --account_name emilys-account --account_id 3 --model_name numbaguessa