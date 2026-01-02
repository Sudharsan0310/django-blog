🚀 Django Blog - Full-Stack Web Application


Live Demo: https://django-blog-k3hz.onrender.com | Duration: 1 week.


A production-ready blogging platform featuring authentication, CRUD operations, and real-time commenting. Built with Django and PostgreSQL.

🎯 Key Features

- User Authentication - Secure registration, login, and session management

- CRUD Operations - Complete blog post management system

- Comment System - Real-time commenting with user permissions

- Search & Filter - Advanced search and category-based filtering

- Admin Dashboard - Role-based content management (Admin, Staff, User)

- Responsive Design - Mobile-first UI with Bootstrap 4

- Auto-Deploy - CI/CD pipeline with GitHub integration

- Production-Ready - Deployed on Render with PostgreSQL databa

🛠️ Tech Stack

Backend: Python, Django 5.1.4, Django ORM

Database: PostgreSQL 16 (render)

Frontend: HTML5, CSS3, Bootstrap 4, Light JavaScript

Deployment: Render (Web + Database), WhiteNoise, Gunicorn

Tools: Git, GitHub, VS Code

⚡ Quick Start
# Clone repository
git clone https://github.com/Sudharsan0310/django-blog.git
cd django-blog

# Create virtual environment
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run development server
python manage.py runserver

Visit: http://127.0.0.1:8000/

🏗️ Architecture

- MVT Pattern: Models → Views → Templates

- ORM: Django ORM for database abstraction

- Security: CSRF, XSS protection, secure sessions

🔮 Planned Enhancements

 - REST API with Django REST Framework
 
 - Email notifications (Celery + Redis)
 
 - Rich text editor (TinyMCE/CKEditor)
 
 - Like/Dislike system
 
 - User profile pages
 
 - Social media sharing
 
 - Pagination
 
 - Unit tests (pytest)

 📊 Project Stats

- Lines of Code: ~2,500

- Development Time: 1 week

- Models: 4 (User, Category, Blog, Comment)

- Views: 15+

- Templates: 12+

- Test Coverage: Manual testing completed

🎓 Key Learnings
- Django MVT architecture and best practices
- Database relationships and ORM optimization
- Production deployment and configuration
- Security implementation (CSRF, XSS, SQL injection prevention)
- Responsive design patterns-✅ Git workflow and version control

👨‍💻 About
- Name : Sudharsan J S
- Linkedin : https://www.linkedin.com/in/sudharsanjs
- Email : jssudharsan7@gmail.com
- Looking For : Backend Developer Roles | Python & Django Developer Roles | Full-Stack Developer Roles.

Show Your Support
If you found this project helpful, please give it a star! 
