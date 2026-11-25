import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

TRAIN_DATA = [
    ("Migros market alışverişi", "Market"),
    ("Bim ekmek süt yumurta", "Market"),
    ("A101 haftalık mutfak", "Market"),
    ("Şok market atıştırmalık", "Market"),
    ("CarrefourSA gıda temizlik", "Market"),
    ("Manav meyve sebze", "Market"),
    ("Kasap et tavuk", "Market"),
    ("Fırın ekmek poğaça", "Market"),
    ("Starbucks kahve latte", "Yeme-İçme"),
    ("Kahve Dünyası filtre kahve", "Yeme-İçme"),
    ("Domino's pizza sipariş", "Yeme-İçme"),
    ("Yemeksepeti tavuk döner", "Yeme-İçme"),
    ("Komagene çiğ köfte dürüm", "Yeme-İçme"),
    ("Restoran akşam yemeği", "Yeme-İçme"),
    ("Kafe çay tost", "Yeme-İçme"),
    ("Burger King menü", "Yeme-İçme"),
    ("Shell benzin yakıt", "Ulaşım"),
    ("Opet motorin akaryakıt", "Ulaşım"),
    ("Otobüs kart dolumu ulaşım", "Ulaşım"),
    ("Uber taksi ücreti", "Ulaşım"),
    ("THY uçak bileti", "Ulaşım"),
    ("Şehirlerarası otobüs bileti", "Ulaşım"),
    ("Otopark ücreti", "Ulaşım"),
    ("Elektrik faturası ödeme", "Fatura"),
    ("Su faturası", "Fatura"),
    ("Doğalgaz faturası", "Fatura"),
    ("Türk Telekom fiber internet", "Fatura"),
    ("Turkcell telefon faturası", "Fatura"),
    ("Vodafone hat ödemesi", "Fatura"),
    ("Kira ödemesi", "Fatura"),
    ("Netflix aylık abonelik", "Eğlence"),
    ("Spotify müzik üyelik", "Eğlence"),
    ("Sinema bileti patlamış mısır", "Eğlence"),
    ("Steam oyun satın alma", "Eğlence"),
    ("Halı saha maç ücreti", "Eğlence"),
    ("Konser tiyatro bileti", "Eğlence"),
    ("Zara kazak pantolon", "Giyim"),
    ("LC Waikiki tişört", "Giyim"),
    ("Nike spor ayakkabı", "Giyim"),
    ("Berber saç tıraşı", "Giyim"),
    ("Gratis parfüm bakım kremi", "Giyim"),
    ("Eczane ilaç vitamin", "Sağlık"),
    ("Hastane muayene", "Sağlık"),
    ("Kırtasiye defter fotokopi", "Eğitim"),
    ("Udemy online kurs kitap", "Eğitim"),
]

class SmartExpenseEngine:
    def __init__(self):
        self.model = make_pipeline(TfidfVectorizer(), MultinomialNB())
        self._train()

    def _train(self):
        texts = [item[0] for item in TRAIN_DATA]
        labels = [item[1] for item in TRAIN_DATA]
        self.model.fit(texts, labels)

    def predict_with_confidence(self, description: str):
        cleaned_text = re.sub(r'\d+([.,]\d+)?', '', description).strip()
        if not cleaned_text:
            return "Diğer", 50.0
        probs = self.model.predict_proba([cleaned_text])[0]
        max_idx = probs.argmax()
        category = self.model.classes_[max_idx]
        confidence = round(float(probs[max_idx]) * 100, 1)
        return category, confidence

    def predict_category(self, description: str) -> str:
        category, _ = self.predict_with_confidence(description)
        return category

    def parse_raw_text(self, raw_text: str):
        numbers = re.findall(r'\d+(?:[.,]\d+)?', raw_text)
        if not numbers:
            raise ValueError(f"'{raw_text}' içinde geçerli tutar bulunamadı.")
        
        amount = float(numbers[-1].replace(',', '.'))
        desc = re.sub(r'\d+(?:[.,]\d+)?', '', raw_text)
        desc = re.sub(r'\b(tl|TL|lira|₺)\b', '', desc).strip()
        if not desc:
            desc = "Genel Harcama"
            
        category, confidence = self.predict_with_confidence(desc)
        return desc, amount, category, confidence

engine = SmartExpenseEngine()