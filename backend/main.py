from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import patients, doctors, cases, vitals, labs, catalog

def create_app():
    app = FastAPI(title="ClinicMS API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(patients.router, prefix="/patients", tags=["patients"])
    app.include_router(doctors.router,  prefix="/doctors",  tags=["doctors"])
    app.include_router(cases.router,    prefix="/cases",    tags=["cases"])
    app.include_router(vitals.router,   prefix="/vitals",   tags=["vitals"])
    app.include_router(labs.router,     prefix="/labs",     tags=["labs"])
    app.include_router(catalog.router,  prefix="/catalog",  tags=["catalog"])

    return app

app = create_app()