from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes import patients, doctors, cases, vitals, labs, catalog, prescriptions, lab_tests


app = FastAPI(title="ClinicMS API")

import logging
logging.basicConfig(level=logging.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_cors_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

app.include_router(patients.router, prefix="/patients", tags=["patients"])
app.include_router(doctors.router, prefix="/doctors", tags=["doctors"])
app.include_router(cases.router, prefix="/cases", tags=["cases"])
app.include_router(vitals.router, prefix="/vitals", tags=["vitals"])
app.include_router(labs.router, prefix="/labs", tags=["labs"])
app.include_router(catalog.router, prefix="/catalog", tags=["catalog"])
app.include_router(prescriptions.router, prefix="/prescriptions", tags=["prescriptions"])
app.include_router(lab_tests.router, prefix="/lab-tests", tags=["Lab Tests"])