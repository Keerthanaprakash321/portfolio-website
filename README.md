# Personal Portfolio Website

[Live Demo]: https://portfolio-website-tn3f-6iwjmjuin-keerthanaprakash321s-projects.vercel.app/#home <!-- Replace with your actual live demo link -->

## Overview
A full-stack, production-ready personal portfolio website built with Django. It is designed to showcase projects, share blog posts, and provide a contact interface, all while exposing RESTful API endpoints. The project is fully configured for deployment on Vercel with a PostgreSQL database (Neon) and uses Tailwind CSS for modern, responsive styling.

## Features
- **Projects Showcase**: Display and manage portfolio projects (`projects_app`).
- **Personal Blog**: Create and publish blog articles (`blog_app`).
- **Contact Form**: Allow visitors to send messages securely (`contact_app`).
- **User Authentication**: Secure user login and registration (`accounts_app`).
- **RESTful API**: Access portfolio data via API endpoints (`api_app`).
- **Responsive Design**: Beautiful, mobile-friendly UI using Tailwind CSS.
- **Production-Ready**: Configured with WhiteNoise for static file serving and PostgreSQL for robust data management.

## Tech Stack
- **Backend**: Python, Django, Django REST Framework
- **Database**: PostgreSQL 
- **Frontend/Styling**: HTML5, Django Templates, Tailwind CSS
- **Deployment**: Vercel (Serverless), Gunicorn, Docker
- **Static File Management**: WhiteNoise

## Project Structure
```text
Portfolio/
├── accounts_app/      # User authentication and account management
├── api_app/           # Django REST Framework API endpoints
├── blog_app/          # Blog models, views, and templates
├── contact_app/       # Contact form handling and messaging
├── projects_app/      # Portfolio projects display
├── portfolio_site/    # Main Django project configuration settings
├── theme/             # Tailwind CSS configuration and styling
├── static/            # Static assets (CSS, JS, Images)
├── templates/         # Global HTML templates
└── build_files.sh     # Build script for Vercel deployment
```

## Author
**Keerthana Prakash**
- **GitHub**: [Keerthanaprakash321](https://github.com/Keerthanaprakash321)
- **Email**: keerthana76666@gmail.com <!-- Please update this with your actual email address -->
- **Phone**: +91 6238705946
