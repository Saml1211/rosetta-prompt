"""
Theme Manager for Streamlit Application
Provides robust dark/light mode switching with CSS injection

This version uses high-specificity CSS selectors to properly override
Streamlit's dynamically-generated st-emotion-cache-* classes.

Features skeuomorphic design touches: subtle gradients, inner shadows,
beveled edges, and depth effects for a tactile feel.
"""

import streamlit as st


class ThemeManager:
    """Manages application theming with CSS injection."""
    
    # Color palettes using Zinc scale with skeuomorphic additions
    COLORS = {
        'dark': {
            'bg_primary': '#18181b',      # Zinc 900
            'bg_secondary': '#27272a',    # Zinc 800
            'bg_tertiary': '#3f3f46',     # Zinc 700
            'bg_elevated': '#52525b',     # Zinc 600 (for raised elements)
            'text_primary': '#fafafa',    # Zinc 50
            'text_secondary': '#a1a1aa',  # Zinc 400
            'accent': '#3b82f6',          # Blue 500
            'accent_light': '#60a5fa',    # Blue 400
            'accent_dark': '#2563eb',     # Blue 600
            'border': '#52525b',          # Zinc 600
            'border_light': '#71717a',    # Zinc 500
            'success_bg': 'rgba(34, 197, 94, 0.15)',
            'error_bg': 'rgba(239, 68, 68, 0.15)',
            'warning_bg': 'rgba(234, 179, 8, 0.15)',
            'info_bg': 'rgba(59, 130, 246, 0.15)',
            # Skeuomorphic shadows
            'shadow_inset': 'inset 0 2px 4px rgba(0, 0, 0, 0.4)',
            'shadow_raised': '0 2px 8px rgba(0, 0, 0, 0.4), 0 1px 2px rgba(0, 0, 0, 0.3)',
            'shadow_floating': '0 8px 24px rgba(0, 0, 0, 0.5)',
            'highlight_top': 'rgba(255, 255, 255, 0.05)',
            'highlight_bottom': 'rgba(0, 0, 0, 0.3)',
        },
        'light': {
            'bg_primary': '#ffffff',
            'bg_secondary': '#f4f4f5',    # Zinc 100
            'bg_tertiary': '#e4e4e7',     # Zinc 200
            'bg_elevated': '#fafafa',     # Zinc 50
            'text_primary': '#18181b',    # Zinc 900
            'text_secondary': '#71717a',  # Zinc 500
            'accent': '#3b82f6',          # Blue 500
            'accent_light': '#60a5fa',    # Blue 400
            'accent_dark': '#2563eb',     # Blue 600
            'border': '#d4d4d8',          # Zinc 300
            'border_light': '#e4e4e7',    # Zinc 200
            'success_bg': 'rgba(34, 197, 94, 0.1)',
            'error_bg': 'rgba(239, 68, 68, 0.1)',
            'warning_bg': 'rgba(234, 179, 8, 0.1)',
            'info_bg': 'rgba(59, 130, 246, 0.1)',
            # Skeuomorphic shadows (lighter for light mode)
            'shadow_inset': 'inset 0 2px 4px rgba(0, 0, 0, 0.1)',
            'shadow_raised': '0 2px 8px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.05)',
            'shadow_floating': '0 8px 24px rgba(0, 0, 0, 0.15)',
            'highlight_top': 'rgba(255, 255, 255, 0.8)',
            'highlight_bottom': 'rgba(0, 0, 0, 0.05)',
        }
    }
    
    @staticmethod
    def get_css(theme_mode: str = 'dark') -> str:
        """
        Generate comprehensive CSS for the specified theme.
        Uses high-specificity selectors to override Streamlit defaults.
        Includes skeuomorphic design elements for depth and tactility.
        
        Args:
            theme_mode: 'dark' or 'light'
            
        Returns:
            CSS string for injection
        """
        colors = ThemeManager.COLORS[theme_mode]
        
        # Gradient directions based on theme
        if theme_mode == 'dark':
            gradient_subtle = f"linear-gradient(180deg, {colors['highlight_top']} 0%, transparent 50%, {colors['highlight_bottom']} 100%)"
            input_gradient = f"linear-gradient(180deg, rgba(0,0,0,0.2) 0%, transparent 30%)"
            button_gradient = f"linear-gradient(180deg, rgba(255,255,255,0.1) 0%, transparent 50%, rgba(0,0,0,0.2) 100%)"
            accent_gradient = f"linear-gradient(180deg, {colors['accent_light']} 0%, {colors['accent']} 50%, {colors['accent_dark']} 100%)"
        else:
            gradient_subtle = f"linear-gradient(180deg, {colors['highlight_top']} 0%, transparent 100%)"
            input_gradient = f"linear-gradient(180deg, rgba(0,0,0,0.03) 0%, transparent 30%)"
            button_gradient = f"linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(255,255,255,0.5) 100%)"
            accent_gradient = f"linear-gradient(180deg, {colors['accent_light']} 0%, {colors['accent']} 100%)"
        
        return f"""
        <style>
        /* ============================================================
           GOOGLE FONTS IMPORT
           ============================================================ */
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
        
        /* ============================================================
           CSS CUSTOM PROPERTIES (Variables for reuse)
           ============================================================ */
        :root {{
            --theme-bg-primary: {colors['bg_primary']};
            --theme-bg-secondary: {colors['bg_secondary']};
            --theme-bg-tertiary: {colors['bg_tertiary']};
            --theme-text-primary: {colors['text_primary']};
            --theme-text-secondary: {colors['text_secondary']};
            --theme-accent: {colors['accent']};
            --theme-border: {colors['border']};
            --shadow-inset: {colors['shadow_inset']};
            --shadow-raised: {colors['shadow_raised']};
            --shadow-floating: {colors['shadow_floating']};
            
            /* Typography */
            --font-display: 'Space Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            --font-mono: 'JetBrains Mono', 'SF Mono', 'Fira Code', 'Monaco', monospace;
        }}
        
        /* ============================================================
           GLOBAL TYPOGRAPHY
           ============================================================ */
        
        html, body, .stApp {{
            font-family: var(--font-display) !important;
            font-weight: 400 !important;
            letter-spacing: -0.01em !important;
            -webkit-font-smoothing: antialiased !important;
            -moz-osx-font-smoothing: grayscale !important;
        }}
        
        /* Headers - Bold geometric */
        h1 {{
            font-family: var(--font-display) !important;
            font-weight: 700 !important;
            letter-spacing: -0.03em !important;
            font-size: 2.5rem !important;
        }}
        
        h2 {{
            font-family: var(--font-display) !important;
            font-weight: 600 !important;
            letter-spacing: -0.02em !important;
        }}
        
        h3, h4, h5, h6 {{
            font-family: var(--font-display) !important;
            font-weight: 500 !important;
            letter-spacing: -0.01em !important;
        }}
        
        /* Body text */
        p, span, li, label, div {{
            font-family: var(--font-display) !important;
        }}
        
        /* Monospace for inputs and code */
        textarea, input, code, pre, .stTextArea textarea, .stTextInput input {{
            font-family: var(--font-mono) !important;
            font-size: 0.9rem !important;
            font-weight: 400 !important;
        }}
        
        /* Buttons - Medium weight */
        button {{
            font-family: var(--font-display) !important;
            font-weight: 500 !important;
            letter-spacing: 0 !important;
        }}
        
        /* ============================================================
           GLOBAL OVERRIDES (High specificity)
           ============================================================ */
        
        /* Main app container */
        .stApp,
        .stApp > header,
        .stApp [data-testid="stAppViewContainer"],
        .stApp [data-testid="stAppViewBlockContainer"] {{
            background-color: {colors['bg_primary']} !important;
        }}
        
        /* Main content area with subtle texture */
        .main .block-container,
        .stApp .main .block-container,
        [data-testid="stAppViewBlockContainer"] > .main > .block-container {{
            background-color: {colors['bg_primary']} !important;
            color: {colors['text_primary']} !important;
        }}
        
        /* Nuclear override for ALL emotion cache divs in main content */
        .stApp [class*="st-emotion-cache"] {{
            background-color: transparent !important;
        }}
        
        /* ============================================================
           SIDEBAR - Skeuomorphic Panel
           ============================================================ */
        
        /* Sidebar with subtle gradient and shadow */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, 
                {colors['bg_secondary']} 0%, 
                {colors['bg_primary']} 100%) !important;
            box-shadow: 2px 0 12px rgba(0, 0, 0, 0.3),
                        inset -1px 0 0 {colors['border_light']} !important;
        }}
        
        /* Sidebar root and all children */
        [data-testid="stSidebar"] > div,
        [data-testid="stSidebar"] > div:first-child,
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"],
        [data-testid="stSidebar"] .element-container {{
            background-color: transparent !important;
        }}
        
        /* Sidebar emotion cache - force override */
        [data-testid="stSidebar"] [class*="st-emotion-cache"] {{
            background-color: transparent !important;
        }}
        
        /* Sidebar text */
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] .stMarkdown {{
            color: {colors['text_primary']} !important;
        }}
        
        /* ============================================================
           INPUT FIELDS - Recessed / Inset Skeuomorphic Style
           ============================================================ */
        
        /* Text inputs everywhere - recessed look */
        input[type="text"],
        input[type="password"],
        input[type="email"],
        input[type="number"],
        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input {{
            background: {input_gradient}, {colors['bg_tertiary']} !important;
            color: {colors['text_primary']} !important;
            border: 1px solid {colors['border']} !important;
            border-top-color: {colors['highlight_bottom']} !important;
            border-radius: 6px !important;
            box-shadow: {colors['shadow_inset']} !important;
            transition: all 0.2s ease !important;
        }}
        
        /* Input focus states - glow effect */
        input:focus,
        textarea:focus {{
            background: {colors['bg_tertiary']} !important;
            border-color: {colors['accent']} !important;
            outline: none !important;
            box-shadow: {colors['shadow_inset']},
                        0 0 0 3px rgba(59, 130, 246, 0.3) !important;
        }}
        
        /* Text areas - recessed with depth */
        textarea,
        [data-testid="stTextArea"] textarea,
        .stTextArea textarea {{
            background: {input_gradient}, {colors['bg_tertiary']} !important;
            color: {colors['text_primary']} !important;
            border: 1px solid {colors['border']} !important;
            border-top-color: {colors['highlight_bottom']} !important;
            border-radius: 8px !important;
            box-shadow: {colors['shadow_inset']} !important;
            transition: all 0.2s ease !important;
        }}
        
        /* Disabled inputs - flatter look */
        input:disabled,
        textarea:disabled,
        [data-testid="stTextArea"] textarea:disabled {{
            background-color: {colors['bg_secondary']} !important;
            color: {colors['text_secondary']} !important;
            opacity: 0.7;
            box-shadow: none !important;
        }}
        
        /* Placeholder text */
        ::placeholder {{
            color: {colors['text_secondary']} !important;
            opacity: 0.6;
        }}
        
        /* ============================================================
           SELECT BOXES AND DROPDOWNS - Raised Style
           ============================================================ */
        
        /* Selectbox container - raised button look */
        [data-testid="stSelectbox"] > div,
        [data-testid="stSelectbox"] > div > div,
        [data-baseweb="select"] {{
            background: {button_gradient}, {colors['bg_tertiary']} !important;
            border: 1px solid {colors['border']} !important;
            border-bottom-color: {colors['highlight_bottom']} !important;
            border-radius: 6px !important;
            box-shadow: {colors['shadow_raised']} !important;
            transition: all 0.15s ease !important;
        }}
        
        /* Selectbox hover */
        [data-baseweb="select"]:hover {{
            box-shadow: {colors['shadow_floating']} !important;
            transform: translateY(-1px);
        }}
        
        /* Selectbox trigger button text */
        [data-baseweb="select"] [data-testid="stMarkdownContainer"],
        [data-baseweb="select"] span {{
            color: {colors['text_primary']} !important;
        }}
        
        /* Dropdown popup/popover - floating panel */
        [data-baseweb="popover"],
        [data-baseweb="menu"],
        [data-baseweb="select"] [role="listbox"],
        [data-testid="stSelectbox"] [role="listbox"],
        div[data-baseweb="popover"] > div {{
            background: linear-gradient(180deg, 
                {colors['bg_elevated']} 0%, 
                {colors['bg_tertiary']} 100%) !important;
            border: 1px solid {colors['border_light']} !important;
            border-radius: 8px !important;
            box-shadow: {colors['shadow_floating']},
                        inset 0 1px 0 {colors['highlight_top']} !important;
            backdrop-filter: blur(8px);
        }}
        
        /* Dropdown options */
        [role="option"],
        [data-baseweb="menu"] li,
        [data-baseweb="select"] li {{
            background-color: transparent !important;
            color: {colors['text_primary']} !important;
            border-radius: 4px !important;
            margin: 2px 4px !important;
            transition: all 0.1s ease !important;
        }}
        
        /* Dropdown option hover - subtle highlight */
        [role="option"]:hover,
        [data-baseweb="menu"] li:hover {{
            background-color: {colors['accent']} !important;
            color: white !important;
            box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3) !important;
        }}
        
        /* ============================================================
           EXPANDERS - Card Style with Depth
           ============================================================ */
        
        /* Expander container - card with shadow */
        [data-testid="stExpander"],
        details[data-testid="stExpander"],
        .streamlit-expanderHeader {{
            background: linear-gradient(180deg, 
                {colors['bg_secondary']} 0%, 
                {colors['bg_primary']} 100%) !important;
            border: 1px solid {colors['border']} !important;
            border-radius: 10px !important;
            box-shadow: {colors['shadow_raised']},
                        inset 0 1px 0 {colors['highlight_top']} !important;
            overflow: hidden !important;
        }}
        
        /* Expander header/summary - beveled top */
        [data-testid="stExpander"] > summary,
        [data-testid="stExpander"] summary,
        details[data-testid="stExpander"] > summary,
        .streamlit-expanderHeader {{
            background: {button_gradient}, {colors['bg_secondary']} !important;
            color: {colors['text_primary']} !important;
            padding: 14px 18px !important;
            border-bottom: 1px solid {colors['border']} !important;
            cursor: pointer !important;
            transition: all 0.15s ease !important;
        }}
        
        /* Expander header emotion cache override */
        [data-testid="stExpander"] summary [class*="st-emotion-cache"],
        [data-testid="stExpander"] > summary [class*="st-emotion-cache"] {{
            background-color: transparent !important;
            color: {colors['text_primary']} !important;
        }}
        
        /* Expander header hover */
        [data-testid="stExpander"] > summary:hover,
        [data-testid="stExpander"] summary:hover {{
            background: {button_gradient}, {colors['bg_tertiary']} !important;
        }}
        
        /* Expander content body */
        [data-testid="stExpander"] > div:not(summary),
        [data-testid="stExpander"] > div:last-child,
        details[data-testid="stExpander"] > div {{
            background-color: {colors['bg_secondary']} !important;
            color: {colors['text_primary']} !important;
            padding: 18px !important;
        }}
        
        /* Expander content emotion cache override */
        [data-testid="stExpander"] > div [class*="st-emotion-cache"] {{
            background-color: transparent !important;
        }}
        
        /* All text inside expanders */
        [data-testid="stExpander"] .stMarkdown,
        [data-testid="stExpander"] p,
        [data-testid="stExpander"] li,
        [data-testid="stExpander"] h1,
        [data-testid="stExpander"] h2,
        [data-testid="stExpander"] h3,
        [data-testid="stExpander"] strong {{
            color: {colors['text_primary']} !important;
            background-color: transparent !important;
        }}
        
        /* ============================================================
           RADIO BUTTONS - Pill Toggle Style
           ============================================================ */
        
        /* Radio container */
        [data-testid="stRadio"],
        [data-testid="stRadio"] > div {{
            background-color: transparent !important;
        }}
        
        /* Radio labels */
        [data-testid="stRadio"] label,
        [data-baseweb="radio"] label {{
            color: {colors['text_primary']} !important;
            background-color: transparent !important;
        }}
        
        /* Radio button indicator */
        [data-baseweb="radio"] div[data-testid] {{
            border-color: {colors['border']} !important;
            box-shadow: {colors['shadow_inset']} !important;
        }}
        
        /* ============================================================
           BUTTONS - 3D Raised Style
           ============================================================ */
        
        /* Primary button - vibrant with depth */
        button[kind="primary"],
        .stButton > button[kind="primary"],
        [data-testid="stButton"] button[kind="primary"] {{
            background: {accent_gradient} !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4),
                        inset 0 1px 0 rgba(255, 255, 255, 0.2),
                        inset 0 -2px 0 rgba(0, 0, 0, 0.2) !important;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
            font-weight: 600 !important;
            transition: all 0.15s ease !important;
        }}
        
        /* Primary button hover - lift effect */
        button[kind="primary"]:hover,
        .stButton > button[kind="primary"]:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5),
                        inset 0 1px 0 rgba(255, 255, 255, 0.3),
                        inset 0 -2px 0 rgba(0, 0, 0, 0.2) !important;
        }}
        
        /* Primary button active - pressed */
        button[kind="primary"]:active,
        .stButton > button[kind="primary"]:active {{
            transform: translateY(1px) !important;
            box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3),
                        inset 0 2px 4px rgba(0, 0, 0, 0.3) !important;
        }}
        
        /* Secondary/default button - subtle raised */
        button[kind="secondary"],
        .stButton > button:not([kind="primary"]),
        [data-testid="stButton"] button:not([kind="primary"]) {{
            background: {button_gradient}, {colors['bg_tertiary']} !important;
            color: {colors['text_primary']} !important;
            border: 1px solid {colors['border']} !important;
            border-bottom-color: {colors['highlight_bottom']} !important;
            border-radius: 8px !important;
            box-shadow: {colors['shadow_raised']} !important;
            font-weight: 500 !important;
            transition: all 0.15s ease !important;
        }}
        
        /* Secondary button hover */
        button[kind="secondary"]:hover,
        .stButton > button:not([kind="primary"]):hover {{
            transform: translateY(-1px) !important;
            box-shadow: {colors['shadow_floating']} !important;
        }}
        
        /* Secondary button active */
        button[kind="secondary"]:active,
        .stButton > button:not([kind="primary"]):active {{
            transform: translateY(1px) !important;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2) !important;
        }}
        
        /* Disabled button */
        button:disabled {{
            opacity: 0.5 !important;
            cursor: not-allowed !important;
            transform: none !important;
            box-shadow: none !important;
        }}
        
        /* ============================================================
           ALERTS AND NOTIFICATIONS - Badge Style
           ============================================================ */
        
        /* Base alert styling with glassy effect */
        [data-testid="stAlert"],
        [role="alert"],
        .stAlert,
        [data-testid="stNotification"] {{
            background: linear-gradient(180deg, 
                rgba(255, 255, 255, 0.08) 0%, 
                transparent 100%), 
                {colors['bg_tertiary']} !important;
            color: {colors['text_primary']} !important;
            border: 1px solid {colors['border']} !important;
            border-radius: 8px !important;
            box-shadow: {colors['shadow_raised']},
                        inset 0 1px 0 {colors['highlight_top']} !important;
            backdrop-filter: blur(4px);
        }}
        
        /* Success alert */
        [data-testid="stAlert"][data-baseweb*="positive"],
        .element-container:has(.stSuccess) [data-testid="stAlert"] {{
            background: linear-gradient(180deg, 
                rgba(34, 197, 94, 0.1) 0%, 
                {colors['success_bg']} 100%) !important;
            border-color: rgba(34, 197, 94, 0.5) !important;
            box-shadow: 0 0 12px rgba(34, 197, 94, 0.2),
                        {colors['shadow_raised']} !important;
        }}
        
        /* Error alert */
        [data-testid="stAlert"][data-baseweb*="negative"],
        .element-container:has(.stError) [data-testid="stAlert"] {{
            background: linear-gradient(180deg, 
                rgba(239, 68, 68, 0.1) 0%, 
                {colors['error_bg']} 100%) !important;
            border-color: rgba(239, 68, 68, 0.5) !important;
            box-shadow: 0 0 12px rgba(239, 68, 68, 0.2),
                        {colors['shadow_raised']} !important;
        }}
        
        /* Warning alert */
        [data-testid="stAlert"][data-baseweb*="warning"],
        .element-container:has(.stWarning) [data-testid="stAlert"] {{
            background: linear-gradient(180deg, 
                rgba(234, 179, 8, 0.1) 0%, 
                {colors['warning_bg']} 100%) !important;
            border-color: rgba(234, 179, 8, 0.5) !important;
            box-shadow: 0 0 12px rgba(234, 179, 8, 0.2),
                        {colors['shadow_raised']} !important;
        }}
        
        /* Info alert */
        [data-testid="stAlert"][data-baseweb*="info"],
        .element-container:has(.stInfo) [data-testid="stAlert"] {{
            background: linear-gradient(180deg, 
                rgba(59, 130, 246, 0.1) 0%, 
                {colors['info_bg']} 100%) !important;
            border-color: rgba(59, 130, 246, 0.5) !important;
            box-shadow: 0 0 12px rgba(59, 130, 246, 0.2),
                        {colors['shadow_raised']} !important;
        }}
        
        /* ============================================================
           TYPOGRAPHY
           ============================================================ */
        
        h1, h2, h3, h4, h5, h6 {{
            color: {colors['text_primary']} !important;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        }}
        
        /* Main title - embossed effect */
        h1 {{
            letter-spacing: -0.02em !important;
        }}
        
        p, span, li, label {{
            color: {colors['text_primary']} !important;
        }}
        
        .stMarkdown, .stMarkdown p {{
            color: {colors['text_primary']} !important;
        }}
        
        /* Secondary text */
        .stCaption, small, .text-secondary {{
            color: {colors['text_secondary']} !important;
        }}
        
        /* Code blocks - terminal style */
        code, pre {{
            background: linear-gradient(180deg, 
                rgba(0, 0, 0, 0.2) 0%, 
                transparent 100%), 
                {colors['bg_tertiary']} !important;
            color: {colors['text_primary']} !important;
            padding: 3px 8px !important;
            border-radius: 6px !important;
            border: 1px solid {colors['border']} !important;
            box-shadow: {colors['shadow_inset']} !important;
            font-family: 'SF Mono', 'Fira Code', 'Monaco', monospace !important;
        }}
        
        /* Links */
        a {{
            color: {colors['accent']} !important;
            text-decoration: none !important;
            transition: all 0.15s ease !important;
        }}
        
        a:hover {{
            color: {colors['accent_light']} !important;
            text-shadow: 0 0 8px rgba(59, 130, 246, 0.4) !important;
        }}
        
        /* ============================================================
           HORIZONTAL RULES AND DIVIDERS
           ============================================================ */
        
        hr {{
            border: none !important;
            height: 1px !important;
            background: linear-gradient(90deg, 
                transparent 0%, 
                {colors['border']} 20%, 
                {colors['border']} 80%, 
                transparent 100%) !important;
            box-shadow: 0 1px 0 {colors['highlight_top']} !important;
        }}
        
        /* Column dividers */
        [data-testid="column"] {{
            background-color: transparent !important;
        }}
        
        /* ============================================================
           SCROLLBARS - Sleek Style
           ============================================================ */
        
        ::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {colors['bg_primary']};
            border-radius: 5px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(180deg, 
                {colors['bg_elevated']} 0%, 
                {colors['bg_tertiary']} 100%);
            border-radius: 5px;
            border: 2px solid {colors['bg_primary']};
            box-shadow: inset 0 1px 0 {colors['highlight_top']};
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(180deg, 
                {colors['border_light']} 0%, 
                {colors['border']} 100%);
        }}
        
        /* ============================================================
           SPINNER/LOADING - Glowing Effect
           ============================================================ */
        
        .stSpinner > div {{
            border-color: {colors['accent']} transparent transparent transparent !important;
            filter: drop-shadow(0 0 4px {colors['accent']}) !important;
        }}
        
        /* ============================================================
           TOOLTIP AND HELP
           ============================================================ */
        
        [data-testid="stTooltipIcon"] {{
            color: {colors['text_secondary']} !important;
            transition: all 0.15s ease !important;
        }}
        
        [data-testid="stTooltipIcon"]:hover {{
            color: {colors['accent']} !important;
            filter: drop-shadow(0 0 4px {colors['accent']}) !important;
        }}
        
        /* ============================================================
           SUBTLE ANIMATIONS
           ============================================================ */
        
        @keyframes subtle-pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.85; }}
        }}
        
        /* Processing indicator pulse */
        .stSpinner {{
            animation: subtle-pulse 1.5s ease-in-out infinite;
        }}
        
        </style>
        """
    
    @staticmethod
    def render_theme_selector():
        """Render theme selector in sidebar and apply CSS."""
        # Initialize theme state
        if 'theme_mode' not in st.session_state:
            st.session_state.theme_mode = 'dark'
        
        # Theme selector in sidebar
        st.sidebar.markdown("---")
        theme_mode = st.sidebar.radio(
            "Theme",
            options=['dark', 'light'],
            index=0 if st.session_state.theme_mode == 'dark' else 1,
            key='theme_selector',
            horizontal=True
        )
        
        # Update state if changed
        if theme_mode != st.session_state.theme_mode:
            st.session_state.theme_mode = theme_mode
            st.rerun()
        
        # Inject CSS
        css = ThemeManager.get_css(st.session_state.theme_mode)
        st.markdown(css, unsafe_allow_html=True)
