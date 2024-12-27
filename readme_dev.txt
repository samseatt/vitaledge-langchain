
cd ~/project/vitaledge/vitaledge-langchain

# conda create -n vitaledge-langchain python=3.11 -y
conda activate vitaledge-langchain

# pip-compile requirements.in
pip install -r requirements.txt

uvicorn app.main:app --host 0.0.0.0 --port 80012 --reload

curl -X POST "http://127.0.0.1:8012/orchestrate/rag" \
     -H "Content-Type: application/json" \
     -d '{"query": "What are the symptoms of diabetes?"}'


