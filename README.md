# Back-End-Development-Songs

A Flask + PyMongo microservice for managing songs stored in MongoDB.

## Tech Stack

- Python
- Flask
- PyMongo
- MongoDB
- Gunicorn
- Docker

## API Endpoints

| Method | Path | Description | Success status |
| --- | --- | --- | --- |
| GET | `/health` | Check service health | 200 |
| GET | `/count` | Get the number of songs | 200 |
| GET | `/song` | List all songs | 200 |
| GET | `/song/<id>` | Get a song by ID | 200 (404 if not found) |
| POST | `/song` | Create a song | 201 (302 if ID exists) |
| PUT | `/song/<id>` | Update a song | 200 (404 if not found) |
| DELETE | `/song/<id>` | Delete a song | 204 (404 if not found) |

## Environment Variables

Configure the MongoDB connection with these environment variables:

| Variable | Description |
| --- | --- |
| `MONGODB_URI` | MongoDB connection string (default `mongodb://localhost:27017`) |
| `MONGODB_DATABASE` | Database name (default `songs`) |

## Run Locally

Install the dependencies and start the Flask development server:

```bash
pip install -r requirements.txt
flask --app songs run --debug
```

The service seeds the MongoDB `songs` collection from `songs/songs.json` when a data endpoint is first used. Seed documents are inserted only when their integer IDs are not already present.

## cURL Examples

Check service health:

```bash
curl -i http://localhost:5000/health
```

Get the number of songs:

```bash
curl -i http://localhost:5000/count
```

List all songs:

```bash
curl -i http://localhost:5000/song
```

Get a song by ID:

```bash
curl -i http://localhost:5000/song/1
```

Create a song:

```bash
curl -i -X POST http://localhost:5000/song \
	-H 'Content-Type: application/json' \
	-d '{"id":11,"title":"Northern Lights","lyrics":"A new song begins"}'
```

Update a song by ID:

```bash
curl -i -X PUT http://localhost:5000/song/1 \
	-H 'Content-Type: application/json' \
	-d '{"id":1,"title":"Morning Window Updated","lyrics":"Updated lyrics"}'
```

Delete a song by ID:

```bash
curl -i -X DELETE http://localhost:5000/song/1
```

## Docker

Build the image and run the container with port `8080` exposed:

```bash
docker build -t songs .
docker run -p 8080:8080 songs
```

## Project structure

```text
.
├── songs/
│   ├── __init__.py
│   ├── routes.py
│   └── songs.json
├── requirements.txt
└── README.md
```