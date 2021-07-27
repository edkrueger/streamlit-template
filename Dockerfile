FROM python:3.7-slim
COPY . ./
RUN pip install -r requirements.txt
CMD streamlit run app/app.py --server.port 80
