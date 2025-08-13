/**
 * MMCalc Web - Client-side JavaScript
 * Enhances user experience with form validation and interactive features
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive features
    initializeFormValidation();
    initializeFormulaHelpers();
    initializeKeyboardShortcuts();
    initializeTooltips();
});

/**
 * Form validation and enhancement
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                e.stopPropagation();
            }
            
            // Add loading state to submit button
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Calculating...';
                
                // Re-enable after 5 seconds as fallback
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 5000);
            }
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input[required]');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                clearFieldValidation(this);
            });
        });
    });
}

/**
 * Validate entire form
 */
function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required]');
    
    inputs.forEach(input => {
        if (!validateField(input)) {
            isValid = false;
        }
    });
    
    return isValid;
}

/**
 * Validate individual field
 */
function validateField(field) {
    const value = field.value.trim();
    let isValid = true;
    let message = '';
    
    // Check if required field is empty
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        message = 'This field is required.';
    }
    
    // Specific validations based on field type/name
    if (field.name === 'formula' && value) {
        if (!isValidChemicalFormula(value)) {
            isValid = false;
            message = 'Please enter a valid chemical formula (e.g., H2SO4, Ca(OH)2).';
        }
    }
    
    if (field.type === 'number' && value) {
        const num = parseFloat(value);
        if (isNaN(num) || num <= 0) {
            isValid = false;
            message = 'Please enter a positive number.';
        }
    }
    
    // Apply validation styling
    if (isValid) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
        hideFieldError(field);
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
        showFieldError(field, message);
    }
    
    return isValid;
}

/**
 * Basic chemical formula validation
 */
function isValidChemicalFormula(formula) {
    // Allow letters, numbers, parentheses
    const basicPattern = /^[A-Za-z0-9()]+$/;
    if (!basicPattern.test(formula)) return false;
    
    // Check for balanced parentheses
    let depth = 0;
    for (let char of formula) {
        if (char === '(') depth++;
        if (char === ')') depth--;
        if (depth < 0) return false; // Closing before opening
    }
    
    return depth === 0; // All parentheses closed
}

/**
 * Clear field validation state
 */
function clearFieldValidation(field) {
    field.classList.remove('is-valid', 'is-invalid');
    hideFieldError(field);
}

/**
 * Show field error message
 */
function showFieldError(field, message) {
    hideFieldError(field); // Remove existing error
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    
    field.parentNode.appendChild(errorDiv);
}

/**
 * Hide field error message
 */
function hideFieldError(field) {
    const existingError = field.parentNode.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }
}

/**
 * Formula input helpers
 */
function initializeFormulaHelpers() {
    const formulaInputs = document.querySelectorAll('input[name="compound"], input[name="formula"]');
    
    formulaInputs.forEach(input => {
        // Auto-capitalize first letter of elements
        input.addEventListener('input', function() {
            let value = this.value;
            
            // Remove spaces
            value = value.replace(/\s/g, '');
            
            // Auto-capitalize element symbols (basic)
            value = value.replace(/\b([a-z])/g, function(match) {
                return match.toUpperCase();
            });
            
            this.value = value;
        });
        
        // Show common formulas on focus
        input.addEventListener('focus', function() {
            showFormulaExamples(this);
        });
        
        input.addEventListener('blur', function() {
            hideFormulaExamples(this);
        });
    });
}

/**
 * Show formula examples
 */
function showFormulaExamples(input) {
    const examples = [
        'H2SO4 (Sulfuric Acid)',
        'Ca(OH)2 (Calcium Hydroxide)',
        'CH3(CH2)3OH (Butanol)',
        'Mg3(PO4)2 (Magnesium Phosphate)',
        'C6H12O6 (Glucose)',
        'NaCl (Sodium Chloride)'
    ];
    
    // Update placeholder with rotating examples
    let currentExample = 0;
    const originalPlaceholder = input.getAttribute('placeholder');
    
    const rotateExamples = () => {
        input.setAttribute('placeholder', examples[currentExample]);
        currentExample = (currentExample + 1) % examples.length;
    };
    
    // Store original placeholder
    input.dataset.originalPlaceholder = originalPlaceholder;
    
    // Start rotation
    rotateExamples();
    input.dataset.exampleInterval = setInterval(rotateExamples, 2000);
}

