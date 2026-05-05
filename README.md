# Employee API — Python / FastAPI

REST API de gestion d'employés bâtie avec **FastAPI**, **SQLAlchemy 2.0** et **Pydantic v2**. Pensé comme support pédagogique pour développeurs Python.

## Tech stack

| Couche        | Technologie                          |
|---------------|--------------------------------------|
| Langage       | Python 3.14                          |
| Framework web | FastAPI                              |
| Validation    | Pydantic v2                          |
| ORM           | SQLAlchemy 2.0                       |
| Migrations    | Alembic                              |
| Base de données | SQLite (local), MySQL (prod)       |
| Tests         | pytest + httpx (`TestClient`)        |
| Lint          | ruff                                 |

## Prérequis

- **Python 3.14**
- pip (livré avec le module standard `venv`)
- MySQL (uniquement pour le profil `prod`)

## Installation

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Lancer en local (SQLite)

```bash
# APP_ENV=local par défaut → SQLite, schéma créé automatiquement au démarrage
uvicorn app.main:app --reload --port 8085
```

L'API est dispo sur http://localhost:8085, et la doc OpenAPI auto-générée sur http://localhost:8085/docs.

## Lancer contre MySQL

```bash
export APP_ENV=prod
export DATABASE_URL="mysql+pymysql://user:password@localhost:3306/otel_employee_db"

# 1) Appliquer les migrations Alembic
alembic upgrade head

# 2) Démarrer le serveur
uvicorn app.main:app --port 8085
```

En profil `prod`, le schéma n'est **pas** créé automatiquement : Alembic est la seule source de vérité.

## Tests

```bash
pytest                         # tous les tests
pytest tests/test_employee_api.py::test_create_employee_returns_201
pytest -k duplicate            # filtrer par mot-clé
```

Les tests utilisent SQLite en mémoire via une fixture `db_session`, et `FastAPI.dependency_overrides` pour injecter cette session dans le `TestClient`.

## Structure du projet

```
.
├── requirements.txt
├── pytest.ini
├── alembic.ini
├── alembic/
│   ├── env.py
│   └── versions/                      # 001_create_employee_table, 002_insert_sample_employees
├── app/
│   ├── main.py                        # entrée FastAPI (lifespan, routers, handlers)
│   ├── core/
│   │   ├── config.py                  # Pydantic Settings (APP_ENV, DATABASE_URL)
│   │   └── database.py                # engine SQLAlchemy + Session + Base déclarative
│   ├── models/
│   │   ├── department.py              # Enum Department
│   │   └── employee.py                # ORM SQLAlchemy → table t_employee
│   ├── schemas/
│   │   ├── employee.py                # EmployeeRequest, EmployeeResponse (Pydantic)
│   │   └── pagination.py              # PaginatedResponse[T]
│   ├── repositories/
│   │   └── employee_repository.py
│   ├── services/
│   │   └── employee_service.py        # logique métier + commit/refresh
│   ├── api/
│   │   └── employees.py               # APIRouter /api/employees
│   └── exceptions/
│       ├── domain.py                  # EmployeeNotFoundException, DuplicateEmailException
│       └── handlers.py                # → ProblemDetail RFC 7807
└── tests/
    ├── conftest.py                    # fixtures db_session + client
    ├── test_employee_api.py
    └── test_employee_service.py
```

## Endpoints

Base path : `/api/employees`

| Méthode | Chemin                | Description                  |
|---------|-----------------------|------------------------------|
| POST    | `/`                   | Créer un employé             |
| GET     | `/{id}`               | Récupérer par ID             |
| GET     | `/`                   | Liste paginée                |
| PUT     | `/{id}`               | Mise à jour                  |
| DELETE  | `/{id}`               | Suppression                  |

### Paramètres de pagination (`GET /`)

| Paramètre  | Défaut       | Description                        |
|------------|--------------|------------------------------------|
| `page`     | `0`          | Numéro de page (0-based)           |
| `size`     | `10`         | Taille de page (1–100)             |
| `sortBy`   | `created_at` | Champ de tri                       |
| `direction`| `asc`        | Direction (`asc` ou `desc`)        |

### Champs Employee

| Champ        | Type       | Contraintes                    |
|--------------|------------|--------------------------------|
| first_name   | str        | Requis                         |
| last_name    | str        | Requis                         |
| email        | EmailStr   | Requis, email valide, unique   |
| phone_number | str        | Requis                         |
| department   | Department | Requis (voir enum ci-dessous)  |

**Department** : `HR`, `IT`, `FINANCE`, `OPERATIONS`, `MARKETING`, `LEGAL`

## Format des erreurs (RFC 7807)

Toutes les erreurs sont renvoyées en `application/problem+json` :

```json
{
  "type": "about:blank",
  "title": "Not Found",
  "status": 404,
  "detail": "Employee not found with id: 9999"
}
```

Les erreurs de validation incluent un champ `errors` listant les champs invalides :

```json
{
  "type": "about:blank",
  "title": "Bad Request",
  "status": 400,
  "detail": "Validation failed",
  "errors": { "email": "value is not a valid email address" }
}
```

## Migrations Alembic

Les migrations vivent dans `alembic/versions/` :

| Révision | Description                |
|----------|----------------------------|
| 001      | Crée la table `t_employee` |
| 002      | Insère des employés sample |

Commandes utiles :

```bash
alembic upgrade head           # appliquer toutes les migrations
alembic downgrade -1           # rollback d'une migration
alembic revision -m "ma mig"   # créer une nouvelle migration vide
alembic history                # lister les révisions
```

## Health check

```bash
curl http://localhost:8085/actuator/health
# {"status":"UP"}
```
