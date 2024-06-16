from fastapi import FastAPI, Request, HTTPException
import requests

app = FastAPI()

GITHUB_TOKEN = "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"  # Replace with your GitHub personal access token
OWNER = "khabdrick"  # Replace with your GitHub username
REPO = "rollback-heroku"  # Replace with your GitHub repository
EVENT_TYPE = "rollback"
HEROKU_API_KEY = "0fe7b1ec-11df-4ebd-aa9f-c178062f0947"  # Replace with your Heroku API key
HEROKU_APP_NAME = "rollback-heroku"  # Replace with your Heroku app name

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print(data)

    try:
        # Example logic to parse and verify the alert data
        alert_name = data.get('alert_name')
        alert_severity = data.get('severity')
        error_rate = data.get('error_rate')

        # Example condition: Trigger rollback if the error rate exceeds 5% and severity is critical
        if alert_name == "High Error Rate" and alert_severity == "critical" and error_rate > 5:
            # Fetch the list of Heroku releases
            releases_response = requests.get(
                f"https://api.heroku.com/apps/{HEROKU_APP_NAME}/releases",
                headers={
                    "Authorization": f"Bearer {HEROKU_API_KEY}",
                    "Accept": "application/vnd.heroku+json; version=3"
                }
            )
            
            if releases_response.status_code != 200:
                raise HTTPException(status_code=releases_response.status_code, detail="Failed to fetch Heroku releases")
            
            releases = releases_response.json()
            if len(releases) < 2:
                raise HTTPException(status_code=400, detail="Not enough releases to perform rollback")
            
            # Determine the version before the current version
            previous_release = releases[-2]['version']
            
            # Trigger GitHub Action for rollback
            response = requests.post(
                f"https://api.github.com/repos/{OWNER}/{REPO}/dispatches",
                headers={
                    "Authorization": f"Bearer {GITHUB_TOKEN}",
                    "Accept": "application/vnd.github.v3+json",
                },
                json={
                    "event_type": EVENT_TYPE,
                    "client_payload": {"release": f"v{previous_release}"},
                },
            )
            
            if response.status_code == 204:
                return {"status": "success", "message": "Rollback triggered successfully"}
            else:
                return {"status": "error", "message": response.json()}
        else:
            return {"status": "ignored", "message": "Alert conditions not met for rollback"}
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing expected field: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
