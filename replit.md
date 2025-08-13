# MMCalc Web - Molar Mass Calculator

## Overview

MMCalc Web is a Flask-based web application that provides chemistry tools for calculating molar masses, reagent masses, and moles with precision formatting. The application is based on IUPAC 1995 Atomic Weights standards and offers multiple calculation modes along with a compound library for saving frequently used chemical formulas. Version 0.1.0 represents a complete web modernization of the original MMCalc Python CLI v0.6.2.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes (August 2025)

- Updated to semantic versioning v0.1.0 based on MMCalc Python CLI v0.6.2
- Replaced ASCII art logo with modern typography design using same color scheme
- Changed default units to mmol for modes 2 and 3 with toggle functionality  
- Added comprehensive settings menu for unit preferences and precision control
- Implemented calculation history with pagination and management features
- Added "Add to Library" functionality directly from calculation results
- Integrated "Import from Library" dropdown in calculation forms
- Enhanced user experience with unit switcher and interactive features
- Updated descriptions: main tagline simplified, added UPLB acknowledgment

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap-based responsive design
- **CSS Framework**: Bootstrap with dark theme and custom CSS for modern logo and chemical formula styling
- **JavaScript**: Enhanced vanilla JavaScript for form validation, unit switching, library import, and interactive features
- **UI Components**: Dark-themed interface with modern typography logo, responsive navigation, unit toggles, and calculation history

### Backend Architecture
- **Web Framework**: Flask with SQLAlchemy ORM for database operations
- **Application Structure**: Modular design separating concerns:
  - `app.py`: Main Flask application and routing
  - `calculator.py`: Core molar mass calculation logic with IUPAC atomic masses
  - `compound_library.py`: Database operations for saved compounds
  - `models.py`: SQLAlchemy data models
- **Calculation Engine**: Object-oriented calculator supporting complex chemical formulas with parentheses and nested structures
- **Session Management**: Flask sessions with configurable secret keys

### Data Storage Solutions
- **Primary Database**: SQLite by default with PostgreSQL support via environment configuration
- **ORM**: SQLAlchemy with DeclarativeBase for model definitions
- **Schema**: Three main models:
  - SavedCompound: Library storage with name, formula, molar mass, and timestamp
  - CalculationHistory: Complete calculation records with mode, inputs, results, and units
  - UserSettings: Configurable preferences for units and precision
- **Connection Pooling**: Configured with pool recycling and pre-ping for reliability

### User Experience Features
- **Unit Management**: Default mmol units with mol/mmol toggle for analytical chemistry workflows
- **Settings System**: Persistent user preferences for units and decimal precision
- **History Tracking**: Automatic saving and management of all calculations with pagination
- **Library Integration**: Direct import from compound library and add-to-library from results
- **Session Security**: Secret key-based session management for flash messages and user state

## External Dependencies

### Python Packages
- **Flask**: Web framework and routing
- **Flask-SQLAlchemy**: Database ORM integration
- **Werkzeug**: WSGI utilities and middleware

### Frontend Libraries
- **Bootstrap**: CSS framework via CDN (agent-dark-theme variant)
- **Font Awesome**: Icon library via CDN
- **Custom CSS**: Application-specific styling for chemical formulas and dark theme enhancements

### Database Support
- **SQLite**: Default embedded database
- **PostgreSQL**: Configurable via DATABASE_URL environment variable
- **Connection Features**: Pool recycling, pre-ping health checks

### Third-party Standards
- **IUPAC Atomic Weights**: Based on 1995 published standards for scientific accuracy
- **Chemical Formula Parsing**: Custom implementation supporting complex molecular structures