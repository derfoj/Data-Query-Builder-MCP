# Tool: load_csv

## Purpose
Load a CSV file into a new SQLite table with automatic column type detection.

## System Prompt
You have the ability to load CSV files into an SQLite database. Use this tool when:
- A user provides a new CSV file they want to analyze
- You need to import data from a file path
- Setting up the initial dataset for queries

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_path` | string | Yes | Path to the CSV file (absolute or relative to current directory) |
| `table_name` | string | Yes | Descriptive name for the new table (e.g., 'employees', 'sales_data') |

## Behavior

- **Auto-detection**: Scans data and determines column types as INTEGER, REAL, or TEXT
- **Row count**: Automatically calculated during import
- **Column detection**: Uses CSV headers as column names
- **Error handling**: Returns descriptive errors if file not found or parsing fails

## Returns

Success:
```
✓ Loaded 1000 rows into table 'employees' with columns: id, name, department, salary
```

Error:
```
Error loading CSV: [detailed error message]
```

## When to Use

✓ "Load this CSV file"  
✓ "I have data in a file"  
✓ Multiple CSV files for multi-table analysis  
✓ Refreshing data with new CSV import  

## When NOT to Use

✗ Querying existing data → use `run_query`  
✗ Viewing schema → use `describe_schema`  
✗ Checking what tables exist → use `list_tables`  

## Best Practices

1. **Verify file exists** before calling the tool
2. **Use descriptive table names** in snake_case (singular preferred)
   - Good: `employees`, `customer_orders`, `sales`
   - Bad: `data`, `table1`, `MyData`
3. **After loading**, call `describe_schema()` to verify column type detection
4. **Handle type errors**: If types are wrong, guide user to fix CSV or use CAST in queries
5. **Large files**: No limits on file size, but very large CSVs may affect performance

## Common Issues

| Issue | Solution |
|-------|----------|
| File not found | Verify absolute or relative path is correct |
| Wrong column types | Check source CSV for consistent values; may need manual CAST in queries |
| Special characters in headers | Column names taken from CSV headers; avoid SQL keywords |
| Duplicate table names | Drop existing table first or use different name |
| Memory issues with huge files | Split CSV into chunks and load separately |

## Example Usage

```
load_csv("c:/data/employees.csv", "employees")
load_csv("./sales_data.csv", "sales")
load_csv("D:/backup/customers.csv", "customer_records")
```

## Workflow Integration

**Typical Sequence:**
1. `load_csv()` - Import the data
2. `list_tables()` - Verify it loaded
3. `describe_schema()` - Check column types
4. `run_query()` - Start analyzing

## Related Tools

- [describe_schema](tool_describe_schema.md) - Verify loaded table structure
- [list_tables](tool_list_tables.md) - See all loaded tables
- [run_query](tool_run_query.md) - Analyze the loaded data
