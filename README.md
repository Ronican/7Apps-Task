# PDF Chat API

This project is a FastAPI application that allows users to upload PDF documents and interact with them through a chat interface powered by Gemini AI. The application processes PDFs, indexes their content, and enables users to ask questions or have conversations based on the content of the uploaded PDFs.

## Table of Contents
- [PDF Chat API](#pdf-chat-api)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
    - [Running the Application](#running-the-application)
    - [API Endpoints](#api-endpoints)
      - [Upload PDF](#upload-pdf)
      - [Chat with PDF](#chat-with-pdf)
    - [Examples](#examples)
      - [Uploading a PDF](#uploading-a-pdf)
      - [Chatting with the Uploaded PDF](#chatting-with-the-uploaded-pdf)
  - [Testing](#testing)
    - [Running Tests](#running-tests)
    - [Test Coverage](#test-coverage)
  - [Dependencies](#dependencies)
  - [User Guide](#user-guide)
    - [Introduction](#introduction)
    - [Getting Started](#getting-started)
    - [Using the API](#using-the-api)
      - [Uploading a PDF](#uploading-a-pdf-1)
      - [Chatting with the PDF](#chatting-with-the-pdf)
    - [Best Practices](#best-practices)
    - [Troubleshooting](#troubleshooting)

## Features
- **PDF Upload**: Upload PDF documents to the server for processing.
- **Content Extraction**: Extract text content from PDFs and store it in a database.
- **Indexing**: Build an index of the PDF content using embeddings for efficient search.
- **Chat Interface**: Interact with the uploaded PDFs through a chat interface.
- **AI-Powered Responses**: Generate responses using the Gemini AI API based on the content of the PDFs.

## Prerequisites
- Python 3.8 or higher
- PostgreSQL: A PostgreSQL database for storing PDF metadata and content.
- Gemini API Key: An API key for the Gemini AI service.

## Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/Ronican/7Apps-Task.git
   cd 7Apps-BackEnd-Task
   ```

2. **Create a Virtual Environment**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Additional System Dependencies**
   - For PDF processing, you may need to install `poppler-utils` or `xpdf`.
   - On Ubuntu/Debian:
     ```bash
     sudo apt-get install poppler-utils
     ```
   - On macOS (using Homebrew):
     ```bash
     brew install poppler
     ```

## Configuration

1. **Set Environment Variables**
   - Create a `.env` file in the project root directory and add the following variables:
     ```env
        APP_NAME=PDFChatAPI
        APP_VERSION=1.0.0
    
        # Database Configuration
        DB_HOST=
        DB_PORT=
        DB_NAME=
        DB_USER=
        DB_PASSWORD=
    
        # Redis Configuration
        REDIS_HOST=
        REDIS_PORT=
        REDIS_DB=
    
        GEMINI_API_KEY=
        SECRET_KEY=
        ACCESS_TOKEN_EXPIRE_MINUTES=
        SENTRY_DSN=

     ```
    

2. **Initialize the Database**
   - Create the database in PostgreSQL:
     ```sql
     CREATE DATABASE pdf_chat_db;
     ```
   - Run database migrations.

3. **Load Environment Variables**
   - Ensure that your application loads the environment variables. Add the following to your `app/main.py` if not already included:
     ```python
     from dotenv import load_dotenv
     load_dotenv()
     ```

## Usage

### Running the Application
Start the FastAPI application using Uvicorn:
```bash
uvicorn app.main:app --reload
```
- The application will be accessible at [http://localhost:8000](http://localhost:8000).
- The interactive API documentation will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

### API Endpoints

#### Upload PDF
- **Endpoint**: `POST /v1/pdf`
- **Description**: Upload a PDF file to the server for processing.
- **Parameters**:
  - `file`: The PDF file to upload (multipart/form-data).
- **Response**:
  - `201 Created` on success.
  - JSON body containing:
    - `detail`: Message indicating success.
    - `pdf_id`: The unique identifier of the uploaded PDF.

**Example Request** (Using curl):
```bash
curl -X POST "http://localhost:8000/v1/pdf" \
     -F "file=@/path/to/your/document.pdf"
```

#### Chat with PDF
- **Endpoint**: `POST /v1/chat/{pdf_id}`
- **Description**: Interact with the uploaded PDF by sending messages and receiving AI-generated responses based on the PDF content.
- **Parameters**:
  - `pdf_id`: The unique identifier of the PDF (path parameter).
  - `message`: The user's message or question (JSON body).
- **Response**:
  - `200 OK` on success.
  - JSON body containing:
    - `response`: The AI-generated response.

**Example Request** (Using curl):
```bash
curl -X POST "http://localhost:8000/v1/chat/{pdf_id}" \
     -H "Content-Type: application/json" \
     -d '{"message": "Can you summarize the main points of the document?"}'
```

### Examples

#### Uploading a PDF
1. **Using Swagger UI**:
   - Navigate to [http://localhost:8000/docs](http://localhost:8000/docs).
   - Expand the `POST /v1/pdf` endpoint.
   - Click on "Try it out" and upload a PDF file.
   - Click "Execute" and note the `pdf_id` returned in the response.

2. **Using curl**:
   ```bash
   curl -X POST "http://localhost:8000/v1/pdf" \
        -F "file=@/path/to/your/document.pdf"
   ```

#### Chatting with the Uploaded PDF
1. **Using Swagger UI**:
   - Navigate to [http://localhost:8000/docs](http://localhost:8000/docs).
   - Expand the `POST /v1/chat/{pdf_id}` endpoint.
   - Click on "Try it out" and enter the `pdf_id` you received from the upload step.
   - In the request body, enter your message:
     ```json
     {
       "message": "What are the key findings of the document?"
     }
     ```
   - Click "Execute" to view the AI-generated response.

## Testing

### Running Tests
Ensure that you have `pytest` and other testing dependencies installed:
```bash
pip install -r requirements-dev.txt
```
Run the tests using:
```bash
pytest tests/
```

### Test Coverage
To generate a test coverage report:
```bash
pytest --cov=app tests/
```




## Dependencies
- **FastAPI**: Web framework for building APIs.
- **Uvicorn**: ASGI server for running FastAPI applications.
- **SQLAlchemy**: ORM for database interactions.
- **AsyncPG**: PostgreSQL driver for asynchronous operations.
- **LangChain**: Library for language model applications.
- **HuggingFace Transformers**: For embeddings and language models.
- **Gemini AI API**: For generating AI-powered responses.
- **aiohttp**: Asynchronous HTTP client/server framework.
- **pypdf** : For extracting text from PDFs.

Install all dependencies using:
```bash
pip install -r requirements.txt
```



## User Guide

### Introduction
The PDF Chat API allows users to interact with PDF documents through a conversational interface. By uploading a PDF, the content is processed and indexed, enabling users to ask questions or request summaries based on the document's content.

### Getting Started
1. **Set Up the Environment**
   - Ensure all prerequisites are met.
   - Install dependencies and configure the application as described in the [Installation](#installation) and [Configuration](#configuration) sections.

2. **Run the Application**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Access the API Documentation**
   - Open a web browser and navigate to [http://localhost:8000/docs](http://localhost:8000/docs) to access the interactive Swagger UI.

### Using the API

#### Uploading a PDF
- Navigate to the `/v1/pdf` endpoint in Swagger UI.
- Click "Try it out" and upload a PDF file.
- Click "Execute" to send the request.
- On success, you'll receive a `pdf_id` in the response.

**Important**: Keep the `pdf_id` safe; you'll need it to interact with the uploaded PDF.

#### Chatting with the PDF
- Navigate to the `/v1/chat/{pdf_id}` endpoint.
- Click "Try it out".
- Enter the `pdf_id` you received from the upload step.
- In the request body, enter your message in JSON format:
  ```json
  {
    "message": "Your question or message here."
  }
  ```
- Click "Execute" to send the request and receive an AI-generated reply.

### Best Practices
- **File Size and Type**: Ensure that the PDFs you upload are not excessively large and are valid PDF documents.
- **Message Clarity**: Provide clear and concise messages to receive the most accurate responses.
- **Security**: Do not share your `pdf_id` with unauthorized users.

### Troubleshooting
- **500 Internal Server Error**: Check the application logs for detailed error messages. Common issues include missing environment variables, database connectivity problems, or invalid API keys.
- **No Response from Chat Endpoint**: Ensure that the `pdf_id` is correct and that the PDF was successfully processed.
- **Deprecation Warnings**: Update your dependencies to the latest versions and adjust your code according to any deprecation notices.

