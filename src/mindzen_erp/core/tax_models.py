"""
Generic Tax Engine Models
"""
from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from mindzen_erp.core.orm import BaseModel

class TaxRegime(BaseModel):
    """Tax Regime (e.g. Saudi Zakat & Tax)"""
    __tablename__ = 'tax_regimes'
    
    name = Column(String(200), nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'))
    is_active = Column(Boolean, default=True)
    
    country = relationship("Country")

class TaxType(BaseModel):
    """Tax Type (e.g. VAT, Zakat, Excise)"""
    __tablename__ = 'tax_types'
    
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True)
    is_active = Column(Boolean, default=True)

class TaxRate(BaseModel):
    """Tax Rate Mapping"""
    __tablename__ = 'tax_rates'
    
    regime_id = Column(Integer, ForeignKey('tax_regimes.id'))
    type_id = Column(Integer, ForeignKey('tax_types.id'))
    rate_percent = Column(Numeric(5, 2), nullable=False)
    is_active = Column(Boolean, default=True)
    
    regime = relationship("TaxRegime")
    tax_type = relationship("TaxType")
