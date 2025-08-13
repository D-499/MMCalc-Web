import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from calculator import MolarMassCalculator

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "mmcalc-secret-key-2025")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///mmcalc.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Import models and initialize database
from models import db, SavedCompound, CalculationHistory, UserSettings
db.init_app(app)

# Initialize calculator
calculator = MolarMassCalculator()

# Import compound library after app setup
from compound_library import CompoundLibrary
compound_library = CompoundLibrary()

def get_setting(key, default):
    """Get a setting value from database"""
    setting = UserSettings.query.filter_by(setting_key=key).first()
    return setting.setting_value if setting else default

def set_setting(key, value):
    """Set a setting value in database"""
    setting = UserSettings.query.filter_by(setting_key=key).first()
    if setting:
        setting.setting_value = value
        setting.updated_at = db.func.current_timestamp()
    else:
        setting = UserSettings(setting_key=key, setting_value=value)
        db.session.add(setting)
    db.session.commit()

def save_calculation(formula, mode, molar_mass, input_value=None, result_value=None, unit='mol'):
    """Save calculation to history"""
    try:
        history = CalculationHistory(
            formula=formula,
            mode=mode,
            molar_mass=molar_mass,
            input_value=input_value,
            result_value=result_value,
            unit=unit
        )
        db.session.add(history)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error saving calculation history: {e}")

with app.app_context():
    db.create_all()
    # Set default settings if they don't exist
    if not UserSettings.query.filter_by(setting_key='default_unit').first():
        set_setting('default_unit', 'mmol')
    if not UserSettings.query.filter_by(setting_key='precision_molar_mass').first():
        set_setting('precision_molar_mass', '3')
    if not UserSettings.query.filter_by(setting_key='precision_reagent_mass').first():
        set_setting('precision_reagent_mass', '4')
    if not UserSettings.query.filter_by(setting_key='precision_moles').first():
        set_setting('precision_moles', '6')

@app.route('/')
def index():
    """Main page showing calculation options"""
    return render_template('index.html')

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    """Handle all calculation modes"""
    if request.method == 'GET':
        mode = request.args.get('mode', '1')
        library_compounds = compound_library.get_all_compounds()
        default_unit = get_setting('default_unit', 'mmol')
        return render_template('calculate.html', mode=mode, library_compounds=library_compounds, default_unit=default_unit)
    
    mode = request.form.get('mode', '1')
    compound = request.form.get('compound', '').strip()
    verbose = request.form.get('verbose') == 'on'
    unit = request.form.get('unit', get_setting('default_unit', 'mmol'))
    
    if not compound:
        flash('Please enter a chemical formula.', 'error')
        library_compounds = compound_library.get_all_compounds()
        return render_template('calculate.html', mode=mode, library_compounds=library_compounds, default_unit=unit)
    
    try:
        results = {}
        
        # Parse and validate formula
        element_counts = calculator.parse_formula(compound)
        if not element_counts:
            flash('Invalid chemical formula. Please check your input.', 'error')
            library_compounds = compound_library.get_all_compounds()
            return render_template('calculate.html', mode=mode, compound=compound, library_compounds=library_compounds, default_unit=unit)
        
        if not calculator.validate_elements(element_counts):
            flash('Invalid element detected in formula. Please use valid element symbols.', 'error')
            library_compounds = compound_library.get_all_compounds()
            return render_template('calculate.html', mode=mode, compound=compound, library_compounds=library_compounds, default_unit=unit)
        
        # Calculate molar mass
        molar_mass = calculator.calculate_molar_mass(compound)
        results['compound'] = compound
        results['molar_mass'] = molar_mass
        results['element_counts'] = element_counts
        results['unit'] = unit
        
        # Verbose mode calculations
        if verbose:
            verbose_calc = []
            for element, count in element_counts.items():
                mass = calculator.element_masses[element]
                total = mass * count
                verbose_calc.append({
                    'element': element,
                    'count': count,
                    'atomic_mass': mass,
                    'total_mass': total
                })
            results['verbose_calc'] = verbose_calc
        
        if mode == '1':
            # Molar mass only
            save_calculation(compound, mode, molar_mass, unit=unit)
            
        elif mode == '2':
            # Molar mass and reagent mass
            moles_str = request.form.get('moles', '').strip()
            if not moles_str:
                flash('Please enter the number of moles.', 'error')
                library_compounds = compound_library.get_all_compounds()
                return render_template('calculate.html', mode=mode, compound=compound, library_compounds=library_compounds, default_unit=unit)
            
            try:
                moles_input = float(moles_str)
                # Convert mmol to mol if needed
                moles_for_calc = moles_input / 1000 if unit == 'mmol' else moles_input
                reagent_mass = calculator.calculate_reagent_mass(moles_for_calc, compound)
                results['moles_input'] = moles_input
                results['reagent_mass'] = reagent_mass
                save_calculation(compound, mode, molar_mass, moles_input, reagent_mass, unit)
            except ValueError:
                flash('Please enter a valid number for moles.', 'error')
                library_compounds = compound_library.get_all_compounds()
                return render_template('calculate.html', mode=mode, compound=compound, library_compounds=library_compounds, default_unit=unit)
                
        elif mode == '3':
            # Calculate moles from reagent mass
            mass_str = request.form.get('mass', '').strip()
            if not mass_str:
                flash('Please enter the mass.', 'error')
                library_compounds = compound_library.get_all_compounds()
                return render_template('calculate.html', mode=mode, compound=compound, library_compounds=library_compounds, default_unit=unit)
            
            try:
                mass = float(mass_str)
                moles_calc = calculator.calculate_moles(mass, compound)
                # Convert mol to mmol if needed
                moles_display = moles_calc * 1000 if unit == 'mmol' else moles_calc
                results['mass'] = mass
                results['calculated_moles'] = moles_display
                save_calculation(compound, mode, molar_mass, mass, moles_display, unit)
            except ValueError:
                flash('Please enter a valid number for mass.', 'error')
                library_compounds = compound_library.get_all_compounds()
                return render_template('calculate.html', mode=mode, compound=compound, library_compounds=library_compounds, default_unit=unit)
        
        library_compounds = compound_library.get_all_compounds()
        return render_template('calculate.html', mode=mode, results=results, verbose=verbose, library_compounds=library_compounds, default_unit=unit)
        
    except Exception as e:
        flash(f'An error occurred during calculation: {str(e)}', 'error')
        library_compounds = compound_library.get_all_compounds()
        return render_template('calculate.html', mode=mode, compound=compound, library_compounds=library_compounds, default_unit=unit)

