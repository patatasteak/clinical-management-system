
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from database import get_connection

router = APIRouter(tags=["Lab Tests"])

# Models
class LabTestCatalogCreate(BaseModel):
    test_name: str
    description: Optional[str] = None
    price: float

class LabTestCatalogUpdate(BaseModel):
    test_name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

class LabTestCatalog(BaseModel):
    catalog_id: str
    test_name: str
    description: Optional[str]
    price: float

# Helper: Generate next catalog ID
def generate_catalog_id() -> str:
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Get the highest catalog_id, strip 'LT' prefix and increment
        cur.execute("SELECT catalog_id FROM labtestcatalog ORDER BY catalog_id DESC LIMIT 1")
        last = cur.fetchone()
        if not last:
            return "LT0001"
        
        last_id = last[0]
        num = int(last_id[2:])
        return f"LT{num+1:04d}"
    finally:
        cur.close()
        conn.close()

@router.get("/catalog", response_model=List[LabTestCatalog])
def get_all_catalog():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT catalog_id, test_name, description, price FROM labtestcatalog ORDER BY catalog_id")
        rows = cur.fetchall()
        return [
            LabTestCatalog(
                catalog_id=row[0],
                test_name=row[1],
                description=row[2],
                price=row[3]
            )
            for row in rows
        ]
    finally:
        cur.close()
        conn.close()

@router.get("/catalog/{catalog_id}", response_model=LabTestCatalog)
def get_catalog_item(catalog_id: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT catalog_id, test_name, description, price FROM labtestcatalog WHERE catalog_id = %s", (catalog_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Lab test catalog item not found")
        return LabTestCatalog(
            catalog_id=row[0],
            test_name=row[1],
            description=row[2],
            price=row[3]
        )
    finally:
        cur.close()
        conn.close()

@router.post("/catalog", response_model=LabTestCatalog, status_code=201)
def create_catalog_item(item: LabTestCatalogCreate):
    conn = get_connection()
    cur = conn.cursor()
    try:
        catalog_id = generate_catalog_id()
        cur.execute(
            "INSERT INTO labtestcatalog (catalog_id, test_name, description, price) VALUES (%s, %s, %s, %s) RETURNING catalog_id, test_name, description, price",
            (catalog_id, item.test_name, item.description, item.price)
        )
        row = cur.fetchone()
        conn.commit()
        return LabTestCatalog(
            catalog_id=row[0],
            test_name=row[1],
            description=row[2],
            price=row[3]
        )
    finally:
        cur.close()
        conn.close()

@router.put("/catalog/{catalog_id}", response_model=LabTestCatalog)
def update_catalog_item(catalog_id: str, item: LabTestCatalogUpdate):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Get existing item
        cur.execute("SELECT catalog_id, test_name, description, price FROM labtestcatalog WHERE catalog_id = %s", (catalog_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Lab test catalog item not found")
        # Update
        new_test_name = item.test_name if item.test_name is not None else row[1]
        new_description = item.description if item.description is not None else row[2]
        new_price = item.price if item.price is not None else row[3]
        cur.execute(
            "UPDATE labtestcatalog SET test_name = %s, description = %s, price = %s WHERE catalog_id = %s RETURNING catalog_id, test_name, description, price",
            (new_test_name, new_description, new_price, catalog_id)
        )
        row = cur.fetchone()
        conn.commit()
        return LabTestCatalog(
            catalog_id=row[0],
            test_name=row[1],
            description=row[2],
            price=row[3]
        )
    finally:
        cur.close()
        conn.close()

@router.delete("/catalog/{catalog_id}", status_code=204)
def delete_catalog_item(catalog_id: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM labtestcatalog WHERE catalog_id = %s", (catalog_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Lab test catalog item not found")
        conn.commit()
    finally:
        cur.close()
        conn.close()

