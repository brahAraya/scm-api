from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import Optional
from operator import itemgetter

app = FastAPI()

employees = []
companies = []


class Employee(BaseModel):
    id: Optional[str]
    rut: str
    name: str
    last_name: str
    company_id: str


class Company(BaseModel):
    id: Optional[str]
    name: str
    location: str


@app.get('/')
def root():
    return {
        "welcome-msg": "Employees and Companies API"
    }


@app.get('/employees')
def get_employees():
    return employees


@app.get('/companies')
def get_companies():
    return companies


@app.post('/employees')
def save_employee(employee: Employee):
    if len(employees) < 1:
        employee.id = "1"
    else:
        max_id = max(int(employee['id']) for employee in employees)
        new_id = str(max_id + 1)
        employee.id = new_id
        print(max_id + 1)

    employees.append(employee.dict())
    return employees[-1]


@app.post('/companies')
def save_company(company: Company):
    if len(companies) < 1:
        company.id = "1"
    else:
        max_id = max(int(company['id']) for company in companies)
        new_id = str(max_id + 1)
        company.id = new_id
        print(max_id + 1)
    companies.append(company.dict())
    return companies[-1]


@app.get('/employees/{employee_id}')
def get_employee(employee_id: str):
    for employee in employees:
        if employee["id"] == employee_id:
            return employee
    raise HTTPException(status_code=404, detail="Employee " +
                        employee_id + " not found")


@app.get('/companies/{company_id}')
def get_company(company_id: str):
    for company in companies:
        if company["id"] == company_id:
            return company
    raise HTTPException(status_code=404, detail="Company " +
                        company_id + " not found")


@app.delete('/employees/{employee_id}')
def delete_employee(employee_id: str):
    for i, employee in enumerate(employees):
        if employee["id"] == employee_id:
            employees.pop(i)
            return {"message": "Employee deleted"}
    raise HTTPException(status_code=404, detail="Employee " +
                        employee_id + " not found")


@app.delete('/companies/{company_id}')
def delete_company(company_id: str):
    for i, company in enumerate(companies):
        if company["id"] == company_id:
            companies.pop(i)
            return {"message": "company deleted"}
    raise HTTPException(status_code=404, detail="Company " +
                        company_id + " not found")


@app.put('/employees/{employee_id}')
def update_employee(employee_id: str, updated_employee: Employee):
    for i, employee in enumerate(employees):
        if employee["id"] == employee_id:
            employees[i]["rut"] = updated_employee.rut
            employees[i]["name"] = updated_employee.name
            employees[i]["last_name"] = updated_employee.last_name
            employees[i]["company_id"] = updated_employee.company_id
            return {"message": "Employee updated"}
    raise HTTPException(status_code=404, detail="Employee " +
                        employee_id + " not found")


@app.put('/companies/{company_id}')
def update_company(company_id: str, updated_company: Company):
    for i, company in enumerate(companies):
        if company["id"] == company_id:
            companies[i]["name"] = updated_company.name
            companies[i]["location"] = updated_company.location
            return {"message": "company updated"}
    raise HTTPException(status_code=404, detail="Company " +
                        company_id + " not found")