@app.route('/library')
def library():
    """Display compound library"""
    compounds = compound_library.get_all_compounds()
    return render_template('library.html', compounds=compounds)

@app.route('/library/add', methods=['POST'])
def add_compound():
    """Add compound to library"""
    name = request.form.get('name', '').strip()
    formula = request.form.get('formula', '').strip()
    
    if not name or not formula:
        flash('Please provide both name and formula.', 'error')
        return redirect(url_for('library'))
    
    # Validate formula
    element_counts = calculator.parse_formula(formula)
    if not element_counts or not calculator.validate_elements(element_counts):
        flash('Invalid chemical formula. Please check your input.', 'error')
        return redirect(url_for('library'))
    
    # Calculate molar mass
    molar_mass = calculator.calculate_molar_mass(formula)
    
    # Add to library
    success = compound_library.add_compound(name, formula, molar_mass)
    if success:
        flash(f'Added {name} ({formula}) to library.', 'success')
    else:
        flash('Compound with this name already exists.', 'error')
    
    return redirect(url_for('library'))

@app.route('/library/delete/<int:compound_id>')
def delete_compound(compound_id):
    """Delete compound from library"""
    success = compound_library.delete_compound(compound_id)
    if success:
        flash('Compound deleted successfully.', 'success')
    else:
        flash('Failed to delete compound.', 'error')
    
    return redirect(url_for('library'))

@app.route('/library/use/<int:compound_id>')
def use_compound(compound_id):
    """Use compound from library in calculation"""
    compound = compound_library.get_compound(compound_id)
    if compound:
        mode = request.args.get('mode', '1')
        library_compounds = compound_library.get_all_compounds()
        default_unit = get_setting('default_unit', 'mmol')
        return render_template('calculate.html', mode=mode, compound=compound['formula'], library_compounds=library_compounds, default_unit=default_unit)
    else:
        flash('Compound not found.', 'error')
        return redirect(url_for('library'))

@app.route('/add_to_library', methods=['POST'])
def add_to_library_from_result():
    """Add compound to library from calculation result"""
    name = request.form.get('name', '').strip()
    formula = request.form.get('formula', '').strip()
    molar_mass = float(request.form.get('molar_mass', 0))
    
    if not name or not formula:
        flash('Please provide both name and formula.', 'error')
        return redirect(request.referrer or url_for('index'))
    
    success = compound_library.add_compound(name, formula, molar_mass)
    if success:
        flash(f'Added {name} ({formula}) to library.', 'success')
    else:
        flash('Compound with this name already exists.', 'error')
    
    return redirect(request.referrer or url_for('index'))

@app.route('/history')
def history():
    """Display calculation history"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    history_query = CalculationHistory.query.order_by(CalculationHistory.created_at.desc())
    history_pagination = history_query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return render_template('history.html', 
                         history=history_pagination.items,
                         pagination=history_pagination)

@app.route('/history/clear')
def clear_history():
    """Clear all calculation history"""
    try:
        CalculationHistory.query.delete()
        db.session.commit()
        flash('History cleared successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to clear history.', 'error')
    
    return redirect(url_for('history'))

@app.route('/history/delete/<int:history_id>')
def delete_history_item(history_id):
    """Delete specific history item"""
    try:
        history_item = CalculationHistory.query.get(history_id)
        if history_item:
            db.session.delete(history_item)
            db.session.commit()
            flash('History item deleted.', 'success')
        else:
            flash('History item not found.', 'error')
    except Exception as e:
        db.session.rollback()
        flash('Failed to delete history item.', 'error')
    
    return redirect(url_for('history'))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """Settings page for user preferences"""
    if request.method == 'GET':
        current_settings = {
            'default_unit': get_setting('default_unit', 'mmol'),
            'precision_molar_mass': get_setting('precision_molar_mass', '3'),
            'precision_reagent_mass': get_setting('precision_reagent_mass', '4'),
            'precision_moles': get_setting('precision_moles', '6')
        }
        return render_template('settings.html', settings=current_settings)
    
    # Update settings
    try:
        set_setting('default_unit', request.form.get('default_unit', 'mmol'))
        set_setting('precision_molar_mass', request.form.get('precision_molar_mass', '3'))
        set_setting('precision_reagent_mass', request.form.get('precision_reagent_mass', '4'))
        set_setting('precision_moles', request.form.get('precision_moles', '6'))
        
        flash('Settings saved successfully.', 'success')
    except Exception as e:
        flash('Failed to save settings.', 'error')
    
    return redirect(url_for('settings'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
