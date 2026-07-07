# Smart Document Q&A

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Install Ollama

Download from:
https://ollama.com

Pull the model:

```bash
ollama pull llama3.2
```

## Run Backend

```bash
uvicorn api:app --reload
```

## Run Frontend

Open another terminal:

```bash
streamlit run app.py
```
