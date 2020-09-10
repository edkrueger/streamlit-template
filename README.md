# streamlit-template

## Python Dev Tools Setup
Change into `backend` directory.
Run `pipenv install --dev` to install the env.
Run `pipenv shell`.
Run `pre-commit install` to initialize the git hooks.
Run `pre-commit run --all-files` if there are file that were committed before adding the git hooks.
Run `pytest --cov-config=.coveragerc --cov=app/package` to run tests.
Note: Currently, `pipenv_to_requirements` must be run manually to sync `requirements.txt` and `requirements-dev.txt`.

## Run Streamlit for Development
Run `pipenv run start` or
Run `pipenv shell` then run `streamlit run app/app.py` or
Run `pipenv run streamlit run app/app.py`

## Build and Run with Docker
Change into `backend` directory.
Build with `docker build . -t streamlit-app`.
Run with `docker run -p 80:8080 -e PORT=8080 streamlit-app`.
Note: This will run the app on port 8080 inside the container and port 80 outside of the container.
To reference it outside of the container, the URL is `http://localhost/`

## Deploy to GCP Compute Engine
Change into `backend` directory.  
Run `gcloud init` to select you account and project.
Run `export PROJECT=$(gcloud config get-value project)` to get and save your project id.
Run `export GCR_TAG=gcr.io/$PROJECT/my-app` to get the GCR tag.
Run `gcloud builds submit --tag $GCR_TAG` to submit the build to GCP Cloud Build.
Run `echo $GCR_TAG` to see the GCR tag.
Go to "Compute Engine" in the GCP UI and select "CREATE INSTANCE".
In the options select the checkbox "Deploy a container image to this VM instance."
Paste in the GCR tag in the "Container Image" field.
Select "Allow HTTP traffic" for a public deployment.
Click "Create".
Click "SSH".
Run `export GCR_TAG=<GCR TAG>`.
Run `docker run -p 80:8080 -e PORT=8080 $GCR_TAG`.

## Deploy to Azure 
cd Change into `backend` directory.  
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
6. Change into `backend` and run `pipenv --py` in your terminal to find the actual path
7. Restart VSCode