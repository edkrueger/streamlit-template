# streamlit-template

## Python Dev Tools Setup
Change into `backend` directory.  
Run `pipenv install --dev` to install the env.  
Run `pipenv shell`.  
Run `pre-commit install` to initialize the git hooks.  
Run `pre-commit run --all-files` if there are file that were committed before adding the git hooks. 
Run `pytest --cov-config=.coveragerc --cov=app/package` to run tests.  
Note: Currently, `pipenv_to_requirements` must be run manually to sync `requirements.txt` and `requirements-dev.txt`.  

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