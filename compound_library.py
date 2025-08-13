"""
Compound Library - Handle saving and retrieving commonly used compounds
"""
import json
import os
from models import SavedCompound, db

class CompoundLibrary:
    def __init__(self):
        self.db = db

    def add_compound(self, name, formula, molar_mass):
        """Add a compound to the library"""
        try:
            # Check if compound with this name already exists
            existing = SavedCompound.query.filter_by(name=name).first()
            if existing:
                return False
            
            compound = SavedCompound(
                name=name,
                formula=formula,
                molar_mass=molar_mass
            )
            
            db.session.add(compound)
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Error adding compound: {e}")
            return False

    def delete_compound(self, compound_id):
        """Delete a compound from the library"""
        try:
            compound = SavedCompound.query.get(compound_id)
            if compound:
                db.session.delete(compound)
                db.session.commit()
                return True
            return False
            
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting compound: {e}")
            return False

    def get_compound(self, compound_id):
        """Get a specific compound by ID"""
        try:
            compound = SavedCompound.query.get(compound_id)
            if compound:
                return {
                    'id': compound.id,
                    'name': compound.name,
                    'formula': compound.formula,
                    'molar_mass': compound.molar_mass,
                    'created_at': compound.created_at
                }
            return None
            
        except Exception as e:
            print(f"Error getting compound: {e}")
            return None

    def get_all_compounds(self):
        """Get all compounds from the library"""
        try:
            compounds = SavedCompound.query.order_by(SavedCompound.name).all()
            return [{
                'id': compound.id,
                'name': compound.name,
                'formula': compound.formula,
                'molar_mass': compound.molar_mass,
                'created_at': compound.created_at
            } for compound in compounds]
            
        except Exception as e:
            print(f"Error getting compounds: {e}")
            return []

    def search_compounds(self, query):
        """Search compounds by name or formula"""
        try:
            compounds = SavedCompound.query.filter(
                db.or_(
                    SavedCompound.name.contains(query),
                    SavedCompound.formula.contains(query)
                )
            ).order_by(SavedCompound.name).all()
            
            return [{
                'id': compound.id,
                'name': compound.name,
                'formula': compound.formula,
                'molar_mass': compound.molar_mass,
                'created_at': compound.created_at
            } for compound in compounds]
            
        except Exception as e:
            print(f"Error searching compounds: {e}")
            return []
