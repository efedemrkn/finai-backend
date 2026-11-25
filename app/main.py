import re
from fastapi import FastAPI, Depends, HTTPException, status
from .analytics import generate_financial_analysis
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
import random

from . import models, schemas, database, auth
from .ml_model import engine as ml_engine

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="FinAI - Akıllı Kişisel Finans & Tahmin API",
    description="Makine Öğrenmesi Destekli Harcama Takip ve Analiz Sistemi",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Bu kullanıcı adı zaten alınmış")
    new_user = models.User(
        username=user.username,
        full_name=user.full_name,
        hashed_password=auth.get_password_hash(user.password)
    )
    db.add(new_user)
    db.commit()
    return {"message": "Hesap başarıyla oluşturuldu"}

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Kullanıcı adı veya şifre hatalı")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
def get_profile(current_user: models.User = Depends(auth.get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "monthly_budget": current_user.monthly_budget
    }

@app.put("/users/budget")
def update_budget(
    budget: schemas.BudgetUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    current_user.monthly_budget = budget.monthly_budget
    db.commit()
    return {"message": "Aylık bütçe hedefi güncellendi", "monthly_budget": current_user.monthly_budget}

@app.post("/expenses", response_model=schemas.ExpenseResponse)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    is_ai = False if expense.category else True
    assigned_category = expense.category if expense.category else ml_engine.predict_category(expense.description)
    
    new_expense = models.Expense(
        description=expense.description,
        amount=expense.amount,
        category=assigned_category,
        is_ai_categorized=is_ai,
        owner_id=current_user.id
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@app.post("/expenses/smart")
def create_smart_expense(
    payload: schemas.SmartExpenseCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    lines = [line.strip() for line in re.split(r'[,;\n]+', payload.raw_text) if line.strip()]
    if not lines:
        raise HTTPException(status_code=400, detail="Geçerli bir harcama metni giriniz.")

    created_items = []
    for line in lines:
        try:
            desc, amount, category, confidence = ml_engine.parse_raw_text(line)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        new_expense = models.Expense(
            description=desc,
            amount=amount,
            category=category,
            is_ai_categorized=True,
            owner_id=current_user.id
        )
        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)
        created_items.append({
            "id": new_expense.id,
            "description": new_expense.description,
            "amount": new_expense.amount,
            "category": new_expense.category,
            "confidence": confidence
        })

    return {"items": created_items, "count": len(created_items)}

@app.get("/expenses", response_model=List[schemas.ExpenseResponse])
def get_expenses(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return db.query(models.Expense).filter(models.Expense.owner_id == current_user.id).order_by(models.Expense.created_at.desc()).all()

@app.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id,
        models.Expense.owner_id == current_user.id
    ).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Harcama bulunamadı")
    db.delete(expense)
    db.commit()
    return {"message": "Harcama silindi"}

@app.post("/demo/seed")
def seed_demo_data(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    sample_items = [
        ("Migros Haftalık Alışveriş", 680.0), ("Starbucks Kahve", 145.0),
        ("Shell Akaryakıt", 950.0), ("Domino's Pizza", 340.0),
        ("Elektrik Faturası", 520.0), ("Türk Telekom İnternet", 390.0),
        ("Bim Mutfak Eksikleri", 290.0), ("Komagene Çiğ Köfte", 130.0),
        ("Otobüs Kart Dolumu", 200.0), ("Netflix Abonelik", 229.0),
        ("Zara Kazak", 1150.0), ("Eczane Vitamin", 310.0),
        ("Halı Saha Maç", 160.0), ("Kırtasiye Fotokopi", 95.0)
    ]
    now = datetime.utcnow()
    created_count = 0
    for i in range(45):
        desc, base_amt = random.choice(sample_items)
        amount = round(base_amt * random.uniform(0.85, 1.25), 2)
        days_ago = random.randint(0, 60)
        cat = ml_engine.predict_category(desc)
        exp = models.Expense(
            description=desc,
            amount=amount,
            category=cat,
            is_ai_categorized=True,
            created_at=now - timedelta(days=days_ago),
            owner_id=current_user.id
        )
        db.add(exp)
        created_count += 1
    db.commit()
    return {"message": f"{created_count} adet sunum verisi başarıyla oluşturuldu!"}

@app.get("/analytics/summary")
def get_analytics_summary(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    expenses = db.query(models.Expense).filter(models.Expense.owner_id == current_user.id).all()
    return generate_financial_analysis(expenses, current_user.monthly_budget)