from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Enum, Boolean, Numeric
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class TransactionType(enum.Enum):
    MANUAL_CASH_SALE = "Manual cash sale"
    INVOICE_GENERATED = "Invoice generated"
    CUSTOMER_RECEIPT = "Customer receipt"
    REPEATED_PATTERN = "Repeated pattern"
    QR_DIGITAL_PAYMENT = "QR/digital payment"
    IDENTITY_INVOICE_ANCHOR = "Identity/invoice anchor"

class Merchant(Base):
    __tablename__ = 'merchants'
    merchant_id = Column(String, primary_key=True)
    whatsapp_number = Column(String, unique=True, nullable=False)
    business_name = Column(String, nullable=False)
    language_preference = Column(String, default="en")
    pin_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    inventory = relationship("InventoryItem", back_populates="merchant")
    transactions = relationship("Transaction", back_populates="merchant")
    snapshots = relationship("EvidenceSnapshot", back_populates="merchant")
    consents = relationship("Consent", back_populates="merchant")

class InventoryItem(Base):
    __tablename__ = 'inventory_items'
    item_id = Column(String, primary_key=True)
    merchant_id = Column(String, ForeignKey('merchants.merchant_id'), nullable=False)
    name = Column(String, nullable=False)
    quantity_on_hand = Column(Integer, default=0)
    unit_price = Column(Numeric(10, 2), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    merchant = relationship("Merchant", back_populates="inventory")

class Transaction(Base):
    __tablename__ = 'transactions'
    transaction_id = Column(String, primary_key=True)
    merchant_id = Column(String, ForeignKey('merchants.merchant_id'), nullable=False)
    item_id = Column(String, ForeignKey('inventory_items.item_id'), nullable=True)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    evidence_weight = Column(Float, nullable=False)
    source_channel = Column(String, nullable=False)
    idempotency_key = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    merchant = relationship("Merchant", back_populates="transactions")
    item = relationship("InventoryItem")

class EvidenceSnapshot(Base):
    __tablename__ = 'evidence_snapshots'
    snapshot_id = Column(String, primary_key=True)
    merchant_id = Column(String, ForeignKey('merchants.merchant_id'), nullable=False)
    week_ending = Column(DateTime(timezone=True), nullable=False)
    transaction_volume = Column(Integer, nullable=False)
    revenue_total = Column(Numeric(10, 2), nullable=False)
    health_score = Column(Float, nullable=False)
    evidence_confidence_pct = Column(Float, nullable=False)
    state_hash = Column(String, nullable=False)
    onchain_tx_hash = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    merchant = relationship("Merchant", back_populates="snapshots")

class Consent(Base):
    __tablename__ = 'consents'
    consent_id = Column(String, primary_key=True)
    merchant_id = Column(String, ForeignKey('merchants.merchant_id'), nullable=False)
    lender_id = Column(String, nullable=False)
    scope = Column(String, nullable=False)
    granted_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)

    merchant = relationship("Merchant", back_populates="consents")
