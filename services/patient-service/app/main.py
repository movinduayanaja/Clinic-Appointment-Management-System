from fastapi import FastAPI

app = FastAPI(title="Patient Service")

@app.get("/health")
def health():
    return {"service": "patient-service", "status": "ok"}

@app.get("/patients")
def get_patients():
    return []