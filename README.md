# RESTFUL-API-learning

This project is a Django REST Framework-based API for managing employees, students, blogs, and comments. It demonstrates CRUD operations, authentication, pagination, and more.

## Features
- Employee, Student, Blog, and Comment models
- CRUD API endpoints for all models
- CSRF protection disabled for API endpoints
- Custom pagination (page number and limit-offset)
- Search and filter support
- ViewSets and Routers for automatic URL generation
- SQLite database

## Setup Instructions

1. **Clone the repository**
	```bash
	git clone https://github.com/alysajad/RESTFUL-API-learning.git
	cd RESTFUL-API-learning
	```

2. **Create and activate a virtual environment**
	```bash
	python -m venv venv
	venv\Scripts\activate  # On Windows
	source venv/bin/activate  # On Linux/Mac
	```

3. **Install dependencies**
	```bash
	pip install -r requirements.txt
	```

4. **Apply migrations**
	```bash
	python manage.py migrate
	```

5. **Run the development server**
	```bash
	python manage.py runserver
	```

6. **Access the API**
	- Employees: `/api/v1/employees/`
	- Students: `/api/v1/students/`
	- Blogs: `/api/v1/blogs/`
	- Comments: `/api/v1/comments/`

## GitHub Push Process

1. Initialize git and make the first commit:
	```bash
	git init
	git add .
	git commit -m "Initial commit"
	```
2. Create a new repository on GitHub and add it as remote:
	```bash
	git remote add origin https://github.com/alysajad/RESTFUL-API-learning
	git branch -M main
	```
3. If the remote already has commits, pull and rebase:
	```bash
	git pull origin main --rebase
	```
4. Push your code:
	```bash
	git push -u origin main
	```

## Notes
- CSRF protection is disabled for API endpoints using a custom authentication class.
- Pagination is customizable per view.
- For any issues, check the Django and DRF documentation.

## License
MIT
