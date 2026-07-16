# KALF Website

A Flask-based public website for the Kick Against Laxity Foundation (KALF), a youth-focused NGO in Makurdi, Nigeria. The project showcases the foundation’s mission, programs, blog content, contact options, and donation flow.

## Overview

This website is designed to help KALF present its work in a clear and professional way. It combines static page templates with JSON-driven content so pages can be updated without changing the application code.

## Features

- Responsive landing page with hero content, impact highlights, and program previews
- About page with the organization’s story, vision, and mission
- Programs page that displays program categories, events, and details
- Blog section with published posts and individual post pages
- Contact and donation pages with a simple user flow
- Data-driven content loaded from JSON files in the static data folder

## Tech Stack

- Python 3
- Flask
- Jinja2 templates
- Tailwind CSS via CDN
- JSON-based content management for programs and blog posts

## Project Structure

```text
kalf/
├── app.py
├── config.py
├── requirements.txt
├── routes/
│   ├── admin.py
│   ├── blog.py
│   ├── main.py
│   └── programs.py
├── services/
│   ├── json_service.py
│   ├── paystack.py
│   └── program_service.py
├── static/
│   ├── css/
│   ├── data/
│   ├── images/
│   └── js/
└── templates/
    ├── partials/
    └── *.html
```

## Getting Started

1. Clone the repository
   ```bash
   git clone <repo-url>
   cd kalf
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   pip install Flask-Cors requests
   ```

4. Run the application
   ```bash
   python app.py
   ```

5. Open the site in your browser
   ```text
   http://localhost:5000
   ```

## Configuration

The application uses environment variables where available. The main ones are:

- FLASK_SECRET_KEY
- PAYSTACK_SECRET_KEY

If these are not set, the app will fall back to default values defined in config.py.

## Content Management

Most website content is stored in JSON files under the static/data directory, including:

- blog.json
- programs.json
- events.json

This makes it easier to update site content without changing templates or Python code.

## License

This project is maintained for the Kick Against Laxity Foundation. All rights reserved unless otherwise stated by the organization.