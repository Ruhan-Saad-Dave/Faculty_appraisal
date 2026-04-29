# How to setup 

1. Download uv package manager
```bash
pip install uv
uv sync
```
2. To add dependencies
```bash
uv add <dependency>
```
3. To run code
```bash
uvicorn main:app --reload
```
4. Go to (http://localhost:8000/docs)[http://localhost:8000/docs] to view and test the documentation