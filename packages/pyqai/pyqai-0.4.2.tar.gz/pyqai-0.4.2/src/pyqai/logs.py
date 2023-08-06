import requests
import json
import argparse
import os

# NOTE: returns a list of pod names.
# TODO: write this into a file, instead of printing to terminal. which is what k8s does, but we want to be better.
# TODO: make this error handling not shit.
def get_pod_logs(model_name, pod_name):
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

    get_podLogs_json = {"model_name":model_name, "pod_name":pod_name,"account_id":account_id,"api_token":api_token,"account_name":account_name}

    try:
        get_pod_logs = requests.post('https://get-pod-logs-fgkue36c2q-uc.a.run.app', json = get_podLogs_json, headers={'Authorization':api_token})
        get_podslogs_response = json.loads(get_pod_logs.text)
        get_podslogs_content = get_podslogs_response["response"]

        get_podslogs_content = get_podslogs_response["response"]
        return get_podslogs_content
    except Exception as e:
        print(f"ERROR. Unable to get pod names with exception: {e}")
        return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", help="The name of your deployed model", required=True)
    parser.add_argument("--pod_name", help="The name of your pod", required=True)

    args = parser.parse_args()

    print(get_pod_logs(args.model_name, args.pod_name))