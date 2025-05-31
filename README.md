# Headless Digital Asset Management (DAM) API

A modern, multi-tenant, headless Digital Asset Management (DAM) system built with **FastAPI**, **MySQL**, and **Elasticsearch**.  
All functionality is exposed via a secure, scalable REST API—ready to power your apps, websites, and workflows.

---

## Features

- **Multi-tenancy:** Strict data isolation per tenant, enforced via JWT tokens.
- **Asset Management:** Upload, version, search, and transform images, videos, documents, and more.
- **Metadata & Tagging:** Flexible metadata schemas, tagging, and localization.
- **Search & Indexing:** Lightning-fast, full-text and faceted search via Elasticsearch.
- **Webhooks:** Real-time event notifications to external systems.
- **Role-based Access Control:** Secure endpoints with JWT authentication and roles.
- **Audit Logs & Reporting:** Track asset usage, API calls, and user actions.
- **Extensible:** Modular codebase, easy to add new file types, transformations, or integrations.

---

## Tech Stack

- **FastAPI** (Python 3.8+)
- **MySQL** (8+)
- **SQLAlchemy** (ORM)
- **Elasticsearch** (8+)
- **S3-compatible storage** (AWS S3, MinIO, etc.)
- **JWT authentication** (`python-jose`)
- **Pillow, pdf2image, ffmpeg-python** (for asset transformations)

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/dam-api.git
cd dam-api
```

### 2. Install Python Dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Start MySQL and Elasticsearch

You can use Docker Compose for local development:

```yaml
# docker-compose.yml (example)
version: '3.8'
services:
  mysql:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: dam_db
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.6.2
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
    volumes:
      - es_data:/usr/share/elasticsearch/data
volumes:
  mysql_data:
  es_data:
```

```bash
docker-compose up -d
```

### 4. Configure Environment

Edit `db.py` and `utils/es.py` to match your MySQL and Elasticsearch settings.

### 5. Initialize the Database

Tables are auto-created on first app startup.  
To create the first admin user, run:

```bash
python create_first_user.py
```

### 6. Run the API Server

```bash
uvicorn main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation.

---

## API Overview

- **Authentication:** `/auth/login`, `/auth/refresh`, `/auth/logout`
- **Users:** `/users/`
- **Assets:** `/assets/`
- **Metadata:** `/metadata/`
- **Tags:** `/tags/`
- **Search:** `/search/`
- **Webhooks:** `/webhooks/`
- **Reports:** `/reports/`
- **Audit:** `/audit/`
- **Transformations:** `/transform/image/{id}`, `/transform/pdf/{id}`, `/transform/video/{id}`

See [OpenAPI docs](http://localhost:8000/docs) for full details.

---

## Multi-Tenancy

- Every API token (JWT) includes a `tenant_id`.
- All data access is scoped to the tenant.
- No cross-tenant data leakage.

---

## Asset Search & Indexing

- Assets are indexed in Elasticsearch on create/update/delete.
- Search supports full-text, tags, mimetype, and pagination.
- Faceted search and advanced queries supported.

---

## Webhooks

- Register webhooks to receive real-time event notifications (e.g., asset uploaded, deleted).
- Secure with secrets and custom headers.

---

## Development Notes

- **Password hashing:** Uses bcrypt via `passlib`.
- **Asset storage:** Integrate with S3 or compatible storage for file uploads.
- **Transformations:** Images, PDFs, and videos can be transformed/thumbnails generated on the fly.
- **Audit logs:** All key actions are logged for compliance and reporting.

---

## Contributing

Pull requests and issues are welcome!  
Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

[MIT License](LICENSE)

---

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Elasticsearch](https://www.elastic.co/elasticsearch/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pillow](https://python-pillow.org/)
- [pdf2image](https://github.com/Belval/pdf2image)
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)

---

**Happy building!** 🚀

---

