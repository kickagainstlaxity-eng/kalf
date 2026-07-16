tailwind.config = {
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        // --- PRIMARY (Now Deep Navy) ---
        primary: "#0f142a",
        "on-primary": "#ffffff",
        "primary-container": "#1c223a",
        "on-primary-container": "#f2f2f2",
        "primary-fixed": "#dce1ff",
        "primary-fixed-dim": "#b1c5ff",
        "on-primary-fixed": "#00154e",
        "on-primary-fixed-variant": "#2e4377",
        "inverse-primary": "#b1c5ff",

        // --- SECONDARY (Your New Orange) ---
        secondary: "#f6921e",
        "on-secondary": "#ffffff",
        "secondary-container": "#ffdbc0",
        "on-secondary-container": "#331200",
        "secondary-fixed": "#ffdbc0",
        "secondary-fixed-dim": "#f6921e",
        "on-secondary-fixed": "#331200",
        "on-secondary-fixed-variant": "#662600",

        // --- TERTIARY / ACCENT (Now Off-White) ---
        tertiary: "#f2f2f2",
        "on-tertiary": "#0f142a", // Dark text on light accent
        "tertiary-container": "#ffffff",
        "on-tertiary-container": "#1a1c1c",
        "tertiary-fixed": "#e2e2e2",
        "tertiary-fixed-dim": "#c4c7c7",
        "on-tertiary-fixed": "#1a1c1c",
        "on-tertiary-fixed-variant": "#444748",

        // --- NEUTRALS & SURFACE ---
        "background": "#f9f9f9",
        "on-background": "#0f142a",
        "surface": "#f9f9f9",
        "on-surface": "#0f142a",
        "surface-variant": "#e2e2e2",
        "on-surface-variant": "#444748",
        "surface-dim": "#dadada",
        "surface-bright": "#f9f9f9",
        "surface-container-lowest": "#ffffff",
        "surface-container-low": "#f3f3f3",
        "surface-container": "#eeeeee",
        "surface-container-high": "#e8e8e8",
        "surface-container-highest": "#e2e2e2",
        "surface-tint": "#0f142a",
        "inverse-surface": "#2f3131",
        "inverse-on-surface": "#f1f1f1",
        "outline": "#747878",
        "outline-variant": "#c4c7c7",

        // --- ERROR ---
        "error": "#ba1a1a",
        "on-error": "#ffffff",
        "error-container": "#ffdad6",
        "on-error-container": "#93000a",
      },
      fontFamily: {
        headline: ["Noto Serif"],
        body: ["Inter"],
        label: ["Inter"],
      },
      borderRadius: {
        DEFAULT: "0.25rem",
        lg: "0.5rem",
        xl: "0.75rem",
        full: "9999px",
      },
      animation: {
        'spin-slow': 'spin 6s linear infinite',
      },
    },
  },
};
