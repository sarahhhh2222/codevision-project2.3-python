import time
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

# =========================================================
# 📝 REQUIRED LIBRARIES :
#
# 1. playwright
# 2. sqlalchemy
#
# 💻 RUN THIS COMMAND TO INSTALL :
# pip install sqlalchemy playwright
# playwright install
# =========================================================

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from playwright.sync_api import sync_playwright

# ==========================================
# 1. TEAM & CONFIGURATION
# ==========================================
TEAM_MEMBERS = ["SHAMS BUKHARI", "JUWAN ALQARNI", "SARAH ALZUBAIRI", "Abdulilah Al Rifai", "Rahaf Ali"]
DATABASE_URL = "sqlite:///minihome_competitors.db"
Base = declarative_base()

MY_TARGET_PRICE = 90.0   
CHECK_INTERVAL = 10      

# ==========================================
# 2. DATABASE MODELS
# ==========================================
@dataclass
class ProductData:
    name: str
    price: float
    url: str

class CompetitorProduct(Base):
    _tablename_ = 'price_history'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    url = Column(String)
    check_date = Column(DateTime, default=datetime.now)

# ==========================================
# 3. SCRAPING LOGIC
# ==========================================
class MarketScraper(ABC):
    @abstractmethod
    def get_product_details(self, url: str) -> Optional[ProductData]:
        pass

class IkeaScraper(MarketScraper):
    def get_product_details(self, url: str) -> Optional[ProductData]:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                print(f"Checking URL...")
                page.goto(url, timeout=60000)
                
                try:
                    page.wait_for_selector(".pip-temp-price_integer, .pip-price_integer", timeout=10000)
                except:
                    pass 
                
                product_name = page.title() 
                
                price_element = page.locator(".pip-temp-price__integer").first
                if not price_element.is_visible():
                     price_element = page.locator(".pip-price__integer").first
                
                if not price_element.is_visible(): return None

                clean_price = re.sub(r'[^\d.]', '', price_element.inner_text())
                if not clean_price: return None

                return ProductData(name=product_name, price=float(clean_price), url=url)
            except Exception as e:
                print(f"Scraping Error: {e}")
                return None
            finally:
                browser.close()

# ==========================================
# 4. DATABASE OPERATIONS
# ==========================================
class DatabaseManager:
    def _init_(self, session):
        self.session = session

    def create_record(self, data: ProductData):
        new_record = CompetitorProduct(name=data.name, price=data.price, url=data.url)
        self.session.add(new_record)
        self.session.commit()
        print("💾 [CREATE] New price record saved to DB.")

    def get_last_record(self) -> Optional[CompetitorProduct]:
        return self.session.query(CompetitorProduct).order_by(CompetitorProduct.id.desc()).first()

    def update_timestamp(self, record_id):
        # Using session.get() to avoid LegacyAPIWarning
        record = self.session.get(CompetitorProduct, record_id)
        if record:
            record.check_date = datetime.now()
            self.session.commit()
            print("🔄 [UPDATE] Price unchanged. Updated timestamp only.")

    def clean_old_records(self):
        time_threshold = datetime.now() - timedelta(days=1)
        try:
            self.session.query(CompetitorProduct).filter(CompetitorProduct.check_date < time_threshold).delete()
            self.session.commit()
        except:
            pass

# ==========================================
# 5. MAIN APP CONTROLLER
# ==========================================
def main():
    print(f"\n💰 MINI HOME | COMPETITOR MONITORING SYSTEM")
    print(f"👥 Team: {', '.join(TEAM_MEMBERS)}")
    print("="*60)

    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    db = DatabaseManager(session)
    
    target_url = "https://www.ikea.com/kw/en/p/malm-bedroom-furniture-set-of-4-black-brown-s19483404//"
    scraper = IkeaScraper()

    try:
        while True:
            db.clean_old_records()

            print(f"\n🔎 Checking Market at {datetime.now().strftime('%H:%M:%S')}...")
            data = scraper.get_product_details(target_url)
            
            if data:
                print(f"✅ Found: {data.name}")
                print(f"💵 Price: {data.price} KD")
                
                if data.price < MY_TARGET_PRICE:
                    print(f"🚨 ALERT: Competitor price ({data.price}) is below target ({MY_TARGET_PRICE})!")
                else:
                    print(f"👍 Market Stable. Competitor is expensive.")

                last_rec = db.get_last_record()
                
                if last_rec and last_rec.price == data.price:
                    db.update_timestamp(last_rec.id)
                else:
                    db.create_record(data)

            else:
                print("⚠ Failed to retrieve data. Will retry...")

            print(f"💤 Waiting {CHECK_INTERVAL}s... (Press Ctrl+C to Stop)")
            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\n🛑 System stopped by user.")

if _name_ == "_main_":
    main()
