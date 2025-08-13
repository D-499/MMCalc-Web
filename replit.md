# MMCalc Web - Molar Mass Calculator

## Overview

MMCalc Web is a Flask-based web application that provides professional chemistry tools for calculating molar masses, reagent masses, and moles with precision formatting for analytical chemistry applications. The application is based on IUPAC 1995 Atomic Weights standards and offers multiple calculation modes along with a compound library for saving frequently used chemical formulas.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap-based responsive design
- **CSS Framework**: Bootstrap with dark theme and custom CSS for chemical formula styling
- **JavaScript**: Vanilla JavaScript for form validation, real-time input enhancement, and user experience improvements
- **UI Components**: Dark-themed interface with ASCII art branding, responsive navigation, and interactive forms

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
- **Schema**: Simple compound storage with name, formula, molar mass, and timestamp fields
- **Connection Pooling**: Configured with pool recycling and pre-ping for reliability

### Authentication and Authorization
- **Current State**: No authentication system implemented
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