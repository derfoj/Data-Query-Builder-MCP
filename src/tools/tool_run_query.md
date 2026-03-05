# Tool: run_query

## Purpose
Execute SELECT queries against the database for data analysis and exploration.

## System Prompt
You have the ability to execute SELECT queries. This is your primary tool for data analysis.

**CRITICAL SECURITY RESTRICTIONS (Enforced by the tool):**
- ✗ Cannot DROP, DELETE, ALTER, INSERT, or UPDATE tables/data
- ✗ Cannot run PRAGMA statements
- ✗ Only SELECT queries allowed
- These restrictions protect data integrity automatically

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `sql` | string | Yes | - | Complete SQL SELECT query with exact column names from `describe_schema()` |
| `limit` | integer | No | 50 | Maximum rows to return. Lower for exploration (5-20), higher for analysis (100-1000) |

## Behavior

- **Auto-limit**: If LIMIT not in query, automatically adds `LIMIT {limit}` parameter
- **Security**: Rejects any non-SELECT operations before execution
- **Format**: Returns results as comma-separated values with column headers
- **History**: All executed queries added to session history (accessible via resource `db://query-history`)

## Returns

Success:
```
id, name, department, salary
1, Alice Johnson, Engineering, 95000
2, Bob Smith, Sales, 75000
3, Carol White, Engineering, 88000
```

Error:
```
Error: Query contains forbidden operation 'UPDATE'. Only SELECT is allowed.
```

Or:
```
Query returned no results.
```

## When to Use

✓ "Show me data from X"  
✓ "Analyze/filter/group/sort the data"  
✓ "Count or aggregate data"  
✓ "Join data from multiple tables"  
✓ "Find records matching specific criteria"  
✓ "Explore data patterns"  

## When NOT to Use

✗ Modifying data (INSERT/UPDATE/DELETE) → NOT allowed  
✗ Creating/dropping tables → NOT allowed  
✗ Just need schema info → use `describe_schema`  
✗ Just need quick stats → use `get_statistics`  
✗ Just need table overview → use `list_tables`  

## Best Practices

### Before Writing Queries
1. Always call `describe_schema()` first
2. Know exact column names and their types
3. Understand table relationships if using JOINs

### Query Construction
1. **Start simple** with `SELECT * FROM table LIMIT 10` to explore
2. **Use exact column names** from `describe_schema()`
3. **Filter with WHERE** to focus on relevant rows
4. **Aggregate with GROUP BY** for summaries
5. **Sort with ORDER BY** for meaningful order
6. **Use LIMIT** for large datasets (start with 10-50, increase if needed)

### Type Handling
```sql
-- Check column type from describe_schema() first
-- INTEGER/REAL columns:
WHERE salary > 50000
WHERE age BETWEEN 25 AND 35

-- TEXT columns:
WHERE name LIKE '%Smith%'
WHERE department = 'Engineering'

-- Type mismatch? Use CAST():
WHERE CAST(employee_id AS TEXT) = '12345'
```

### Sort and Summarize
```sql
-- Simple sort:
ORDER BY salary DESC

-- Multiple sort criteria:
ORDER BY department, name ASC

-- Aggregation:
SELECT department, COUNT(*) as count, AVG(salary) as avg_salary
FROM employees
GROUP BY department
HAVING COUNT(*) > 5
```

### Joins
```sql
-- Verify foreign key relationships first using describe_schema()
SELECT e.name, s.amount, s.date
FROM employees e
JOIN sales s ON e.id = s.employee_id
WHERE s.amount > 1000
ORDER BY s.date DESC
```

## Example Queries

### Exploration
```sql
SELECT * FROM employees LIMIT 10
```

### Filtering
```sql
SELECT name, salary 
FROM employees 
WHERE salary > 50000
```

### Aggregation
```sql
SELECT department, COUNT(*) as employee_count
FROM employees
GROUP BY department
ORDER BY employee_count DESC
```

### Complex Analysis
```sql
SELECT 
  department,
  COUNT(*) as headcount,
  AVG(CAST(salary AS REAL)) as avg_salary,
  MIN(salary) as min_salary,
  MAX(salary) as max_salary
FROM employees
GROUP BY department
HAVING COUNT(*) > 0
ORDER BY avg_salary DESC
LIMIT 20
```

## Common Issues

| Issue | Error/Symptom | Solution |
|-------|---|---|
| Column not found | "Error executing query" | Check exact name in `describe_schema()` |
| Type mismatch | Wrong results or error | Use CAST() to convert types |
| Too many results | Results truncated at 50 | Increase `limit` parameter or add WHERE to filter |
| Query timeout | Long running | Add WHERE clause to filter, or check table size |
| No results when expected | "Query returned no results" | Verify WHERE conditions; try simpler query |
| Syntax error | "Error executing query" | Check SQL syntax; verify column names and table names |

## Query Patterns - Copy & Modify

### Count rows
```sql
SELECT COUNT(*) as row_count FROM table_name
```

### Get distinct values
```sql
SELECT DISTINCT column_name FROM table_name LIMIT 50
```

### Find nulls
```sql
SELECT * FROM table_name WHERE column_name IS NULL
```

### Text search
```sql
SELECT * FROM table_name WHERE column_name LIKE '%search_term%'
```

### Range queries
```sql
SELECT * FROM table_name WHERE column_name BETWEEN value1 AND value2
```

### Multiple conditions
```sql
SELECT * FROM table_name 
WHERE condition1 = value1 AND condition2 > value2 OR condition3 IS NULL
```

## Execution Flow

1. User requests data analysis
2. Call `describe_schema()` if unsure of structure
3. Construct SELECT query with verified column names
4. Execute with appropriate `limit`
5. Analyze results OR refine query and retry
6. Query added to history (viewed via `db://query-history`)

## SQL Functions Available

- `COUNT()` - Count rows
- `SUM()` - Add numeric values
- `AVG()` - Average numeric values
- `MIN()` / `MAX()` - Minimum/maximum values
- `GROUP_CONCAT()` - Combine values
- `SUBSTR()` - Extract text substrings
- `UPPER()` / `LOWER()` - Case conversion
- `CAST()` - Type conversion
- `CASE` - Conditional logic
- `LIKE` - Pattern matching
- Boolean: `AND`, `OR`, `NOT`
- Comparison: `=`, `!=`, `<`, `>`, `<=`, `>=`, `BETWEEN`, `IN`
- Null: `IS NULL`, `IS NOT NULL`

## Related Tools

- [describe_schema](tool_describe_schema.md) - Verify column names and types
- [list_tables](tool_list_tables.md) - See available tables
- [get_statistics](tool_get_statistics.md) - Quick column statistics
- [load_csv](tool_load_csv.md) - Load new data to query
