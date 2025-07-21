import requests

def get_latest_app_id_and_status(resourcemanager_url):
    try:
        url = f"{resourcemanager_url}/ws/v1/cluster/apps?states=RUNNING,ACCEPTED,FAILED,KILLED,FINISHED"
        response = requests.get(url)
        apps = response.json().get('apps', {}).get('app', [])
        if apps:
            latest_app = sorted(apps, key=lambda x: x['startedTime'], reverse=True)[0]
            return latest_app['id'], latest_app['finalStatus']
        return None, "UNKNOWN"
    except Exception as e:
        return None, f"ERROR: {e}"
