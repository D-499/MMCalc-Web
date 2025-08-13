from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class SavedCompound(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    formula = db.Column(db.String(200), nullable=False)
    molar_mass = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def __repr__(self):
        return f'<SavedCompound {self.name}: {self.formula}>'

class CalculationHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    formula = db.Column(db.String(200), nullable=False)
    mode = db.Column(db.String(10), nullable=False)  # '1', '2', '3'
    molar_mass = db.Column(db.Float, nullable=False)
    input_value = db.Column(db.Float, nullable=True)  # moles or mass input
    result_value = db.Column(db.Float, nullable=True)  # reagent mass or calculated moles
    unit = db.Column(db.String(10), default='mol')  # 'mol' or 'mmol'
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def __repr__(self):
        return f'<CalculationHistory {self.formula} mode {self.mode}>'

class UserSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    setting_key = db.Column(db.String(50), unique=True, nullable=False)
    setting_value = db.Column(db.String(200), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    def __repr__(self):
        return f'<UserSettings {self.setting_key}: {self.setting_value}>'
