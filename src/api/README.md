## Running the API Server

```bash
python3 -m venv venv
source venv/bin/activate
```

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements/api.txt
```

```bash
export PYTHONPATH=$(pwd)/src
```

```bash
uvicorn api.main:app --reload
```