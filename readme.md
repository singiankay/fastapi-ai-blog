# FastAPI AI Generated Blog

This is a FastAPI application that provides a CRUD (Create, Read, Update, Delete) functionality for blog posts. Each post contains a title, content, and rating. The content of the post can be generated using OpenAI. The rating can be manually assigned or generated using AI from a scale of 1 to 10. The application uses PostgreSQL as the database to store the blog posts.

## Prerequisites

- Python 3.9 or above
- PostgreSQL database
- OpenAI API key

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/singiankay/fastapi-ai-blog.git
   ```

2. Change into the project directory:

   ```bash
   cd fastapi-ai-blog
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The application requires configuration for the database and OpenAI API key. Create a `.env` file in the root directory of the project and add the following configuration variables:

```
OPENAI_API_KEY=your-api-key
DATABASE_URL=127.0.0.1
DATABASE_PORT=5432
DATABASE_USER=your-postgres-user
DATABASE_PASSWORD=your-postgres-password
DATABASE_NAME=fastapi
```


## Database Setup

1. Create a PostgreSQL database.


## Running the Application

Start the FastAPI application with the following command:

```bash
python main.py
```

The application will be accessible at `http://127.0.0.1:8000`.

## Docs

Swagger API documentation is available at http://127.0.0.1:8000/docs


## AI-Generated Content

To generate AI-generated content for a new post, send a `POST` request to the `/posts/` endpoint with the `generate_content` parameter to True


## AI-Generated Rating

To generate an AI-generated rating for a post, send a `PUT` request to the `/posts/{post_id}/rating` endpoint with the `generate_rating` parameter to True



## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.