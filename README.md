# VIRTU LEARN (Backend)
Virtu Learn Backend is a robust server-side component designed for the Learning Management System (LMS). It serves as the backbone for building a feature-rich online learning platform, offering a comprehensive solution for educators and learners alike.

Built with Django, Django Rest Framework, and PostgreSQL, Virtu Learn Backend provides a powerful set of APIs to facilitate seamless integration with frontend applications. These APIs enable functionalities such as user authentication, course management, quiz creation, study material distribution, and more.


## Key Features
* User Management: Effortlessly manage teacher and student accounts, profiles, and activities.
* Course Management: Create, update, and organize courses. Assign courses to teachers and students.
* Quiz Management: Develop quizzes, assign them to courses, and monitor student attempts and results.
* Study Material Distribution: Upload, organize, and deliver study materials tailored to each course.
* Notification System: Keep users informed with notifications for course updates, announcements, and other important events.
* API Documentation: Access comprehensive API documentation to understand and utilize available endpoints efficiently.


## Installation
To install and run Virtu Learn (Backend), follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/preciousimo/virtu-learn-backend.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Apply database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Start the server:
```bash
python manage.py runserver
```

## API Documentation
The Virtu Learn Backend project offers a RESTful API that follows the best practices of API design, with a clear separation of concerns between the API views, serializers, and models. The API documentation can be found in the [API documentation file](https://virtulearn-api.onrender.com/). You can use this documentation to explore the available endpoints, their inputs and outputs, and the expected behavior.


## Contributing
This project is designed to be scalable and can be used as a starting point for building a learning management system or as a learning resource for developers who want to learn how to build backend APIs for LMS. If you're interested in contributing to the project, feel free to fork it and submit pull requests. We welcome contributions of any kind, including bug fixes, new features, and documentation improvements.


## License
This project is licensed under the MIT License.


## Acknowledgements
* [Django Docs](https://docs.djangoproject.com/en/4.2/)
* [DRF Docs](https://www.django-rest-framework.org/)
