# Tool: describe_schema

## Purpose
List all tables and their columns with data types (INTEGER, REAL, or TEXT).

## System Prompt
You have the ability to describe the current database schema. Use this tool when:
- A user asks "What tables do I have?" or "Show me the schema"
- You need to verify column names before writing queries
- Understanding data structure before analysis begins
- Debugging query errors related to column names or types

## Parameters

None - this is a read-only introspection tool.

## Behavior

- **Scope**: Shows ALL tables currently in the database
- **Type information**: Displays each column's data type (INTEGER, REAL, TEXT)
- **Format**: Easy-to-read hierarchical listing
- **No network calls**: Instant query of local database metadata

## Returns

```
Table: employees
  - id (INTEGER)
  - name (TEXT)
  - department (TEXT)
  - salary (INTEGER)

Table: sales
  - id (INTEGER)
  - employee_id (INTEGER)
  - amount (REAL)
  - date (TEXT)
```

Or if empty:
```
No tables loaded yet.
```

## When to Use

✓ Right after loading CSV data to verify successful import  
✓ Before writing complex queries to ensure column name accuracy  
✓ When user asks "What data do I have?"  
✓ Debugging "column not found" query errors  
✓ Understanding foreign key relationships between tables  
✓ Verifying type detection from CSV imports  

## When NOT to Use

✗ Just need table names and row counts → use `list_tables`  
✗ Need statistics on a column → use `get_statistics`  
✗ Ready to query data → use `run_query`  

## Best Practices

1. **Always call first** after loading CSV data
2. **Use exact column names** from the output in your SQL queries
   - Copy-paste column names to ensure correct spelling
   - SQL is case-sensitive in some databases
3. **Verify types before querying**
   - TEXT columns: use LIKE, string comparison
   - INTEGER/REAL: use mathematical operations
   - Mismatched types cause query errors
4. **Reference this output** when writing GROUP BY, WHERE, SELECT clauses
5. **Note relationships**: Identify foreign key columns manually (naming indicates relationships)

## Common Issues

| Issue | Solution |
|-------|----------|
| Column name in query causes error | Compare against output; check spelling and case |
| Type mismatch in WHERE clause | Use CAST() to convert types if needed |
| Can't find expected table | Use `list_tables()` to verify it exists; may need `load_csv()` |
| Unexpected column types | CSV may have mixed data; guide user to fix or use CAST in queries |

## Example Workflow

```
User: "What data do I have?"
1. Call describe_schema() to get full view
2. Present table and column list
3. Offer to analyze or query specific tables
```

## Query Reference Using Schema

Once you know the schema, write queries with confidence:

```sql
-- Using exact names from schema:
SELECT name, salary FROM employees WHERE salary > 50000

-- Multiple tables respect column types:
SELECT e.name, s.amount, s.date 
FROM employees e 
JOIN sales s ON e.id = s.employee_id 
WHERE s.amount > 1000
```

## Related Tools

- [load_csv](tool_load_csv.md) - Load new data before describing
- [list_tables](tool_list_tables.md) - See table row counts
- [run_query](tool_run_query.md) - Query using schema info
- [get_statistics](tool_get_statistics.md) - Analyze specific columns
