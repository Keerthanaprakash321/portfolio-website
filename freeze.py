import os
import shutil
import re

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio_site.settings")
import django
django.setup()

from django.conf import settings
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append('testserver')

from django.test import Client
client = Client()

BUILD_DIR = 'github_pages_build'
os.makedirs(os.path.join(BUILD_DIR, 'projects'), exist_ok=True)

urls_to_scrape = {
    '/': 'index.html',
    '/contact/': 'contact.html',
    '/resume/': 'resume.html',
    '/education/': 'education.html',
    '/certificates/': 'certificates.html',
}

try:
    from projects_app.models import Project
    for p in Project.objects.all():
        urls_to_scrape[f'/projects/{p.slug}/'] = f'projects/{p.slug}.html'
except Exception as e:
    print(f"No projects found or error loading models: {e}")

# Function to fix links in HTML
def fix_links(html, depth=0):
    prefix = '../' * depth
    # Change absolute links to relative for GitHub Pages compatibility
    html = re.sub(r'href="/contact/"', f'href="{prefix}contact.html"', html)
    html = re.sub(r'href="/resume/"', f'href="{prefix}resume.html"', html)
    html = re.sub(r'href="/education/"', f'href="{prefix}education.html"', html)
    html = re.sub(r'href="/certificates/"', f'href="{prefix}certificates.html"', html)
    html = re.sub(r'href="/projects/([^"/]+)/"', f'href="{prefix}projects/\\1.html"', html)
    html = re.sub(r'href="/"', f'href="{prefix}index.html"', html)
    html = re.sub(r'href="/#', f'href="{prefix}index.html#', html)
    
    html = html.replace('href="/static/', f'href="{prefix}static/')
    html = html.replace('src="/static/', f'src="{prefix}static/')
    html = html.replace('href="/media/', f'href="{prefix}media/')
    html = html.replace('src="/media/', f'src="{prefix}media/')
    
    # Replace contact form POST action
    html = re.sub(
        r'<form[^>]*method="post"[^>]*>', 
        '<form action="https://formsubmit.co/keerthana76666@gmail.com" method="POST">', 
        html, 
        flags=re.IGNORECASE
    )
    # Remove CSRF tags
    html = re.sub(r'<input type="hidden" name="csrfmiddlewaretoken"[^>]*>', '', html)
    # FormSubmit config inputs
    html = html.replace('</form>', '<input type="hidden" name="_captcha" value="false"></form>')
    return html

for url, filename in urls_to_scrape.items():
    res = client.get(url)
    if res.status_code == 200:
        html_content = res.content.decode('utf-8')
        depth = filename.count('/')
        fixed_html = fix_links(html_content, depth)
        
        filepath = os.path.join(BUILD_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_html)
        print(f"Created: {filepath}")
    else:
        print(f"Failed to scrape {url} (Status {res.status_code})")

if os.path.exists('static'):
    shutil.copytree('static', os.path.join(BUILD_DIR, 'static'), dirs_exist_ok=True)
if os.path.exists('media'):
    shutil.copytree('media', os.path.join(BUILD_DIR, 'media'), dirs_exist_ok=True)

print("Static freeze complete!")
