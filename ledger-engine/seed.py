import uuid
import random
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Merchant, InventoryItem, Transaction, TransactionType, EvidenceSnapshot, Base

def seed_db():
    print("Starting Demo Seed Script...")
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        merchant_id = "+27821234567"
        existing = db.query(Merchant).filter(Merchant.merchant_id == merchant_id).first()
        if existing:
            print("Merchant already exists. Clearing old data for clean seed...")
            db.query(EvidenceSnapshot).filter(EvidenceSnapshot.merchant_id == merchant_id).delete()
            db.query(Transaction).filter(Transaction.merchant_id == merchant_id).delete()
            db.query(InventoryItem).filter(InventoryItem.merchant_id == merchant_id).delete()
            db.delete(existing)
            db.commit()
            
        print(f"Populating realistic example merchant: {merchant_id}")
        
        # 14 months history -> ~420 days ago
        created_at = datetime.now(timezone.utc) - timedelta(days=420)
        
        merchant = Merchant(
            merchant_id=merchant_id,
            whatsapp_number="+27821234567",
            business_name="Sipho's Spaza",
            pin_hash="1234",
            created_at=created_at
        )
        db.add(merchant)
        
        item = InventoryItem(
            item_id=str(uuid.uuid4()),
            merchant_id=merchant_id,
            name="General Stock",
            quantity_on_hand=500,
            unit_price=155.0
        )
        db.add(item)
        db.commit()
        
        # Generate 2481 transactions
        print("Generating 2,481 transactions...")
        transactions = []
        cumulative_revenue = 0.0
        
        # Target: 384,200 total revenue -> average ~155 per tx
        types = [
            (TransactionType.MANUAL_CASH_SALE, 0.2),
            (TransactionType.CUSTOMER_RECEIPT, 0.6),
            (TransactionType.QR_DIGITAL_PAYMENT, 0.85)
        ]
        
        for i in range(2481):
            tx_type, weight = random.choice(types)
            amount = round(random.uniform(50.0, 300.0), 2)
            
            # To strictly hit exactly 384200.0, we will adjust the last few transactions
            if i == 2480:
                amount = round(384200.0 - cumulative_revenue, 2)
                
            cumulative_revenue += amount
            
            # Random date within the 14 months
            tx_date = created_at + timedelta(days=random.randint(0, 420), minutes=random.randint(0, 1440))
            
            transactions.append(Transaction(
                transaction_id=str(uuid.uuid4()),
                merchant_id=merchant_id,
                item_id=item.item_id,
                transaction_type=tx_type,
                amount=amount,
                evidence_weight=weight,
                source_channel="voice" if random.random() > 0.5 else "button",
                created_at=tx_date
            ))
            
        db.bulk_save_objects(transactions)
        
        # Snapshot matching the exact requirements
        snapshot = EvidenceSnapshot(
            snapshot_id=str(uuid.uuid4()),
            merchant_id=merchant_id,
            week_ending=datetime.now(timezone.utc),
            transaction_volume=2481,
            revenue_total=384200.0,
            health_score=81.0,
            evidence_confidence_pct=78.5,
            state_hash="0xmockhash1234567890abcdef",
            onchain_tx_hash="0xtxhash1234567890abcdef"
        )
        db.add(snapshot)
        
        db.commit()
        
        print("Seed complete. Dashboard is ready for live demo!")
        print(f"History: 14 months")
        print(f"Total Transactions: 2,481")
        print(f"Cumulative Revenue: R 384,200.00")
        print(f"Revenue Consistency: 87%")
        print(f"Health Score: 81/100")
        print(f"Evidence Confidence Level: 78.5%")

    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
