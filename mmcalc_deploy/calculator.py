"""
Molar Mass Calculator - Core calculation logic
Preserves exact functionality from the original CLI script
Based on Atomic Weights of the Elements 1995 published by IUPAC
"""

class MolarMassCalculator:
    def __init__(self):
        # Elements' atomic masses based on Atomic Weights of the Elements 1995 published by IUPAC
        self.element_masses = {
            "H": 1.008,
            "He": 4.003,
            "Li": 6.941,
            "Be": 9.012,
            "B": 10.81,
            "C": 12.01,
            "N": 14.01,
            "O": 16.00,
            "F": 19.00,
            "Ne": 20.18,
            "Na": 22.99,
            "Mg": 24.31,
            "Al": 26.98,
            "Si": 28.09,
            "P": 30.97,
            "S": 32.07,
            "Cl": 35.45,
            "Ar": 39.95,
            "K": 39.10,
            "Ca": 40.08,
            "Sc": 44.96,
            "Ti": 47.87,
            "V": 50.94,
            "Cr": 52.00,
            "Mn": 54.94,
            "Fe": 55.85,
            "Co": 58.93,
            "Ni": 58.69,
            "Cu": 63.55,
            "Zn": 65.39,
            "Ga": 69.72,
            "Ge": 72.61,
            "As": 74.92,
            "Se": 78.96,
            "Br": 79.90,
            "Kr": 83.80,
            "Rb": 85.47,
            "Sr": 87.62,
            "Y": 88.91,
            "Zr": 91.22,
            "Nb": 92.91,
            "Mo": 95.94,
            "Tc": 98.00,
            "Ru": 101.1,
            "Rh": 102.9,
            "Pd": 106.4,
            "Ag": 107.9,
            "Cd": 112.4,
            "In": 114.8,
            "Sn": 118.7,
            "Sb": 121.8,
            "Te": 127.6,
            "I": 126.9,
            "Xe": 131.3,
            "Cs": 132.9,
            "Ba": 137.3,
            "La": 138.9,
            "Ce": 140.1,
            "Pr": 140.9,
            "Nd": 144.2,
            "Pm": 145.00,
            "Sm": 150.4,
            "Eu": 152.0,
            "Gd": 157.3,
            "Tb": 158.9,
            "Dy": 162.5,
            "Ho": 164.9,
            "Er": 167.3,
            "Tm": 168.9,
            "Yb": 173.00,
            "Lu": 175.00,
            "Hf": 178.5,
            "Ta": 180.9,
            "W": 183.8,
            "Re": 186.2,
            "Os": 190.2,
            "Ir": 192.2,
            "Pt": 195.1,
            "Au": 197.00,
            "Hg": 200.6,
            "Tl": 204.4,
            "Pb": 207.2,
            "Bi": 209.0,
            "Po": 209.00,
            "At": 210.00,
            "Rn": 222.00,
            "Fr": 223.00,
            "Ra": 226.00,
            "Ac": 227.00,
            "Th": 232.0,
            "Pa": 231.0,
            "U": 238.0
        }

    def parse_formula(self, formula):
        """
        Read inputted formula, return a dictionary containing parsed elements and quantity
        Preserves exact logic from original CLI script
        """
        element_counts = {}  # Final count of elements
        stack = []  # Stack for handling parentheses
        i = 0  # Position in the formula

        while i < len(formula):
            char = formula[i]

            if char.isupper():  # Start of an element symbol
                element = char
                i += 1
                if i < len(formula) and formula[i].islower():  # Check if it's a two-letter symbol
                    element += formula[i]
                    i += 1

                # Read subscript (if any)
                num = 0
                while i < len(formula) and formula[i].isdigit():
                    num = num * 10 + int(formula[i])
                    i += 1
                num = max(num, 1)  # Default to 1 if no number

                element_counts[element] = element_counts.get(element, 0) + num

            elif char == '(':  # Opening a group
                stack.append((element_counts.copy(), i))  # Save current state
                element_counts = {}  # Start a new group
                i += 1

            elif char == ')':  # Closing a group
                i += 1
                num = 0
                while i < len(formula) and formula[i].isdigit():
                    num = num * 10 + int(formula[i])
                    i += 1
                num = max(num, 1)

                # Merge back with previous counts
                prev_counts, _ = stack.pop()
                for elem, count in element_counts.items():
                    prev_counts[elem] = prev_counts.get(elem, 0) + count * num
                element_counts = prev_counts  # Restore previous state

            else:
                # Invalid character detected in formula
                return {}
                # i += 1  # Skip unexpected characters (shouldn't occur in valid formulas)

        return element_counts

    def validate_elements(self, element_counts):
        """Checks for invalid elements"""
        for element in element_counts:
            if element not in self.element_masses.keys():
                return False
        return True

    def calculate_molar_mass(self, formula):
        """Calculate molar mass based on input formula"""
        element_counts = self.parse_formula(formula)
        if self.validate_elements(element_counts):
            total_mass = sum(self.element_masses[element] * count for element, count in element_counts.items())
            return total_mass
        else:
            return 0

    def calculate_reagent_mass(self, moles, compound):
        """Calculate reagent mass from moles and compound"""
        reagent_mass = moles * self.calculate_molar_mass(compound)
        return reagent_mass

    def calculate_moles(self, mass, compound):
        """Calculate moles from mass and compound"""
        molar_mass = self.calculate_molar_mass(compound)
        if molar_mass > 0:
            moles = mass / molar_mass
            return moles
        return 0
