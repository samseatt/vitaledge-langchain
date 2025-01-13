
cd ~/project/vitaledge/vitaledge-langchain

# conda create -n vitaledge-langchain python=3.11 -y
conda activate vitaledge-langchain

# pip-compile requirements.in
pip install -r requirements.txt

uvicorn app.main:app --host 0.0.0.0 --port 8012 --reload

curl -X POST "http://127.0.0.1:8012/orchestrate/rag" \
     -H "Content-Type: application/json" \
     -d '{"query": "Given the genomic profile of this patient, what are the chances of this patient getting luminal B-like breast cancer?"}'

curl -X POST "http://127.0.0.1:8012/orchestrate/rag" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is rheumatoid arthritis?"}'


## Diagnosis
pipdeptree --reverse --packages langchain

