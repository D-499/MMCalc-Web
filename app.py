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
from models import db, SavedCompound
db.init_app(app)

# Initialize calculator
calculator = MolarMassCalculator()

# Import compound library after app setup
from compound_library import CompoundLibrary
compound_library = CompoundLibrary()

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """Main page showing calculation options"""
    return render_template('index.html')

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    """Handle all calculation modes"""
    if request.method == 'GET':
        mode = request.args.get('mode', '1')
        return render_template('calculate.html', mode=mode)
    
    mode = request.form.get('mode', '1')
    compound = request.form.get('compound', '').strip()
    verbose = request.form.get('verbose') == 'on'
    
    if not compound:
        flash('Please enter a chemical formula.', 'error')
        return render_template('calculate.html', mode=mode)
    
    try:
        results = {}
        
        # Parse and validate formula
        element_counts = calculator.parse_formula(compound)
        if not element_counts:
            flash('Invalid chemical formula. Please check your input.', 'error')
            return render_template('calculate.html', mode=mode, compound=compound)
        
        if not calculator.validate_elements(element_counts):
            flash('Invalid element detected in formula. Please use valid element symbols.', 'error')
            return render_template('calculate.html', mode=mode, compound=compound)
        
        # Calculate molar mass
        molar_mass = calculator.calculate_molar_mass(compound)
        results['compound'] = compound
        results['molar_mass'] = molar_mass
        results['element_counts'] = element_counts
        
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
            pass
            
        elif mode == '2':
            # Molar mass and reagent mass
            moles_str = request.form.get('moles', '').strip()
            if not moles_str:
                flash('Please enter the number of moles.', 'error')
                return render_template('calculate.html', mode=mode, compound=compound)
            
            try:
                moles = float(moles_str)
                reagent_mass = calculator.calculate_reagent_mass(moles, compound)
                results['moles'] = moles
                results['reagent_mass'] = reagent_mass
            except ValueError:
                flash('Please enter a valid number for moles.', 'error')
                return render_template('calculate.html', mode=mode, compound=compound)
                
        elif mode == '3':
            # Calculate moles from reagent mass
            mass_str = request.form.get('mass', '').strip()
            if not mass_str:
                flash('Please enter the mass.', 'error')
                return render_template('calculate.html', mode=mode, compound=compound)
            
            try:
                mass = float(mass_str)
                moles = calculator.calculate_moles(mass, compound)
                results['mass'] = mass
                results['calculated_moles'] = moles
            except ValueError:
                flash('Please enter a valid number for mass.', 'error')
                return render_template('calculate.html', mode=mode, compound=compound)
        
        return render_template('calculate.html', mode=mode, results=results, verbose=verbose)
        
    except Exception as e:
        flash(f'An error occurred during calculation: {str(e)}', 'error')
        return render_template('calculate.html', mode=mode, compound=compound)

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
        return render_template('calculate.html', mode=mode, compound=compound['formula'])
    else:
        flash('Compound not found.', 'error')
        return redirect(url_for('library'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
