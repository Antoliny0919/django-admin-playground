<!-- ABOUT THE PROJECT -->

## django-admin-playground

This project provides an optimal environment for contributing to Django Admin.

![logo](image/readme_logo.png)

It provides the following features:

- Before/After Comparison Pages(Access the "/compare" path.)
- Various Admin Use Cases
- Initial Data for Testing
- Provides images for visual regression testing via screenshots (planned)
- Automated generation of admin images for the [Django Project documentation](https://www.djangoproject.com/) (planned)

## Table of Contents

- [Running](#running)
- [Contributing](#contributing)

### Running

1. Clone django repo
   ```sh
   git clone https://github.com/django/django.git
   ```

2. Clone this repo into the django folder
   ```sh
   cd django
   git clone https://github.com/Antoliny0919/django-admin-playground.git
   ```

> [!WARNING]
> If you cloned django-admin-playground into a different path within the django folder,
> you need to update the values in the following files:
> - [manage.py](https://github.com/Antoliny0919/django-admin-playground/blob/main/manage.py#L12)
> - [settings.py](https://github.com/Antoliny0919/django-admin-playground/blob/main/main/settings.py#L7)

3. Create your virtual environment

   ```sh
   python -m venv venv
   source venv/bin/activate
   ```

> [!NOTE]
>
> If a virtual environment already exists in the cloned Django folder,
> you can use that environment and skip this step without any issues.

4. Install requirements
   ```sh
   pip install -r requirements.txt
   ```

5. Run migrations
   ```sh
   python manage.py migrate
   ```

6. Add initial data
   ```sh
   python manage.py loaddata auth_fixture.json changelist_fixture.json form_fixture.json inline_fixture.json
   ```

> [!TIP]
> django-admin-playground provides a superuser by default.
>
> - Username: ``admin``
> - Password: ``admin``

7. Run server 🚀
   ```sh
   python manage.py runserver
   ```


### Contributing

- Add test cases.

   django-admin-playground welcomes values or settings that can create visual differences in the Django Admin.
   Please add a ModelAdmin or fixture with specific values that can create visual differences.
   (Refer to this [document](https://docs.djangoproject.com/en/5.2/ref/django-admin/#dumpdata) for instructions on how to add fixtures.)

- Keep Django Admin templates up-to-date.

   The [before_admin](https://github.com/Antoliny0919/django-admin-playground/tree/main/templates/before_admin) template folder must always stay up-to-date with the latest [Django Admin templates](https://github.com/django/django/tree/main/django/contrib/admin/templates/admin).
   If there are any changes in the Django Admin templates, the template files in the `before_admin` folder must be kept identical.
   If the Django Admin templates have been modified, please reflect those changes in the `before_admin` templates!

- Feature improvements

   django-admin-playground aims to create the optimal environment for contributing to Django Admin.
   If you have any ideas or items that could improve the contribution environment, don’t hesitate to create an Issue.

Finally, I would like to thank everyone who has contributed to Django and django-admin-playground ❤️