/**
 * Hide formula examples
 */
function hideFormulaExamples(input) {
    if (input.dataset.exampleInterval) {
        clearInterval(input.dataset.exampleInterval);
        delete input.dataset.exampleInterval;
    }
    
    if (input.dataset.originalPlaceholder) {
        input.setAttribute('placeholder', input.dataset.originalPlaceholder);
    }
}

/**
 * Keyboard shortcuts
 */
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit form
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const form = document.querySelector('form');
            if (form) {
                form.requestSubmit();
            }
        }
        
        // Escape to clear form
        if (e.key === 'Escape') {
            const activeForm = document.querySelector('form');
            if (activeForm) {
                const inputs = activeForm.querySelectorAll('input[type="text"], input[type="number"]');
                inputs.forEach(input => {
                    input.value = '';
                    clearFieldValidation(input);
                });
                if (inputs.length > 0) {
                    inputs[0].focus();
                }
            }
        }
        
        // Quick mode switching (1, 2, 3)
        if (!e.target.matches('input, textarea, select')) {
            if (e.key >= '1' && e.key <= '3') {
                const modeUrl = new URL(window.location.origin + '/calculate');
                modeUrl.searchParams.set('mode', e.key);
                window.location.href = modeUrl.toString();
            }
        }
    });
}

/**
 * Initialize tooltips
 */
function initializeTooltips() {
    // Add tooltips to buttons and help icons
    const tooltipElements = document.querySelectorAll('[title]');
    
    tooltipElements.forEach(element => {
        // Simple tooltip implementation
        element.addEventListener('mouseenter', function() {
            showTooltip(this);
        });
        
        element.addEventListener('mouseleave', function() {
            hideTooltip(this);
        });
    });
}

/**
 * Show tooltip
 */
function showTooltip(element) {
    const tooltip = document.createElement('div');
    tooltip.className = 'custom-tooltip';
    tooltip.textContent = element.getAttribute('title');
    tooltip.style.cssText = `
        position: absolute;
        background: var(--bs-dark);
        color: var(--bs-light);
        padding: 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.875rem;
        z-index: 1000;
        pointer-events: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    `;
    
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
    
    element.dataset.tooltip = 'active';
}

/**
 * Hide tooltip
 */
function hideTooltip(element) {
    if (element.dataset.tooltip === 'active') {
        const tooltip = document.querySelector('.custom-tooltip');
        if (tooltip) {
            tooltip.remove();
        }
        delete element.dataset.tooltip;
    }
}

/**
 * Copy result to clipboard
 */
function copyToClipboard(text, element) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showCopyFeedback(element, 'Copied!');
        }).catch(() => {
            fallbackCopyToClipboard(text, element);
        });
    } else {
        fallbackCopyToClipboard(text, element);
    }
}

/**
 * Fallback copy method
 */
function fallbackCopyToClipboard(text, element) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showCopyFeedback(element, 'Copied!');
    } catch (err) {
        showCopyFeedback(element, 'Copy failed');
    }
    
    document.body.removeChild(textArea);
}

/**
 * Show copy feedback
 */
function showCopyFeedback(element, message) {
    const originalText = element.textContent;
    element.textContent = message;
    element.classList.add('text-success');
    
    setTimeout(() => {
        element.textContent = originalText;
        element.classList.remove('text-success');
    }, 1500);
}

/**
 * Format numbers for display
 */
function formatNumber(num, decimals = 3) {
    return parseFloat(num).toFixed(decimals);
}

/**
 * Add copy buttons to results
 */
function addCopyButtons() {
    const resultBoxes = document.querySelectorAll('.result-box h4');
    
    resultBoxes.forEach(resultElement => {
        if (!resultElement.querySelector('.copy-btn')) {
            const copyBtn = document.createElement('button');
            copyBtn.className = 'btn btn-sm btn-outline-secondary copy-btn ms-2';
            copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
            copyBtn.title = 'Copy to clipboard';
            copyBtn.onclick = (e) => {
                e.preventDefault();
                const textToCopy = resultElement.textContent.trim();
                copyToClipboard(textToCopy, copyBtn);
            };
            
            resultElement.appendChild(copyBtn);
        }
    });
}

// Add copy buttons when results are loaded
if (document.querySelector('.result-box')) {
    addCopyButtons();
}
