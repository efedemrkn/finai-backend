from datetime import datetime
import calendar
import statistics
from typing import List
from . import models

SUBSCRIPTION_KEYWORDS = ["netflix", "spotify", "fatura", "internet", "elektrik", "su ", "doğalgaz", "kira", "turkcell", "vodafone", "telekom", "abonelik"]
NEEDS_CATEGORIES = {"Market", "Fatura", "Ulaşım", "Sağlık", "Eğitim"}
DAYS_TR = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

def generate_financial_analysis(expenses: List[models.Expense], monthly_budget: float):
    now = datetime.utcnow()
    current_year = now.year
    current_month = now.month
    days_in_month = calendar.monthrange(current_year, current_month)[1]
    current_day = max(now.day, 1)

    prev_month = 12 if current_month == 1 else current_month - 1
    prev_year = current_year - 1 if current_month == 1 else current_year

    this_month_expenses = [
        e for e in expenses
        if e.created_at.year == current_year and e.created_at.month == current_month
    ]
    prev_month_expenses = [
        e for e in expenses
        if e.created_at.year == prev_year and e.created_at.month == prev_month
    ]

    total_this_month = round(sum(e.amount for e in this_month_expenses), 2)
    total_prev_month = round(sum(e.amount for e in prev_month_expenses), 2)

    daily_average = round(total_this_month / current_day, 2)
    projected_end_of_month = round(daily_average * days_in_month, 2)

    if total_prev_month > 0:
        month_change_pct = round(((total_this_month - total_prev_month) / total_prev_month) * 100, 1)
    else:
        month_change_pct = 0.0

    # Kategori dağılımları
    category_totals = {}
    for e in this_month_expenses:
        category_totals[e.category] = round(category_totals.get(e.category, 0.0) + e.amount, 2)

    prev_category_totals = {}
    for e in prev_month_expenses:
        prev_category_totals[e.category] = round(prev_category_totals.get(e.category, 0.0) + e.amount, 2)

    top_category = max(category_totals.items(), key=lambda x: x[1])[0] if category_totals else "Veri Yok"

    remaining_budget = round(monthly_budget - total_this_month, 2)
    budget_usage_pct = round((total_this_month / monthly_budget) * 100, 1) if monthly_budget > 0 else 0.0

    # 1. Haftanın Günlerine Göre Harcama Davranışı
    weekday_totals = {day: 0.0 for day in DAYS_TR}
    for e in this_month_expenses:
        day_name = DAYS_TR[e.created_at.weekday()]
        weekday_totals[day_name] = round(weekday_totals[day_name] + e.amount, 2)
    peak_day = max(weekday_totals.items(), key=lambda x: x[1])[0] if total_this_month > 0 else "Veri Yok"

    # 2. 50/30/20 Kuralı (Zorunlu İhtiyaç vs. Kişisel İstek)
    needs_total = round(sum(e.amount for e in this_month_expenses if e.category in NEEDS_CATEGORIES), 2)
    wants_total = round(sum(e.amount for e in this_month_expenses if e.category not in NEEDS_CATEGORIES), 2)
    needs_pct = round((needs_total / total_this_month) * 100, 1) if total_this_month > 0 else 0.0
    wants_pct = round((wants_total / total_this_month) * 100, 1) if total_this_month > 0 else 0.0

    # 3. Sabit Gider & Abonelik Analizi
    recurring_items = []
    for e in this_month_expenses:
        desc_lower = e.description.lower()
        if e.category == "Fatura" or any(k in desc_lower for k in SUBSCRIPTION_KEYWORDS):
            recurring_items.append({
                "description": e.description,
                "category": e.category,
                "amount": e.amount
            })
    recurring_total = round(sum(x["amount"] for x in recurring_items), 2)

    # 4. Finansal Sağlık Skoru (0 - 100)
    score = 100
    if monthly_budget > 0:
        projected_ratio = projected_end_of_month / monthly_budget
        if projected_ratio > 1.0:
            score -= min(45, int((projected_ratio - 1.0) * 100))
        elif projected_ratio > 0.85:
            score -= 10
    if month_change_pct > 15:
        score -= min(20, int(month_change_pct - 15))
    if wants_pct > 45:
        score -= 10
    health_score = max(15, min(100, score))

    if health_score >= 80:
        health_label = "Mükemmel Disiplin"
    elif health_score >= 60:
        health_label = "Dengeli Seyir"
    else:
        health_label = "Yüksek Risk / Aşım"

    # 5. Anomali Tespiti
    anomalies = []
    if len(this_month_expenses) >= 4:
        amounts = [e.amount for e in this_month_expenses]
        mean_val = statistics.mean(amounts)
        stdev_val = statistics.stdev(amounts)
        threshold = mean_val + (1.5 * stdev_val)
        for e in this_month_expenses:
            if e.amount > threshold and e.amount > 500:
                anomalies.append({
                    "id": e.id,
                    "description": e.description,
                    "category": e.category,
                    "amount": e.amount,
                    "date": e.created_at.strftime("%d.%m.%Y"),
                    "ratio": round(e.amount / mean_val, 1)
                })

    # 6. AI Yönetici Özeti
    insights = []
    if projected_end_of_month > monthly_budget and monthly_budget > 0:
        over_amount = round(projected_end_of_month - monthly_budget, 2)
        insights.append(
            f"⚠️ Mevcut günlük ₺{daily_average:,.0f} harcama hızınızla ay sonunda bütçenizi ₺{over_amount:,.0f} aşma riskiniz bulunuyor."
        )
    else:
        insights.append(
            f"✅ Harcama disiplininiz dengeli. Ay sonunda tahmini ₺{projected_end_of_month:,.0f} ile bütçe sınırınız içinde kalıyorsunuz."
        )

    if total_this_month > 0:
        insights.append(
            f"⚖️ 50/30/20 Analizi: Harcamalarınızın %{needs_pct}'i zorunlu ihtiyaçlara (₺{needs_total:,.0f}), %{wants_pct}'i kişisel isteklere (₺{wants_total:,.0f}) gitti."
        )

    if peak_day != "Veri Yok":
        insights.append(
            f"📅 Davranışsal Analiz: Hafta içinde en yüksek harcama yoğunluğunuz '{peak_day}' günlerinde (₺{weekday_totals[peak_day]:,.0f}) gerçekleşiyor."
        )

    return {
        "total_this_month": total_this_month,
        "total_prev_month": total_prev_month,
        "month_change_pct": month_change_pct,
        "daily_average": daily_average,
        "projected_end_of_month": projected_end_of_month,
        "monthly_budget": monthly_budget,
        "remaining_budget": remaining_budget,
        "budget_usage_pct": budget_usage_pct,
        "top_category": top_category,
        "category_breakdown": category_totals,
        "prev_category_breakdown": prev_category_totals,
        "weekday_breakdown": weekday_totals,
        "peak_day": peak_day,
        "needs_total": needs_total,
        "wants_total": wants_total,
        "needs_pct": needs_pct,
        "wants_pct": wants_pct,
        "recurring_items": recurring_items,
        "recurring_total": recurring_total,
        "health_score": health_score,
        "health_label": health_label,
        "anomalies": anomalies,
        "insights": insights,
        "days_passed": current_day,
        "days_in_month": days_in_month
    }