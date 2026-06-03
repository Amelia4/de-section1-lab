# Schema Design - E-Commerce Store

## SQL Schema (Normalized)

### Customers
| Column | Type |
|----------|----------|
| customer_id | INTEGER (PK) |
| name | TEXT |
| email | TEXT |

### Products
| Column | Type |
|----------|----------|
| product_id | INTEGER (PK) |
| name | TEXT |
| price | REAL |

### Orders
| Column | Type |
|----------|----------|
| order_id | INTEGER (PK) |
| customer_id | INTEGER (FK) |
| product_id | INTEGER (FK) |
| qty | INTEGER |
| order_date | TEXT |

### Relationships

Customers (1) ---- (*) Orders

Products (1) ---- (*) Orders

---

## NoSQL Schema (Embedded)

```json
{
  "_id": 101,
  "customer": {
    "id": 1,
    "name": "Alice"
  },
  "order_date": "2024-01-01",
  "items": [
    {
      "product": "Laptop",
      "qty": 1,
      "price": 999.0
    },
    {
      "product": "Mouse",
      "qty": 1,
      "price": 25.5
    }
  ]
}
```

## Comparison

### SQL
- Structured tables
- Uses relationships
- Requires JOIN
- Suitable for analytics and reporting

### NoSQL
- Flexible document structure
- Embedded data
- Fewer joins
- Suitable for scalable web applications

## Reflection

For analytics and reporting, SQL databases are easier because data is normalized and can be queried using joins.

For scalable web applications, NoSQL databases are often more flexible because related data can be stored in a single document.