# Tool: list_tables

## Purpose
List all loaded tables in the database with their row counts.

## System Prompt
You have the ability to list all tables in the database. Use this tool when:
- A user asks "What tables do I have?" or "What's loaded?"
- Getting a quick overview of loaded data
- Verifying successful CSV import
- Understanding database scope and size

## Parameters

None - this is a read-only introspection tool.

## Behavior

- **Scope**: Shows ALL tables currently in the database
- **Metadata**: Displays exact row count for each table
- **Speed**: Instant query of database metadata
- **Format**: Simple, easy-to-read list with counts

## Returns

```
Tables:
  - employees (150 rows)
  - sales (1250 rows)
  - departments (8 rows)
```

Or if empty:
```
No tables loaded yet.
```

## When to Use

✓ Verify CSV import was successful  
✓ "What data is in the database?"  
✓ Quick data scope check  
✓ Before deciding what to analyze  
✓ After loading multiple files  
✓ Confirming table names before writing queries  

## When NOT to Use

✗ Need column details → use `describe_schema`  
✗ Need column statistics → use `get_statistics`  
✗ Ready to query → use `run_query`  
✗ Need to load data → use `load_csv`  

## Best Practices

1. **Call early and often**: Use this as your first sanity check
2. **Verify imports**: After `load_csv()`, use `list_tables()` to confirm
3. **Load multiple files**: If loading several CSVs, verify each appeared in the list
4. **Size awareness**: Row counts help determine query strategy
   - Small tables (< 1K rows): Can query with minimal LIMIT concerns
   - Medium tables (1K - 100K rows): Use reasonable LIMIT (50-500)
   - Large tables (> 100K rows): Use smaller LIMIT (10-50) for exploration
5. **Cross-reference**: Use table names shown here in `describe_schema()` and `run_query()`

## Typical Usage Flow

```
User: "I've loaded some data, show me what's there"

1. Call list_tables() → Get overview of loaded tables and row counts
2. Observe: "3 tables loaded, mostly medium-sized"
3. Next step depends on user goal:
   - "What columns do these have?" → Use describe_schema()
   - "Show me the data" → Use run_query()
   - "Load more data" → Use load_csv()
```

## Workflow Integration

### Initial Data Load
```
1. load_csv("file1.csv", "table1")
2. load_csv("file2.csv", "table2")
3. list_tables() → Verify both loaded
4. describe_schema() → See structure
5. run_query() → Start analyzing
```

### Checking Database State
```
User: "Are all my files loaded?"
Answer: Call list_tables() and review the list
If table missing: Call load_csv() again with correct path
```

### Performance Planning
```
get_statistics() needs which columns?
→ First: list_tables() to know what's available
→ Then: describe_schema() to find column names
→ Then: get_statistics() for specific columns
```

## Size Guidelines for Analysis

| Table Size | Recommended LIMIT | Use Case |
|---|---|---|
| < 100 rows | No limit needed | Explore all data |
| 100-1K rows | 50-100 | Safe exploration |
| 1K-10K rows | 20-50 | Careful exploration |
| 10K-100K rows | 10-20 | Aggregation queries better |
| > 100K rows | 5-10 | Always filter with WHERE |

## Verification Checklist

After loading CSV files, use `list_tables()` to verify:

- [ ] All expected files appear in the list
- [ ] Row counts match expected data size
- [ ] No unexpected tables from previous sessions
- [ ] Table names are correct and descriptive
- [ ] Row count > 0 for each table

If any checks fail:
- Missing table? Verify file path in `load_csv()` call
- Wrong row count? Check CSV source for actual data
- Wrong table name? Use `describe_schema()` to confirm then rename strategy
- Extra tables? May be fine (prior session data), list for reference

## Quick Diagnostics

| Problem | How to Check | Solution |
|---|---|---|
| File didn't load | `list_tables()` - missing table | Call `load_csv()` again with correct path |
| Wrong table name | `list_tables()` - see actual name | Delete and reload OR use actual name in queries |
| Table is empty | `list_tables()` - row count is 0 | Check CSV file has data; verify delimiter |
| Too many tables | `list_tables()` - unexpected tables | May be from prior session; proceed with current tables |

## Related Tools

- [load_csv](tool_load_csv.md) - Load data before listing
- [describe_schema](tool_describe_schema.md) - See table structure and columns
- [run_query](tool_run_query.md) - Query the tables listed
- [get_statistics](tool_get_statistics.md) - Analyze specific columns

## Example Scenarios

### Scenario 1: First time user loading data
```
User: "I loaded data, what should I do now?"
1. list_tables() → Shows 1 table: employees (500 rows)
2. "Great! Let me show you the structure..."
3. describe_schema()
4. "Ready to analyze?"
5. run_query()
```

### Scenario 2: Multi-file analysis
```
User: "Load employees.csv, sales.csv, and departments.csv then show me everything"
1. load_csv("employees.csv", "employees")
2. load_csv("sales.csv", "sales")
3. load_csv("departments.csv", "departments")
4. list_tables() → Verify all 3 loaded successfully
5. describe_schema() → Show full structure
```

### Scenario 3: Checking what's in the database
```
User: "What data do I have available? I forgot what I loaded"
1. list_tables() → Shows all available tables with sizes
2. Present list to user
3. Offer more detailed schema view or query options
```
