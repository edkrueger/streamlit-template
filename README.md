# streamlit-template

## Python Dev Tools Setup
To install the env, run `pipenv install --dev`  
To initialize the git hooks, run `pipenv run pre-commit install`  
If there are file that were committed before adding the git hooks, run `pipenv run pre-commit run --all-files`  
To run tests, run `pipenv run pytest --cov-config=.coveragerc --cov=resc`  

## Run Streamlit for Development
To run the app, run `pipenv run streamlit run app/app.py`  
Alternatively, run `pipenv run start`  

## Build and Run with Docker
If you haven't run the hooks, before builtind, run `pipenv run pre-commit run --all-files`  
To build the container, run `docker build . -t streamlit-app`  
Run with `docker run -p 80:80 streamlit-app`  
Note: This will run the app on port 80 inside the container and port 80 outside of the container.  
_Ignore the urls and ports in the terminal -- those are the ones in the Docker network._  
To reference it outside of the container, the URL is `http://localhost/`  

## Deploy to GCP Compute Engine
### Build and Deploy to GCR
To select you account and project, run `gcloud init`  
Select a default compute region  
To get and save your project id, run `export PROJECT=$(gcloud config get-value project)`  
To get the GCR tag, run `export GCR_TAG=gcr.io/$PROJECT/my-app`  
To submit the build to GCP Cloud Build, run `gcloud builds submit --tag $GCR_TAG`  
To see the GCR tag, run `echo $GCR_TAG`  

### Manually Deploy to GCE and Start Container option 1)
Go to "Compute Engine" in the GCP UI and select "CREATE INSTANCE".  
In the options select the checkbox "Deploy a container image to this VM instance."  
Paste in the GCR tag in the "Container Image" field.  
Select "Allow HTTP traffic" for a public deployment.  
Click "Create".  

### Automatically Deploy to GCE and Start Container (option 2)

Run:
```
gcloud compute instances create-with-container streamlit \
  --machine-type e2-small \
  --container-image $GCR_TAG \
  --container-command "streamlit run app/app.py --server.port 80" \
  --tags streamlit
```

Run: 
```
gcloud compute firewall-rules create allow-http \
  --allow tcp:80 \
  --target-tags streamlit
``` 
## Deploy to Azure 
Set the following environmental variables:  

```
AZURE_GROUP=steamlit-template2
REGION=centralus
ACR_IMAGE_NAME=streamlit-template-app
ACR_NAME=streamlittemplateregistry2
ACI_NAME=streamlit-template-app
```

Run this following:

```
az group create --name $AZURE_GROUP --location $REGION
az acr create --name $ACR_NAME --resource-group $AZURE_GROUP --sku Basic --admin-enabled true
az acr build --registry $ACR_NAME --image=$ACR_IMAGE_NAME --file Dockerfile .

ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --resource-group $AZURE_GROUP --query "loginServer" --output tsv)
ACR_ADMIN_USERNAME=$(az acr credential show --name $ACR_NAME --query username --output tsv)                
ACR_ADMIN_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" --output tsv)

az container create \
    --resource-group $AZURE_GROUP \
    --name $ACI_NAME \
    --image $ACR_LOGIN_SERVER/$ACR_IMAGE_NAME\:latest \
    --registry-login-server $ACR_LOGIN_SERVER \
    --ip-address Public \
    --location $REGION \
    --registry-username $ACR_ADMIN_USERNAME \
    --registry-password $ACR_ADMIN_PASSWORD \
    --environment-variables PORT=80
```


## Integrating Pipenv with VSCode
Unfortunately by default, VSCode will not interpret the python code as using the virtual environment that was created in the [Dev Tool Setup section](##python-dev-tools-setup).

The easiest way to get VSCode and Pipenv to work together is by following the steps found in [this article](https://www.therightchoyce.com/2018/10/01/setting-up-visual-studio-code-with-pipenv-and-python3/).

The steps boil down to the following:
1. Add the [Python Extension Pack](https://marketplace.visualstudio.com/items?itemName=donjayamanne.python-extension-pack)
3. Open your VSCode settings
4. Go to Workspace settings
5. Add the following:
```json
{
  "python.venvPath": "/Users/me/.local/share/virtualenvs/",
  "python.pythonPath": "/Users/me/.local/share/virtualenvs/ENV-NAME/bin/python",
  "python.jediEnabled": true,
}
```
6. Restart VSCode
