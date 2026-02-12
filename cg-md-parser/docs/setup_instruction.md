Ollama Setup Guide (Windows)

install, run, and use **Ollama** locally, and connect it with your Python script.


## 📦 0. Install Python Dependencies

Run this command in the project folder:

```bash
pip install -r requirements.txt
```

---


## ✅ 1. Download & Install Ollama

1. Go to: https://ollama.com
2. Click **Download for Windows**
3. Install it like a normal app (Next → Next → Finish)
4. **Restart your PC** (recommended)

---

## ▶️ 2. Start Ollama Server

Open **Command Prompt** or **PowerShell** and run:

```bash
ollama serve
```

You should see something like:

```text
Listening on 127.0.0.1:11434
```

## 🧠 Download a Model

Open **another** Command Prompt window and run:

```bash
ollama pull qwen2.5:3b
```

## 💬 Test Ollama in Terminal

Run:

```bash
ollama run qwen2.5:3b
```

Type:

```text
Hello, how are you?
```

You should see the model's response. ollama is working.

Exit with:

```bash
/bye
```

## 🌐 Test the Ollama API (Important)

Check if Ollama API is running:

```bash
curl http://localhost:11434/api/tags
```

You should see something like:

```json
{
  "models": [
    {
      "name": "qwen2.5:3b"
    }
  ]
}
```

## Use Ollama in Python


In your Python script:

```python
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"
```


Make sure Ollama is running:

```bash
ollama serve
```
