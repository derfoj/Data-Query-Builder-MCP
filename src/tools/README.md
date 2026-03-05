# Data Query Builder Tools - Index

This directory contains individual system prompts and documentation for each tool in the Data Query Builder MCP server.

## Tools Overview

| Tool | File | Purpose | Primary Use |
|------|------|---------|-------------|
| **load_csv** | [tool_load_csv.md](tool_load_csv.md) | Import CSV data into tables | Load new data files |
| **describe_schema** | [tool_describe_schema.md](tool_describe_schema.md) | View table structure and columns | Understand schema before querying |
| **run_query** | [tool_run_query.md](tool_run_query.md) | Execute SELECT queries | Analyze and explore data |
| **get_statistics** | [tool_get_statistics.md](tool_get_statistics.md) | Get column statistics | Assess data quality and distribution |
| **list_tables** | [tool_list_tables.md](tool_list_tables.md) | Show all tables and row counts | Quick database overview |

## Recommended Workflow

### 1. **Initial Setup** (First time with new data)
```
load_csv() → list_tables() → describe_schema() → run_query()
```

### 2. **Data Exploration** (Understanding new dataset)
```
list_tables() → describe_schema() → get_statistics() → run_query()
```

### 3. **Data Analysis** (Answering questions)
```
describe_schema() → run_query() → get_statistics() (if needed)
```

## Quick Reference

### I want to...

**...load data**
→ See [tool_load_csv.md](tool_load_csv.md)
- Upload a CSV file to analyze
- Set up multiple tables from different files

**...understand my data**
→ See [tool_describe_schema.md](tool_describe_schema.md) or [tool_list_tables.md](tool_list_tables.md)
- Know what tables and columns exist
- Write correct query syntax
- Check data types

**...analyze/query data**
→ See [tool_run_query.md](tool_run_query.md)
- Filter, sort, group data
- Calculate aggregates
- Join multiple tables
- Explore patterns

**...assess data quality**
→ See [tool_get_statistics.md](tool_get_statistics.md)
- Understand ranges and distributions
- Find missing/null values
- Check for anomalies

**...see what's loaded**
→ See [tool_list_tables.md](tool_list_tables.md)
- Quick overview of tables
- Verify imports were successful
- Understand database scope

## File Structure

```
tools/
├── README.md                  (This file - navigation and index)
├── tool_load_csv.md          (Load CSV files)
├── tool_describe_schema.md   (View schema)
├── tool_run_query.md         (Execute queries)
├── tool_get_statistics.md    (Column statistics)
└── tool_list_tables.md       (Table overview)
```

## Key Concepts

### Column Types
All columns are one of three types:
- **INTEGER** - Whole numbers (id, count, age)
- **REAL** - Decimal numbers (price, percentage, rating)
- **TEXT** - Strings (name, category, description)

### Selection Strategy
Choose the right tool for each question:

```
"How many tables?" → list_tables()
"What columns?" → describe_schema()
"Show me the data" → run_query()
"What's the data like?" → get_statistics()
"Load a file" → load_csv()
```

### Query Security
Some operations are **NEVER allowed** for data protection:
- ✗ UPDATE, DELETE, INSERT (cannot modify data)
- ✗ DROP (cannot delete tables)
- ✗ ALTER (cannot change structure)
- ✓ SELECT only (read-only analysis)

## Related Resources

- **[TOOL_PROMPTS.md](../TOOL_PROMPTS.md)** - Comprehensive tool overview
- **[server.py](../server.py)** - Tool source code and implementation
- **[Sample Data](../sample_employees.csv)** - Example dataset for testing

## Tips for Success

1. **Always verify schema first**: Call `describe_schema()` before writing complex queries
2. **Start simple**: Use LIMIT when exploring unknown data
3. **Check column names**: Use exact names from `describe_schema()` in queries
4. **Understand types**: Match your WHERE clause logic to column types
5. **Build incrementally**: Test queries with small limits, then expand
6. **Use statistics for quality**: Run `get_statistics()` to understand data health

## Common Workflows

### Load and Explore CSV
```
1. load_csv("file.csv", "table_name")
2. list_tables()                          # Verify loaded
3. describe_schema()                      # See structure
4. run_query("SELECT * FROM table_name LIMIT 10")  # Preview
5. get_statistics("table_name", "column") # Understand data
```

### Multi-table Analysis
```
1. load_csv() for each file
2. list_tables()                # See all tables
3. describe_schema()            # Understand relationships
4. run_query() with JOINs       # Analyze together
```

### Data Quality Assessment
```
1. list_tables()
2. describe_schema()
3. For each important column:
   - get_statistics()
   - run_query() to verify nulls/outliers
```

## Troubleshooting

| Problem | Solution | Tool |
|---------|----------|------|
| "Column not found" | Check exact spelling in schema | `describe_schema()` |
| Query returns nothing | Verify WHERE conditions or column types | `run_query()` with simpler query |
| Unexpected data types | CSV may have mixed values | Check raw CSV, use CAST() in queries |
| File won't load | Verify path and CSV format | Check file exists, try absolute path |
| Too many/few rows | Adjust LIMIT parameter | `run_query()` with different limit |

## Next Steps

- Choose a tool from the table above
- Read its individual guide for detailed usage
- Practice with [sample_employees.csv](../sample_employees.csv)
- Ask for help with specific queries
