import streamlit as st
import pandas as pd
import requests
from PIL import Image
import io

# Set page configuration with dark theme
st.set_page_config(
    page_title="Universal Unit Converter",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply dark theme including sidebar fixes
st.markdown("""
<style>
    /* Dark theme colors */
    :root {
        --background-color: #121212;
        --secondary-background-color: #1e1e1e;
        --text-color: #e0e0e0;
        --accent-color: #4e8df5;
        --accent-hover-color: #3a7bd5;
        --card-background: #1e1e1e;
        --header-color: #4e8df5;
        --result-background: #2d2d2d;
    }
    
    /* Main elements */
    .main {
        background-color: var(--background-color);
        color: var(--text-color);
        padding: 1rem;
    }
    
    .stApp {
        background-color: var(--background-color);
    }
    
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: var(--text-color) !important;
    }
    
    /* Sidebar styling - fixing the color issue */
    .css-1d391kg, .css-1lcbmhc, [data-testid="stSidebar"] {
        background-color: var(--secondary-background-color) !important;
    }
    
    [data-testid="stSidebar"] .sidebar-content {
        background-color: var(--secondary-background-color);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4, 
    [data-testid="stSidebar"] h5, 
    [data-testid="stSidebar"] h6, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] div, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stRadio label {
        color: var(--text-color) !important;
    }
    
    /* Radio buttons in sidebar */
    .stRadio > div {
        background-color: var(--secondary-background-color);
    }
    
    .stRadio label {
        color: var(--text-color) !important;
    }
    
    /* Sidebar divider */
    [data-testid="stSidebar"] hr {
        border-color: #444;
    }
    
    /* Sidebar info box */
    [data-testid="stSidebar"] .stAlert {
        background-color: var(--card-background);
        color: var(--text-color);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: var(--background-color);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 4px;
        padding: 10px 16px;
        background-color: var(--secondary-background-color);
        color: var(--text-color);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--accent-color) !important;
        color: white !important;
    }
    
    /* Converter card styling */
    .converter-card {
        background-color: var(--card-background);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: var(--header-color) !important;
    }
    
    /* Category header */
    .category-header {
        background-color: var(--secondary-background-color);
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    
    /* Result display */
    .result-display {
        background-color: var(--result-background);
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
        font-weight: bold;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background-color: var(--secondary-background-color);
        color: var(--text-color);
        border: 1px solid #444;
    }
    
    /* Select boxes */
    .stSelectbox > div > div > div {
        background-color: var(--secondary-background-color);
        color: var(--text-color);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .converter-card {
            padding: 15px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: auto;
            padding: 8px;
            font-size: 0.8rem;
        }
        
        .stColumns [data-testid="column"] {
            width: 100%;
            margin-bottom: 10px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🔄 Universal Unit Converter")
st.markdown("Convert units across various industries and general use cases")

# Sidebar for navigation
st.sidebar.title("Navigation")
category = st.sidebar.radio(
    "Select Category",
    ["General Converters", 
     "Fabric & Paper Industry", 
     "Metal & Engineering Industry", 
     "Plastic & Packaging Industry", 
     "Construction & Wood Industry"]
)

# Function to create a converter UI without button (auto-convert)
def create_converter(title, from_options, to_options, conversion_function):
    st.markdown(f"<div class='converter-card'>", unsafe_allow_html=True)
    st.subheader(title)
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        input_value = st.text_input("Enter value", value="1.0", key=f"{title}_input")
        from_unit = st.selectbox("From", from_options, key=f"{title}_from")
    
    with col2:
        st.markdown("<div style='display: flex; justify-content: center; align-items: center; height: 100%;'>➡️</div>", unsafe_allow_html=True)
    
    with col3:
        to_unit = st.selectbox("To", to_options, key=f"{title}_to")
        
        try:
            input_value = float(input_value)
            result = conversion_function(input_value, from_unit, to_unit)
            st.markdown(f"<div class='result-display'>Result: {result:.6g} {to_unit}</div>", unsafe_allow_html=True)
        except ValueError:
            st.error("Please enter a valid number")
    
    st.markdown("</div>", unsafe_allow_html=True)

# General Converters
if category == "General Converters":
    st.markdown("<div class='category-header'><h2>General Converters</h2></div>", unsafe_allow_html=True)
    
    # Length Converter
    length_units = ["mm", "cm", "m", "km", "in", "ft", "yd", "mi"]
    
    def convert_length(value, from_unit, to_unit):
        # Convert to meters first (base unit)
        to_meter = {
            "mm": 0.001,
            "cm": 0.01,
            "m": 1,
            "km": 1000,
            "in": 0.0254,
            "ft": 0.3048,
            "yd": 0.9144,
            "mi": 1609.34
        }
        
        # Convert from input unit to meters, then to output unit
        return value * to_meter[from_unit] / to_meter[to_unit]
    
    create_converter("Length Converter", length_units, length_units, convert_length)
    
    # Weight Converter
    weight_units = ["mg", "g", "kg", "ton", "oz", "lb", "st", "ton (US)"]
    
    def convert_weight(value, from_unit, to_unit):
        # Convert to grams first (base unit)
        to_gram = {
            "mg": 0.001,
            "g": 1,
            "kg": 1000,
            "ton": 1000000,  # metric ton
            "oz": 28.3495,
            "lb": 453.592,
            "st": 6350.29,  # stone
            "ton (US)": 907185  # US ton
        }
        
        # Convert from input unit to grams, then to output unit
        return value * to_gram[from_unit] / to_gram[to_unit]
    
    create_converter("Weight Converter", weight_units, weight_units, convert_weight)
    
    # Temperature Converter
    temp_units = ["Celsius", "Fahrenheit", "Kelvin"]
    
    def convert_temperature(value, from_unit, to_unit):
        # First convert to Celsius
        if from_unit == "Fahrenheit":
            celsius = (value - 32) * 5/9
        elif from_unit == "Kelvin":
            celsius = value - 273.15
        else:
            celsius = value
        
        # Then convert from Celsius to target unit
        if to_unit == "Fahrenheit":
            return celsius * 9/5 + 32
        elif to_unit == "Kelvin":
            return celsius + 273.15
        else:
            return celsius
    
    create_converter("Temperature Converter", temp_units, temp_units, convert_temperature)
    
    # Time Converter
    time_units = ["milliseconds", "seconds", "minutes", "hours", "days", "weeks", "months", "years"]
    
    def convert_time(value, from_unit, to_unit):
        # Convert to seconds first (base unit)
        to_seconds = {
            "milliseconds": 0.001,
            "seconds": 1,
            "minutes": 60,
            "hours": 3600,
            "days": 86400,
            "weeks": 604800,
            "months": 2592000,  # 30 days
            "years": 31536000  # 365 days
        }
        
        # Convert from input unit to seconds, then to output unit
        return value * to_seconds[from_unit] / to_seconds[to_unit]
    
    create_converter("Time Converter", time_units, time_units, convert_time)
    
    # Speed Converter
    speed_units = ["m/s", "km/h", "mph", "knot", "ft/s"]
    
    def convert_speed(value, from_unit, to_unit):
        # Convert to m/s first (base unit)
        to_ms = {
            "m/s": 1,
            "km/h": 0.277778,
            "mph": 0.44704,
            "knot": 0.514444,
            "ft/s": 0.3048
        }
        
        # Convert from input unit to m/s, then to output unit
        return value * to_ms[from_unit] / to_ms[to_unit]
    
    create_converter("Speed Converter", speed_units, speed_units, convert_speed)
    
    # Area Converter
    area_units = ["sq mm", "sq cm", "sq m", "hectare", "sq km", "sq in", "sq ft", "sq yd", "acre", "sq mi"]
    
    def convert_area(value, from_unit, to_unit):
        # Convert to square meters first (base unit)
        to_sqm = {
            "sq mm": 0.000001,
            "sq cm": 0.0001,
            "sq m": 1,
            "hectare": 10000,
            "sq km": 1000000,
            "sq in": 0.00064516,
            "sq ft": 0.092903,
            "sq yd": 0.836127,
            "acre": 4046.86,
            "sq mi": 2589988.11
        }
        
        # Convert from input unit to square meters, then to output unit
        return value * to_sqm[from_unit] / to_sqm[to_unit]
    
    create_converter("Area Converter", area_units, area_units, convert_area)
    
    # Volume Converter
    volume_units = ["ml", "l", "cu cm", "cu m", "cu in", "cu ft", "fl oz", "gal (US)", "gal (UK)"]
    
    def convert_volume(value, from_unit, to_unit):
        # Convert to liters first (base unit)
        to_liter = {
            "ml": 0.001,
            "l": 1,
            "cu cm": 0.001,
            "cu m": 1000,
            "cu in": 0.0163871,
            "cu ft": 28.3168,
            "fl oz": 0.0295735,
            "gal (US)": 3.78541,
            "gal (UK)": 4.54609
        }
        
        # Convert from input unit to liters, then to output unit
        return value * to_liter[from_unit] / to_liter[to_unit]
    
    create_converter("Volume Converter", volume_units, volume_units, convert_volume)
    
    # Pressure Converter
    pressure_units = ["Pa", "kPa", "MPa", "bar", "psi", "atm", "mmHg", "inHg"]
    
    def convert_pressure(value, from_unit, to_unit):
        # Convert to Pascal first (base unit)
        to_pascal = {
            "Pa": 1,
            "kPa": 1000,
            "MPa": 1000000,
            "bar": 100000,
            "psi": 6894.76,
            "atm": 101325,
            "mmHg": 133.322,
            "inHg": 3386.39
        }
        
        # Convert from input unit to Pascal, then to output unit
        return value * to_pascal[from_unit] / to_pascal[to_unit]
    
    create_converter("Pressure Converter", pressure_units, pressure_units, convert_pressure)
    
    # Energy Converter
    energy_units = ["J", "kJ", "cal", "kcal", "Wh", "kWh", "BTU", "ft-lb"]
    
    def convert_energy(value, from_unit, to_unit):
        # Convert to Joules first (base unit)
        to_joule = {
            "J": 1,
            "kJ": 1000,
            "cal": 4.184,
            "kcal": 4184,
            "Wh": 3600,
            "kWh": 3600000,
            "BTU": 1055.06,
            "ft-lb": 1.35582
        }
        
        # Convert from input unit to Joules, then to output unit
        return value * to_joule[from_unit] / to_joule[to_unit]
    
    create_converter("Energy Converter", energy_units, energy_units, convert_energy)
    
    # Power Converter
    power_units = ["W", "kW", "MW", "hp", "BTU/h", "ft-lb/s"]
    
    def convert_power(value, from_unit, to_unit):
        # Convert to Watts first (base unit)
        to_watt = {
            "W": 1,
            "kW": 1000,
            "MW": 1000000,
            "hp": 745.7,
            "BTU/h": 0.293071,
            "ft-lb/s": 1.35582
        }
        
        # Convert from input unit to Watts, then to output unit
        return value * to_watt[from_unit] / to_watt[to_unit]
    
    create_converter("Power Converter", power_units, power_units, convert_power)
    
    # Data Storage Converter
    data_units = ["bit", "Byte", "KB", "MB", "GB", "TB", "PB"]
    
    def convert_data(value, from_unit, to_unit):
        # Convert to bits first (base unit)
        to_bit = {
            "bit": 1,
            "Byte": 8,
            "KB": 8 * 1024,
            "MB": 8 * 1024**2,
            "GB": 8 * 1024**3,
            "TB": 8 * 1024**4,
            "PB": 8 * 1024**5
        }
        
        # Convert from input unit to bits, then to output unit
        return value * to_bit[from_unit] / to_bit[to_unit]
    
    create_converter("Data Storage Converter", data_units, data_units, convert_data)
    
    # Currency Converter
    currency_units = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CNY", "INR"]
    
    def convert_currency(value, from_unit, to_unit):
        # Exchange rates relative to USD (as of a certain date)
        to_usd = {
            "USD": 1,
            "EUR": 1.09,
            "GBP": 1.27,
            "JPY": 0.0067,
            "CAD": 0.74,
            "AUD": 0.66,
            "CNY": 0.14,
            "INR": 0.012
        }
        
        # Convert from input currency to USD, then to output currency
        return value * to_usd[from_unit] / to_usd[to_unit]
    
    create_converter("Currency Converter", currency_units, currency_units, convert_currency)
    
    st.info("Note: Currency rates are fixed for demonstration purposes. In a production app, these would be fetched from an API.")
    
    # Angle Converter
    angle_units = ["degree", "radian", "gradian", "minute of arc", "second of arc"]
    
    def convert_angle(value, from_unit, to_unit):
        # Convert to radians first (base unit)
        to_radian = {
            "degree": 0.0174533,
            "radian": 1,
            "gradian": 0.0157080,
            "minute of arc": 0.000290888,
            "second of arc": 4.84814e-6
        }
        
        # Convert from input unit to radians, then to output unit
        return value * to_radian[from_unit] / to_radian[to_unit]
    
    create_converter("Angle Converter", angle_units, angle_units, convert_angle)
    
    # Fuel Efficiency Converter
    fuel_units = ["mpg (US)", "mpg (UK)", "km/l", "l/100km"]
    
    def convert_fuel_efficiency(value, from_unit, to_unit):
        # First convert to l/100km (base unit)
        if from_unit == "mpg (US)":
            l_per_100km = 235.215 / value
        elif from_unit == "mpg (UK)":
            l_per_100km = 282.481 / value
        elif from_unit == "km/l":
            l_per_100km = 100 / value
        else:
            l_per_100km = value
        
        # Then convert from l/100km to target unit
        if to_unit == "mpg (US)":
            return 235.215 / l_per_100km
        elif to_unit == "mpg (UK)":
            return 282.481 / l_per_100km
        elif to_unit == "km/l":
            return 100 / l_per_100km
        else:
            return l_per_100km
    
    create_converter("Fuel Efficiency Converter", fuel_units, fuel_units, convert_fuel_efficiency)
    
    # Frequency Converter
    freq_units = ["Hz", "kHz", "MHz", "GHz", "rpm", "rad/s"]
    
    def convert_frequency(value, from_unit, to_unit):
        # Convert to Hz first (base unit)
        to_hz = {
            "Hz": 1,
            "kHz": 1000,
            "MHz": 1000000,
            "GHz": 1000000000,
            "rpm": 1/60,
            "rad/s": 1/(2*3.14159)
        }
        
        # Convert from input unit to Hz, then to output unit
        return value * to_hz[from_unit] / to_hz[to_unit]
    
    create_converter("Frequency Converter", freq_units, freq_units, convert_frequency)

# Fabric & Paper Industry
elif category == "Fabric & Paper Industry":
    st.markdown("<div class='category-header'><h2>Fabric & Paper Industry Converters</h2></div>", unsafe_allow_html=True)
    
    # Create tabs for different converter types
    fabric_tabs = st.tabs([
        "GSM", "Thickness", "Elongation", "Moisture Content", "Brightness & Opacity"
    ])
    
    # GSM Converter
    with fabric_tabs[0]:
        gsm_units = ["GSM", "oz/yd²", "lb/ream", "kg/ream"]
        
        def convert_gsm(value, from_unit, to_unit):
            # Convert to GSM first (base unit)
            to_gsm = {
                "GSM": 1,
                "oz/yd²": 33.906,
                "lb/ream": 1.48,  # 500 sheets of 25x38 inch paper
                "kg/ream": 0.6719  # 500 sheets of A0 paper
            }
            
            # Convert from input unit to GSM, then to output unit
            return value * to_gsm[from_unit] / to_gsm[to_unit]
        
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            input_value = st.text_input("Enter value", value="100", key="gsm_input")
            from_unit = st.selectbox("From", gsm_units, key="gsm_from")
        
        with col2:
            st.markdown("<div style='display: flex; justify-content: center; align-items: center; height: 100%;'>➡️</div>", unsafe_allow_html=True)
        
        with col3:
            to_unit = st.selectbox("To", gsm_units, key="gsm_to")
            
            try:
                input_value = float(input_value)
                result = convert_gsm(input_value, from_unit, to_unit)
                st.markdown(f"<div class='result-display'>Result: {result:.6g} {to_unit}</div>", unsafe_allow_html=True)
            except ValueError:
                st.error("Please enter a valid number")
        
        st.markdown("""
        **About GSM:**
        - GSM (Grams per Square Meter) is a measure of paper or fabric weight
        - Higher GSM indicates thicker/heavier material
        - Common paper GSM ranges: 80-100 for office paper, 170-300 for card stock
        """)
    
    # Thickness Converter
    with fabric_tabs[1]:
        thickness_units = ["mm", "cm", "mil", "inch", "point (pt)"]
        
        def convert_thickness(value, from_unit, to_unit):
            # Convert to mm first (base unit)
            to_mm = {
                "mm": 1,
                "cm": 10,
                "mil": 0.0254,  # 1 mil = 0.001 inch
                "inch": 25.4,
                "point (pt)": 0.0352778  # 1 pt = 1/72 inch
            }
            
            # Convert from input unit to mm, then to output unit
            return value * to_mm[from_unit] / to_mm[to_unit]
        
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            input_value = st.text_input("Enter value", value="1", key="thickness_input")
            from_unit = st.selectbox("From", thickness_units, key="thickness_from")
        
        with col2:
            st.markdown("<div style='display: flex; justify-content: center; align-items: center; height: 100%;'>➡️</div>", unsafe_allow_html=True)
        
        with col3:
            to_unit = st.selectbox("To", thickness_units, key="thickness_to")
            
            try:
                input_value = float(input_value)
                result = convert_thickness(input_value, from_unit, to_unit)
                st.markdown(f"<div class='result-display'>Result: {result:.6g} {to_unit}</div>", unsafe_allow_html=True)
            except ValueError:
                st.error("Please enter a valid number")
        
        st.markdown("""
        **About Thickness Measurements:**
        - Paper thickness is often measured in points (pt) where 1 pt = 1/1000 inch
        - Fabric thickness may be measured in mm or mil
        - Caliper is another term for thickness in the paper industry
        """)
    
    # Elongation Converter
    with fabric_tabs[2]:
        elongation_units = ["%", "mm/mm", "in/in", "cm/m"]
        
        def convert_elongation(value, from_unit, to_unit):
            # Convert to % first (base unit)
            to_percent = {
                "%": 1,
                "mm/mm": 100,
                "in/in": 100,
                "cm/m": 1  # 1 cm/m = 1%
            }
            
            # Convert from input unit to %, then to output unit
            return value * to_percent[from_unit] / to_percent[to_unit]
        
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            input_value = st.text_input("Enter value", value="5", key="elongation_input")
            from_unit = st.selectbox("From", elongation_units, key="elongation_from")
        
        with col2:
            st.markdown("<div style='display: flex; justify-content: center; align-items: center; height: 100%;'>➡️</div>", unsafe_allow_html=True)
        
        with col3:
            to_unit = st.selectbox("To", elongation_units, key="elongation_to")
            
            try:
                input_value = float(input_value)
                result = convert_elongation(input_value, from_unit, to_unit)
                st.markdown(f"<div class='result-display'>Result: {result:.6g} {to_unit}</div>", unsafe_allow_html=True)
            except ValueError:
                st.error("Please enter a valid number")
        
        st.markdown("""
        **About Elongation:**
        - Elongation is the increase in length expressed as a percentage of the original length
        - Important for textiles and papers to determine stretchability
        - Higher elongation indicates more elastic material
        """)
    
    # Moisture Content Converter
    with fabric_tabs[3]:
        moisture_units = ["% (wet basis)", "% (dry basis)", "moisture ratio"]
        
        def convert_moisture(value, from_unit, to_unit):
            # First convert to wet basis
            if from_unit == "% (wet basis)":
                wet_basis = value
            elif from_unit == "% (dry basis)":
                wet_basis = (value / (100 + value)) * 100
            else:  # moisture ratio
                wet_basis = (value / (1 + value)) * 100
            
            # Then convert from wet basis to target unit
            if to_unit == "% (wet basis)":
                return wet_basis
            elif to_unit == "% (dry basis)":
                return (wet_basis / (100 - wet_basis)) * 100
            else:  # moisture ratio
                return wet_basis / (100 - wet_basis)
        
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            input_value = st.text_input("Enter value", value="10", key="moisture_input")
            from_unit = st.selectbox("From", moisture_units, key="moisture_from")
        
        with col2:
            st.markdown("<div style='display: flex; justify-content: center; align-items: center; height: 100%;'>➡️</div>", unsafe_allow_html=True)
        
        with col3:
            to_unit = st.selectbox("To", moisture_units, key="moisture_to")
            
            try:
                input_value = float(input_value)
                result = convert_moisture(input_value, from_unit, to_unit)
                st.markdown(f"<div class='result-display'>Result: {result:.6g} {to_unit}</div>", unsafe_allow_html=True)
            except ValueError:
                st.error("Please enter a valid number")
        
        st.markdown("""
        **About Moisture Content:**
        - Wet basis: (water weight / total weight) × 100%
        - Dry basis: (water weight / dry weight) × 100%
        - Moisture ratio: water weight / dry weight
        - Critical for paper manufacturing and textile processing
        """)
    
    # Brightness & Opacity Converter
    with fabric_tabs[4]:
        brightness_units = ["% ISO", "% GE", "% TAPPI", "CIE Whiteness"]
        
        def convert_brightness(value, from_unit, to_unit):
            # These are approximate conversions
            if from_unit == to_unit:
                return value
            
            # Convert to ISO first (base unit)
            if from_unit == "% ISO":
                iso = value
            elif from_unit == "% GE":
                iso = value * 0.98  # Approximate
            elif from_unit == "% TAPPI":
                iso = value * 0.97  # Approximate
            else:  # CIE Whiteness
                iso = value * 0.9  # Very approximate
            
            # Then convert from ISO to target unit
            if to_unit == "% ISO":
                return iso
            elif to_unit == "% GE":
                return iso / 0.98
            elif to_unit == "% TAPPI":
                return iso / 0.97
            else:  # CIE Whiteness
                return iso / 0.9
        
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            input_value = st.text_input("Enter value", value="90", key="brightness_input")
            from_unit = st.selectbox("From", brightness_units, key="brightness_from")
        
        with col2:
            st.markdown("<div style='display: flex; justify-content: center; align-items: center; height: 100%;'>➡️</div>", unsafe_allow_html=True)
        
        with col3:
            to_unit = st.selectbox("To", brightness_units, key="brightness_to")
            
            try:
                input_value = float(input_value)
                result = convert_brightness(input_value, from_unit, to_unit)
                st.markdown(f"<div class='result-display'>Result: {result:.6g} {to_unit}</div>", unsafe_allow_html=True)
            except ValueError:
                st.error("Please enter a valid number")
        
        st.markdown("""
        **About Brightness & Whiteness:**
        - ISO Brightness: Measures reflectance of blue light (457 nm)
        - GE Brightness: General Electric scale, similar to ISO
        - TAPPI Brightness: Technical Association of the Pulp and Paper Industry standard
        - CIE Whiteness: Comprehensive measure including brightness and tint
        - Note: These conversions are approximate as they measure different properties
        """)

# Metal & Engineering Industry
elif category == "Metal & Engineering Industry":
    st.markdown("<div class='category-header'><h2>Metal & Engineering Industry Converters</h2></div>", unsafe_allow_html=True)
    
    # Create tabs for different converter types
    metal_tabs = st.tabs([
        "Hardness", "Tensile Strength", "Yield Strength", "Coating Thickness"
    ])
    
    # Hardness Converter
    with metal_tabs[0]:
        hardness_units = ["HRC (Rockwell C)", "HRB (Rockwell B)", "HV (Vickers)", "HB (Brinell)", "Shore D"]
        
        def convert_hardness(value, from_unit, to_unit):
            # These conversions are approximate and valid only for certain ranges
            if from_unit == to_unit:
                return value
            
            # First convert to HRC (base unit for this converter)
            if from_unit == "HRC (Rockwell C)":
                hrc = value
            elif from_unit == "HRB (Rockwell B)":
                if value < 30:
                    hrc = 0
                else:
                    hrc = (value - 30) * 0.8  # Approximate
            elif from_unit == "HV (Vickers)":
                if value < 240:
                    hrc = 0
                else:
                    hrc = (value - 240) * 0.1  # Approximate
            elif from_unit == "HB (Brinell)":
                if value < 200:
                    hrc = 0
                else:
                    hrc = (value - 200) * 0.1  # Approximate
            else:  # Shore D
                hrc = (value - 30) * 0.75  # Very approximate
            
            # Then convert from HRC to target unit
            if to_unit == "HRC (Rockwell C)":
                return hrc
            elif to_unit == "HRB (Rockwell B)":
                return 30 + hrc / 0.8
            elif to_unit == "HV (Vickers)":
                return 240 + hrc / 0.1
            elif to_unit == "HB (Brinell)":
                return 200 + hrc / 0.1
            else:  # Shore D
                return 30 + hrc / 0.75
        
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            input_value = st.text_input("Enter value", value="45", key="hardness_input")
            from_unit = st.selectbox("From", hardness_units, key="hardness_from")
        
        with col2:
            st.markdown("<div style='display: flex; justify-content: center; align-items: center; height: 100%;'>➡️</div>", unsafe_allow_html=True)
        
        with col3:
            to_unit = st.selectbox("To", hardness_units, key="hardness_to")
            
            try:
                input_value = float(input_value)
                result = convert_hardness(input_value, from_unit, to_unit)
                st.markdown(f"<div class='result-display'>Result: {result:.6g} {to_unit}</div>", unsafe_allow_html=True)
            except ValueError:
                st.error("Please enter a valid number")
        
        st.markdown("""
        **About Hardness Scales:**
        - Rockwell C (HRC): Used for harder materials like hardened steel
        - Rockwell B (HRB): Used for softer materials like mild steel, brass
        - Vickers (HV): Uses a diamond pyramid indenter, suitable for a wide range of materials
        - Brinell (HB): Uses a hardened steel ball, good for cast iron and non-ferrous metals
        - Shore D: Used for hard plastics and hard rubbers
        
        **Note:** These conversions are approximate as the scales measure different properties and are valid only within certain ranges.
        """)
    
    # Tensile Strength Converter
    with metal_tabs[1]:
        tensile_units = ["MPa", "N/mm²", "psi", "ksi", "kgf/mm²"]
        
        def convert_tensile(value, from_unit, to_unit):
            # Convert to MPa first (base unit)
            to_mpa = {
                "MPa": 1,
                "N/mm²": 1,  # Same as MPa
                "psi": 0.00689476,
                "ksi": 6.89476,
                "kgf/mm²": 9.80665
            }
            
            # Convert from input unit to MPa, then to output unit
            return value * to_mpa[from_unit] / to_mpa[to_unit]
        
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            input_value = st.text_input("Enter value", value="400", key="tensile_input")
            from_unit = st.selectbox("From", tensile_units, key="tensile_from")
        
        with col2:
            st.markdown("<div style='display: flex; justify-content: center; align-items: center; height: 100%;'>➡️</div>", unsafe_allow_html=True)
        
        with col3:
            to_unit = st.selectbox("To", tensile_units, key="tensile_to")
            
            try:
                input_value = float(input_value)
                result = convert_tensile(input_value, from_unit, to_unit)
                st.markdown(f"<div class='result-display'>Result: {result:.6g} {to_unit}</div>", unsafe_allow_html=True)
            except ValueError:
                st.error("Please enter a valid number")
        
        st.markdown("""
        **About Tensile Strength:**
        - Tensile strength is the maximum stress a material can withstand while being stretched before breaking
        - MPa (Megapascal) and N/mm² are identical units
        - Common values:
          - Mild steel: ~400 MPa
          - Aluminum alloys: 70-700 MPa
          - Titanium alloys: 900-1200 MPa
        """)
    
    # Yield Strength Converter
    with metal_tabs[2]:
        yield_units = ["MPa", "N/mm²", "psi", "ksi", "kgf/mm²"]
        
        def convert_yield(value, from_unit, to_unit):
            # Convert to MPa first (base unit)
            to_mpa = {
                "MPa": 1,
                "N/mm²": 1,  # Same as MPa
                "psi": 0.00689476,
                "ksi": 6.89476,
                "kgf/mm²": 9.80665
            }
            
            # Convert from input unit to MPa, then to output unit
            return value * to_mpa[from_unit] / to_mpa[to_unit]
        
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            input_value = st.text_input("Enter value", value="250", key="yield_input")
            from_unit = st.selectbox("From", yield_units, key="yield_from")
        
        with col2:
            st.markdown("<div style='display: flex; justify-content: center; align-items: center; height: 100%;'>➡️</div>", unsafe_allow_html=True)
        
        with col3:
            to_unit = st.selectbox("To", yield_units, key="yield_to")
            
            try:
                input_value = float(input_value)
                result = convert_yield(input_value, from_unit, to_unit)
                st.markdown(f"<div class='result-display'>Result: {result:.6g} {to_unit}</div>", unsafe_allow_html=True)
            except ValueError:
                st.error("Please enter a valid number")
        
        st.markdown("""
        **About Yield Strength:**
        - Yield strength is the stress at which a material begins to deform plastically
        - It marks the transition from elastic to plastic deformation
        - Common values:
          - Mild steel: ~250 MPa
          - Aluminum alloys: 35-500 MPa
          - Titanium alloys: 800-1100 MPa
        """)
    
    # Coating Thickness Converter
    with metal_tabs[3]:
        coating_units = ["μm", "mil", "mm", "inch", "gauge"]
        
        def convert_coating(value, from_unit, to_unit):
            # Convert to μm first (base unit)
            to_micron = {
                "μm": 1,
                "mil": 25.4,  # 1 mil = 0.001 inch
                "mm": 1000,
                "inch": 25400,
                "gauge": 8.128  # Approximate, varies by material
            }
            
            # Convert from input unit to μm, then to output unit
            return value * to_micron[from_unit] / to_micron[to_unit]
        
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            input_value = st.text_input("Enter value", value="10", key="coating_input")
            from_unit = st.selectbox("From", coating_units, key="coating_from")
        
        with col2:
            st.markdown("<div style='display: flex; justify-content: center; align-items: center; height: 100%;'>➡️</div>", unsafe_allow_html=True)
        
        with col3:
            to_unit = st.selectbox("To", coating_units, key="coating_to")
            
            try:
                input_value = float(input_value)
                result = convert_coating(input_value, from_unit, to_unit)
                st.markdown(f"<div class='result-display'>Result: {result:.6g} {to_unit}</div>", unsafe_allow_html=True)
            except ValueError:
                st.error("Please enter a valid number")
        
        st.markdown("""
        **About Coating Thickness:**
        - Common for measuring paint, galvanization, anodizing, and other surface treatments
        - Micron (μm) is the most common unit in industrial specifications
        - Mil is commonly used in the US (1 mil = 25.4 μm)
        - Gauge is an older unit system where higher numbers indicate thinner material
        """)

# Plastic & Packaging Industry
elif category == "Plastic & Packaging Industry":
    st.markdown("<div class='category-header'><h2>Plastic & Packaging Industry Converters</h2></div>", unsafe_allow_html=True)
    
    # Create tabs for different converter types
    plastic_tabs = st.tabs([
        "Micron (μm)", "Bursting Strength", "Tear Resistance", "Impact Strength", "Peel Strength"
    ])
    
    # Micron Converter
    with plastic_tabs[0]:
        micron_units = ["μm (micron)", "mil", "gauge", "mm", "inch"]
        
        def convert_micron(value, from_unit, to_unit):
            # Convert to micron first (base unit)
            to_micron = {
                "μm (micron)": 1,
                "mil": 25.4,  # 1 mil = 0.001 inch
                "gauge": 8.128,  # Approximate, varies by material
                "mm": 1000,
                "inch": 25400
            }
            
            # Convert from input unit to micron, then to output unit
            return value * to_micron[from_unit] / to_micron[to_unit]
        
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            input_value = st.text_input("Enter value", value="50", key="micron_input")
            from_unit = st.selectbox("From", micron_units, key="micron_from")
        
        with col2:
            st.markdown("<div style='display: flex; justify-content: center; align-items: center; height: 100%;'>➡️</div>", unsafe_allow_html=True)
        
        with col3:
            to_unit = st.selectbox("To", micron_units, key="micron_to")
            
            try:
                input_value = float(input_value)
                result = convert_micron(input_value, from_unit, to_unit)
                st.markdown(f"<div class='result-display'>Result: {result:.6g} {to_unit}</div>", unsafe_allow_html=True)
            except ValueError:
                st.error("Please enter a valid number")
        
        st.markdown("""
        **About Film Thickness:**
        - Micron (μm) is the standard metric unit for film thickness
        - Common plastic film thicknesses:
          - Grocery bags: 10-20 μm
          - Food packaging: 20-100 μm
          - Heavy duty bags: 100-250 μm
        - Gauge is an older unit system where the definition varies by material
        """)
    
    # Bursting Strength Converter
    with plastic_tabs[1]:
        burst_units = ["kPa", "psi", "kg/cm²", "bar"]
        
        def convert_burst(value, from_unit, to_unit):
            # Convert to kPa first (base unit)
            to_kpa = {
                "kPa": 1,
                "psi": 6.89476,
                "kg/cm²": 98.0665,
                "bar": 100
            }
            
            # Convert from input unit to kPa, then to output unit
            return value * to_kpa[from_unit] / to_kpa[to_unit]
        
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            input_value = st.text_input("Enter value", value="200", key="burst_input")
            from_unit = st.selectbox("From", burst_units, key="burst_from")
        
        with col2:
            st.markdown("<div style='display: flex; justify-content: center; align-items: center; height: 100%;'>➡️</div>", unsafe_allow_html=True)
        
        with col3:
            to_unit = st.selectbox("To", burst_units, key="burst_to")
            
            try:
                input_value = float(input_value)
                result = convert_burst(input_value, from_unit, to_unit)
                st.markdown(f"<div class='result-display'>Result: {result:.6g} {to_unit}</div>", unsafe_allow_html=True)
            except ValueError:
                st.error("Please enter a valid number")
        
        st.markdown("""
        **About Bursting Strength:**
        - Measures the pressure required to rupture a material
        - Critical for packaging materials that need to withstand pressure
        - Measured using Mullen test or similar methods
        - Higher values indicate stronger materials
        """)
    
    # Tear Resistance Converter
    with plastic_tabs[2]:
        tear_units = ["N", "gf", "mN", "lbf", "kgf"]
        
        def convert_tear(value, from_unit, to_unit):
            # Convert to N first (base unit)
            to_newton = {
                "N": 1,
                "gf": 0.00980665,
                "mN": 0.001,
                "lbf": 4.44822,
                "kgf": 9.80665
            }
            
            # Convert from input unit to N, then to output unit
            return value * to_newton[from_unit] / to_newton[to_unit]
        
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            input_value = st.text_input("Enter value", value="5", key="tear_input")
            from_unit = st.selectbox("From", tear_units, key="tear_from")
        
        with col2:
            st.markdown("<div style='display: flex; justify-content: center; align-items: center; height: 100%;'>➡️</div>", unsafe_allow_html=True)
        
        with col3:
            to_unit = st.selectbox("To", tear_units, key="tear_to")
            
            try:
                input_value = float(input_value)
                result = convert_tear(input_value, from_unit, to_unit)
                st.markdown(f"<div class='result-display'>Result: {result:.6g} {to_unit}</div>", unsafe_allow_html=True)
            except ValueError:
                st.error("Please enter a valid number")
        
        st.markdown("""
        **About Tear Resistance:**
        - Measures the force required to propagate a tear in a material
        - Important for packaging materials, films, and textiles
        - Commonly tested using Elmendorf tear test
        - Measured in force units (N, gf) rather than energy
        """)
    
    # Impact Strength Converter
    with plastic_tabs[3]:
        impact_units = ["J/m", "ft·lbf/in", "kJ/m²", "J/cm", "in·lbf/in"]
        
        def convert_impact(value, from_unit, to_unit):
            # Convert to J/m first (base unit)
            to_jm = {
                "J/m": 1,
                "ft·lbf/in": 53.3784,
                "kJ/m²": 1,  # For 1mm thickness
                "J/cm": 100,
                "in·lbf/in": 4.44822
            }
            
            # Convert from input unit to J/m, then to output unit
            return value * to_jm[from_unit] / to_jm[to_unit]
        
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            input_value = st.text_input("Enter value", value="10", key="impact_input")
            from_unit = st.selectbox("From", impact_units, key="impact_from")
        
        with col2:
            st.markdown("<div style='display: flex; justify-content: center; align-items: center; height: 100%;'>➡️</div>", unsafe_allow_html=True)
        
        with col3:
            to_unit = st.selectbox("To", impact_units, key="impact_to")
            
            try:
                input_value = float(input_value)
                result = convert_impact(input_value, from_unit, to_unit)
                st.markdown(f"<div class='result-display'>Result: {result:.6g} {to_unit}</div>", unsafe_allow_html=True)
            except ValueError:
                st.error("Please enter a valid number")
        
        st.markdown("""
        **About Impact Strength:**
        - Measures a material's ability to absorb energy during fracture
        - Critical for materials that need to withstand sudden forces
        - Common tests include Izod and Charpy impact tests
        - Higher values indicate more impact-resistant materials
        - Note: Conversions are approximate as test methods vary
        """)
    
    # Peel Strength Converter
    with plastic_tabs[4]:
        peel_units = ["N/25mm", "gf/25mm", "N/in", "lbf/in", "N/cm"]
        
        def convert_peel(value, from_unit, to_unit):
            # Convert to N/25mm first (base unit)
            to_n25mm = {
                "N/25mm": 1,
                "gf/25mm": 0.00980665,
                "N/in": 0.984252,  # 1 inch = 25.4 mm
                "lbf/in": 4.44822 * 0.984252,
                "N/cm": 2.5
            }
            
            # Convert from input unit to N/25mm, then to output unit
            return value * to_n25mm[from_unit] / to_n25mm[to_unit]
        
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            input_value = st.text_input("Enter value", value="2", key="peel_input")
            from_unit = st.selectbox("From", peel_units, key="peel_from")
        
        with col2:
            st.markdown("<div style='display: flex; justify-content: center; align-items: center; height: 100%;'>➡️</div>", unsafe_allow_html=True)
        
        with col3:
            to_unit = st.selectbox("To", peel_units, key="peel_to")
            
            try:
                input_value = float(input_value)
                result = convert_peel(input_value, from_unit, to_unit)
                st.markdown(f"<div class='result-display'>Result: {result:.6g} {to_unit}</div>", unsafe_allow_html=True)
            except ValueError:
                st.error("Please enter a valid number")
        
        st.markdown("""
        **About Peel Strength:**
        - Measures the force required to separate two bonded materials
        - Critical for adhesives, laminates, and sealed packages
        - Typically measured in force per width units
        - Higher values indicate stronger bonds
        - Common test methods include T-peel, 90° peel, and 180° peel tests
        """)

# Construction & Wood Industry
elif category == "Construction & Wood Industry":
    st.markdown("<div class='category-header'><h2>Construction & Wood Industry Converters</h2></div>", unsafe_allow_html=True)
    
    # Create tabs for different converter types
    construction_tabs = st.tabs([
        "Compressive Strength", "Wood Moisture Content", "Density", "Flexural Strength"
    ])
    
    # Compressive Strength Converter
    with construction_tabs[0]:
        compressive_units = ["MPa", "N/mm²", "psi", "ksi", "kg/cm²"]
        
        def convert_compressive(value, from_unit, to_unit):
            # Convert to MPa first (base unit)
            to_mpa = {
                "MPa": 1,
                "N/mm²": 1,  # Same as MPa
                "psi": 0.00689476,
                "ksi": 6.89476,
                "kg/cm²": 0.0980665
            }
            
            # Convert from input unit to MPa, then to output unit
            return value * to_mpa[from_unit] / to_mpa[to_unit]
        
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            input_value = st.text_input("Enter value", value="30", key="compressive_input")
            from_unit = st.selectbox("From", compressive_units, key="compressive_from")
        
        with col2:
            st.markdown("<div style='display: flex; justify-content: center; align-items: center; height: 100%;'>➡️</div>", unsafe_allow_html=True)
        
        with col3:
            to_unit = st.selectbox("To", compressive_units, key="compressive_to")
            
            try:
                input_value = float(input_value)
                result = convert_compressive(input_value, from_unit, to_unit)
                st.markdown(f"<div class='result-display'>Result: {result:.6g} {to_unit}</div>", unsafe_allow_html=True)
            except ValueError:
                st.error("Please enter a valid number")
        
        st.markdown("""
        **About Compressive Strength:**
        - Measures a material's ability to withstand loads that reduce size
        - Critical for concrete, wood, and structural materials
        - Common values:
          - Concrete: 20-40 MPa
          - Structural steel: 250-550 MPa
          - Wood (parallel to grain): 5-100 MPa
        """)
    
    # Wood Moisture Content Converter
    with construction_tabs[1]:
        moisture_units = ["% (wet basis)", "% (dry basis)", "moisture ratio"]
        
        def convert_wood_moisture(value, from_unit, to_unit):
            # First convert to wet basis
            if from_unit == "% (wet basis)":
                wet_basis = value
            elif from_unit == "% (dry basis)":
                wet_basis = (value / (100 + value)) * 100
            else:  # moisture ratio
                wet_basis = (value / (1 + value)) * 100
            
            # Then convert from wet basis to target unit
            if to_unit == "% (wet basis)":
                return wet_basis
            elif to_unit == "% (dry basis)":
                return (wet_basis / (100 - wet_basis)) * 100
            else:  # moisture ratio
                return wet_basis / (100 - wet_basis)
        
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            input_value = st.text_input("Enter value", value="12", key="wood_moisture_input")
            from_unit = st.selectbox("From", moisture_units, key="wood_moisture_from")
        
        with col2:
            st.markdown("<div style='display: flex; justify-content: center; align-items: center; height: 100%;'>➡️</div>", unsafe_allow_html=True)
        
        with col3:
            to_unit = st.selectbox("To", moisture_units, key="wood_moisture_to")
            
            try:
                input_value = float(input_value)
                result = convert_wood_moisture(input_value, from_unit, to_unit)
                st.markdown(f"<div class='result-display'>Result: {result:.6g} {to_unit}</div>", unsafe_allow_html=True)
            except ValueError:
                st.error("Please enter a valid number")
        
        st.markdown("""
        **About Wood Moisture Content:**
        - Wet basis: (water weight / total weight) × 100%
        - Dry basis: (water weight / dry weight) × 100%
        - Moisture ratio: water weight / dry weight
        - Equilibrium moisture content (EMC) varies by region and climate
        - Indoor wood typically has 6-8% moisture content
        - Green (freshly cut) wood can have 30-200% moisture content (dry basis)
        """)
    
    # Density Converter
    with construction_tabs[2]:
        density_units = ["kg/m³", "g/cm³", "lb/ft³", "lb/in³", "g/ml"]
        
        def convert_density(value, from_unit, to_unit):
            # Convert to kg/m³ first (base unit)
            to_kgm3 = {
                "kg/m³": 1,
                "g/cm³": 1000,
                "lb/ft³": 16.0185,
                "lb/in³": 27679.9,
                "g/ml": 1000
            }
            
            # Convert from input unit to kg/m³, then to output unit
            return value * to_kgm3[from_unit] / to_kgm3[to_unit]
        
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            input_value = st.text_input("Enter value", value="1000", key="density_input")
            from_unit = st.selectbox("From", density_units, key="density_from")
        
        with col2:
            st.markdown("<div style='display: flex; justify-content: center; align-items: center; height: 100%;'>➡️</div>", unsafe_allow_html=True)
        
        with col3:
            to_unit = st.selectbox("To", density_units, key="density_to")
            
            try:
                input_value = float(input_value)
                result = convert_density(input_value, from_unit, to_unit)
                st.markdown(f"<div class='result-display'>Result: {result:.6g} {to_unit}</div>", unsafe_allow_html=True)
            except ValueError:
                st.error("Please enter a valid number")
        
        st.markdown("""
        **About Density:**
        - Measures mass per unit volume
        - Critical for material selection and structural calculations
        - Common values:
          - Water: 1000 kg/m³ (1 g/cm³)
          - Concrete: 2300-2400 kg/m³
          - Steel: 7850 kg/m³
          - Softwoods: 350-700 kg/m³
          - Hardwoods: 600-1200 kg/m³
        """)
    
    # Flexural Strength Converter
    with construction_tabs[3]:
        flexural_units = ["MPa", "N/mm²", "psi", "ksi", "kg/cm²"]
        
        def convert_flexural(value, from_unit, to_unit):
            # Convert to MPa first (base unit)
            to_mpa = {
                "MPa": 1,
                "N/mm²": 1,  # Same as MPa
                "psi": 0.00689476,
                "ksi": 6.89476,
                "kg/cm²": 0.0980665
            }
            
            # Convert from input unit to MPa, then to output unit
            return value * to_mpa[from_unit] / to_mpa[to_unit]
        
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            input_value = st.text_input("Enter value", value="5", key="flexural_input")
            from_unit = st.selectbox("From", flexural_units, key="flexural_from")
        
        with col2:
            st.markdown("<div style='display: flex; justify-content: center; align-items: center; height: 100%;'>➡️</div>", unsafe_allow_html=True)
        
        with col3:
            to_unit = st.selectbox("To", flexural_units, key="flexural_to")
            
            try:
                input_value = float(input_value)
                result = convert_flexural(input_value, from_unit, to_unit)
                st.markdown(f"<div class='result-display'>Result: {result:.6g} {to_unit}</div>", unsafe_allow_html=True)
            except ValueError:
                st.error("Please enter a valid number")
        
        st.markdown("""
        **About Flexural Strength:**
        - Also known as bending strength or modulus of rupture
        - Measures a material's ability to resist deformation under load
        - Critical for beams, slabs, and structural elements
        - Common values:
          - Concrete: 3-5 MPa
          - Fiber-reinforced concrete: 7-10 MPa
          - Wood (parallel to grain): 10-100 MPa
        """)

# Footer
st.markdown("---")
st.markdown("### About This Tool")
st.markdown("""
This comprehensive unit converter is designed for professionals across various industries. It provides accurate conversions between different units of measurement, helping you work more efficiently.

**Features:**
- General converters for everyday use presented in a block format
- Industry-specific converters for specialized applications
- Clean, responsive interface with automatic conversion
- Dark theme for reduced eye strain
- Educational information about each unit type

**Note:** While we strive for accuracy, please verify critical conversions with official standards.
""")

# Sidebar footer
st.sidebar.markdown("---")
st.sidebar.markdown("© 2025 Universal Unit Converter")