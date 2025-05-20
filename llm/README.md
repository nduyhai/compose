# PoC using local AI create docs


## Install llama2

```bash
curl http://localhost:11434/api/pull -d '{"name": "llama2"}'
```

## Clone repos

```bash
mkdir -p repos
git clone https://github.com/nduyhai/passforge repos/passforge

```


## Create docs 
```bash
pip install -r requirements.txt
python generate_docs.py

```