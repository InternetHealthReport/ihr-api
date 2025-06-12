# Adding a New Endpoint to the IHR FastAPI Application

This guide explains how to add a new endpoint to the application, ensuring it adheres to the **Service-Controller-Repository** architecture and follows practices such as pagination, ordering, and wrapping responses in the `GenericResponseDTO`.

---

## Steps to Add a New Endpoint

### 1. **Define the Controller**
Create a new controller file in the `controllers/` directory or modify an existing one. Use `APIRouter` to define the endpoint and ensure the response is wrapped in `GenericResponseDTO`.

---

### 2. **Implement the Service**
Create a service file in the `services/` directory or modify an existing one. The service should interact with the repository and map database models to DTOs.

---

### 3. **Create the Repository**
Add a repository file in the `repositories/` directory or modify an existing one. Ensure it handles pagination and ordering using `offset` and `limit`.

---

### 4. **Define the Model**
Add a new model in the `models/` directory or modify an existing one. If you need indexing or hypertable functionality, include the `__indexes__` and `__hypertable__` attributes.

#### `__indexes__` Attribute
Defines custom indexes for the table. Example:
```python
__indexes__ = [
    {
        'name': 'new_entity_field1_idx',
        'columns': ['field1']
    },
]
```

#### `__hypertable__` Attribute
Defines TimescaleDB hypertable metadata. Example:
```python
__hypertable__ = {
    'time_column': 'timestamp_field',  # Time column for hypertable
    'chunk_time_interval': '1 day',   # Chunk interval for partitioning
    'compress': True,                 # Enable compression
    'compress_segmentby': 'field1',   # Segment by column for compression
    'compress_orderby': 'timestamp_field',  # Order by column for compression
    'compress_policy': True,          # Enable compression policy
    'compress_after': '7 days'        # Compress data older than 7 days
}
```

Example model:
```python
# filepath: models/new_entity_model.py
from sqlalchemy import Column, String, TIMESTAMP
from config.database import Base

class NewEntity(Base):
    __tablename__ = "new_entity"

    __indexes__ = [
        {
            'name': 'new_entity_field1_idx',
            'columns': ['field1']
        },
    ]

    __hypertable__ = {
        'time_column': 'timestamp_field',
        'chunk_time_interval': '1 day',
        'compress': True,
        'compress_segmentby': 'field1',
        'compress_orderby': 'timestamp_field',
        'compress_policy': True,
        'compress_after': '7 days'
    }

    field1 = Column(String, primary_key=True)
    field2 = Column(String, nullable=False)
    timestamp_field = Column(TIMESTAMP, nullable=False)
```

---

### 5. **Create the DTO**
Add a DTO in the `dtos/` directory to define the structure of the response.

Example:
```python
# filepath: dtos/new_entity_dto.py
from pydantic import BaseModel

class NewEntityDTO(BaseModel):
    field1: str
    field2: str

    class Config:
        from_attributes = True
```
---

## Key Notes
1. **Pagination and Ordering**: Ensure the repository uses `offset` and `limit` for pagination and supports ordering by columns.
2. **GenericResponseDTO**: Wrap all responses in `GenericResponseDTO` to maintain consistency.
3. **Indexes**: Use the `__indexes__` attribute in models to define indexes.
4. **Hypertables**: Use the `__hypertable__` attribute in models for TimescaleDB-specific features. The hypertables will only be generated for newely generated tables. Fields:
   - `time_column`: Column used for time-based partitioning.
   - `chunk_time_interval`: Interval for partitioning data.
   - `compress`: Enable compression.
   - `compress_segmentby`: Column for segmenting compressed data.
   - `compress_orderby`: Column for ordering compressed data.
   - `compress_policy`: Enable automatic compression policy.
   - `compress_after`: Time after which data is compressed.
