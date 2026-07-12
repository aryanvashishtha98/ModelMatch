# Database Design

## Database

ModelMatch uses **PostgreSQL** hosted on **Supabase**.

---

# Why PostgreSQL?

The project stores structured information that has clear relationships.

For every uploaded dataset we need to store:

- Dataset information
- Meta-features
- Recommendation history
- Model runs
- Hyperparameters
- Evaluation metrics

These entities naturally form relational tables.

---

# Why NOT MongoDB?

MongoDB works well for document-oriented applications.

However, ModelMatch requires:

- Foreign keys
- Joins
- Historical queries
- Ranking
- Aggregations
- Consistent relationships

PostgreSQL handles these efficiently.

---

# Why NOT a Vector Database?

A vector database stores embeddings.

ModelMatch does not compare text embeddings.

Instead, it compares structured numerical meta-features using K-Nearest Neighbors.

Therefore a relational database is a better fit.

---

# Database Tables

## datasets

Stores uploaded datasets and OpenML datasets.

Columns

- id
- name
- source
- meta_features
- created_at

---

## runs

Stores every verified model execution.

Columns

- id
- dataset_id
- model_name
- hyperparameters
- score
- metric_type
- created_at

---

## recommendations

Stores recommendation history.

Columns

- id
- dataset_id
- ranked_shortlist
- reasoning
- created_at

---

# Entity Relationship Diagram

```
datasets
    |
    | 1
    |
    |------< runs

datasets
    |
    | 1
    |
    |------< recommendations
```

Each dataset can have:

- many recommendations
- many tuning runs

---

# Why JSONB?

Some fields have flexible structure.

Examples:

Meta Features

```json
{
    "nr_inst":150,
    "nr_attr":4,
    "class_entropy":0.89
}
```

Hyperparameters

```json
{
    "max_depth":8,
    "n_estimators":200
}
```

Using JSONB allows PostgreSQL to store these efficiently while still supporting indexing and querying.

---

# Supabase Setup

### Step 1

Create a free Supabase project.

---

### Step 2

Open

SQL Editor

---

### Step 3

Paste

```
db/schema.sql
```

Execute.

---

### Step 4

Copy

Project URL

and

Anon Key

---

### Step 5

Create a `.env` file.

```env
SUPABASE_URL=your_project_url
SUPABASE_KEY=your_anon_key
DATABASE_URL=postgresql://postgres:password@host:5432/postgres
```

---

# Python Libraries

```bash
pip install

supabase

sqlalchemy

psycopg2-binary
```

---

# Example SQLAlchemy Connection

```python
from sqlalchemy import create_engine
import os

engine = create_engine(
    os.getenv("DATABASE_URL")
)
```

---

# Advantages of This Design

- Normalized schema
- Fast joins
- JSONB flexibility
- Foreign key integrity
- Historical experiment tracking
- Efficient indexing
- Compatible with Supabase
- Easily extensible for future models