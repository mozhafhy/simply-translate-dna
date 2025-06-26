# simply-translate-dna

Welcome to my mini project. This is a simple DNA/RNA transcription and translation 
API built using Flask.

## Features

- Transcribe DNA to RNA
- Translate RNA to sequence of amino acids
- Convert RNA to DNA
- Convert codon to amino acid

## Project Structure

```bash
.
│
├── flaskr/
│   ├── __init__.py         # Application factory (create_app)
│   ├── resource.py         # Blueprints: routes & error handlers
│   ├── middleware.py       # Middleware (request/response hooks)
│   └── response_type.py    # Response helpers/types
│
├── dna/
│   ├── dna_tools.py        # Business logic
│   ├── error_enum.py       # Error enums/types
│   ├── error_types.py      # Custom exception classes
│   └── result_types.py     # Result types for business logic
│
├── dto/
│   └── request_dto.py      # Pydantic DTOs for request validation
│
├── .gitignore
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
└── run.py                  # To run the server using waitress
```

## Installation

1. Clone this repository:
   ```bash
   git clone <repo-url>
   ```
2. (Recommended) Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

1. Run the following command
   ```bash
   python run.py
   ```
2. The API will be available at `http://localhost:5000/`

Alternatively, you can run the server using this command:
```bash
waitress-serve --listen=*:5000 --call 'flaskr:create_app'
```

## API Endpoints

- `POST /api/transcribe` — Transcribe DNA to RNA
- `POST /api/translate` — Translate RNA to sequence of amino acids
- `POST /api/rna-to-dna` — Convert RNA to DNA
- `POST /api/codon-to-protein` — Convert codon to amino acid

Each endpoint expects a JSON payload as described in the `dto/` models.

## Notes
I recommend to use this for educational purposes only since it's not made for more advance biology.
