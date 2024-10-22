# BlogIt - (Django Blog Application)

This is a Django-based blog application that allows users to read posts. Users can also comment on posts, bookmark their favorite posts, like posts, and subscribe to the blog for updates.

## Features

- User Authentication and Registration
- Create, Read, Update, Delete (CRUD) Posts involves admin panel.
- Add Comments to Posts
- Bookmark and Like Posts
- View Posts by Tags and Authors
- Search Posts
- Subscribe to Blog Updates
- View and Manage Bookmarked and Liked Posts

## Installation

### Running with Docker

1. **Pull the Docker image:**
    ```sh
    docker pull sakibmondal7/blog-it
    ```

2. **Run the Docker container:**
    ```sh
    docker run -d \
      --name blog-it \
      -e PIPELINE=local \
      -p 8000:8000 \
      sakibmondal7/blog-it
    ```

3. **Open your web browser and go to:**
    ```sh
    http://127.0.0.1:8000/
    ```

### Local Development (Optional)

If you prefer to run the application locally without Docker, follow these steps:

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/django-blog-app.git
    cd django-blog-app
    ```

2. **Create a virtual environment and activate it:**
    ```sh
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Apply the migrations:**
    ```sh
    python manage.py migrate
    ```

5. **Create a superuser:**
    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server:**
    ```sh
    python manage.py runserver
    ```

7. **Open your web browser and go to:**
    ```sh
    http://127.0.0.1:8000/
    ```

    ```

## Project Structure

- **Blogit/**: Contains the main application configuration.
  - `__init__.py`: Marks the directory as a Python package.
  - `asgi.py`: ASGI configuration for asynchronous support.
  - `settings.py`: Settings and configurations for the Django project.
  - `urls.py`: URL routing configuration for the project.
  - `wsgi.py`: WSGI configuration for web server support.

- **app/**: Contains the core functionality of the blog application.
  - `__init__.py`: Marks the directory as a Python package.
  - `admin.py`: Admin panel configuration.
  - `apps.py`: Application configuration.
  - `forms.py`: Form definitions for the application.
  - **migrations/**: Database migration files.
    - `0001_initial.py`: Initial migration file.
    - `__init__.py`: Marks the directory as a Python package.
  - `models.py`: Database models for the application.
  - **static/app/**: Static files for the application.
    - **images/**: Image files.
    - `style.css`: CSS stylesheet.
    - `url.js`: JavaScript file.
  - **templates/app/**: HTML templates for the application.
    - `about.html`: About page template.
    - `all_bookmark_post.html`: Template for displaying all bookmarked posts.
    - `all_liked_post.html`: Template for displaying all liked posts.
    - `all_post.html`: Template for displaying all posts.
    - `author.html`: Template for displaying posts by author.
    - `contact_us.html`: Contact us page template.
    - `index.html`: Index page template.
    - `post.html`: Template for displaying a single post.
    - `search.html`: Search results page template.
    - `tag.html`: Template for displaying posts by tag.
  - **templates/registration/**: Templates for user authentication.
    - `logged_out.html`: Template for logged out page.
    - `login.html`: Login page template.
    - `registration.html`: Registration page template.
  - `tests.py`: Test cases for the application.
  - `urls.py`: URL routing configuration for the application.
  - `views.py`: View functions for handling requests and rendering templates.

- `db.sqlite3`: SQLite database file.

- `manage.py`: Django management script.

- `requirements.txt`: List of dependencies for the project.

- **templates/**: Base templates for the project.
  - `layout.html`: Layout template used across the project.

## Views

### Post Views

- **post_page**: Displays a single post with comments and related information.
- **index**: Displays the index page with top, recent, and featured posts.
- **tag**: Displays posts by a specific tag.
- **author**: Displays posts by a specific author.
- **search_posts**: Allows searching for posts.
- **about**: Displays the about page.
- **contact_us**: Displays the contact us page.
- **register**: Handles user registration.
- **bookmark_post**: Allows users to bookmark a post.
- **all_bookmark_post**: Displays all bookmarked posts.
- **all_liked_post**: Displays all liked posts.
- **all_post**: Displays all posts.
- **like_post**: Allows users to like a post.

## Templates

Templates are located in the `templates/app` directory and include:
- **post.html**: Template for displaying a single post.
- **index.html**: Template for the index page.
- **tag.html**: Template for displaying posts by tag.
- **author.html**: Template for displaying posts by author.
- **search.html**: Template for displaying search results.
- **about.html**: Template for the about page.
- **contact_us.html**: Template for the contact us page.
- **registration.html**: Template for user registration.
- **all_bookmark_post.html**: Template for displaying all bookmarked posts.
- **all_liked_post.html**: Template for displaying all liked posts.
- **all_post.html**: Template for displaying all posts.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.


