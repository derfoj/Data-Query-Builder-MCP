# Tool: get_statistics

## Purpose
Compute and display summary statistics for a specific column: total rows, nulls, min, max, and mean.

## System Prompt
You have the ability to compute summary statistics for a specific column. Use this when:
- A user asks "What are the stats for this column?"
- Analyzing numerical or mixed data distributions
- Assessing data quality (checking nulls and ranges)
- Quick overview of column characteristics

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `table_name` | string | Yes | Exact table name from `describe_schema()` |
| `column` | string | Yes | Exact column name from `describe_schema()` |

## Behavior

- **Scope**: Analyzes a single column across all rows in the specified table
- **Null handling**: Separately counts NULL values
- **Mean calculation**: Computed for all types but only meaningful for numeric columns
- **Performance**: Fast even on large tables (aggregation operation)

## Returns

```
Statistics for employees.salary:
  Total rows: 150
  Non-null: 148
  Nulls: 2
  Min: 35000
  Max: 125000
  Mean: 72500.00
```

Or for TEXT columns:
```
Statistics for employees.name:
  Total rows: 150
  Non-null: 150
  Nulls: 0
  Min: Alice
  Max: Zachary
  Mean: N/A
```

## When to Use

✓ "Show me statistics for [column]"  
✓ "What's the range of values in this column?"  
✓ "Show me min/max/average"  
✓ "How many nulls in this column?"  
✓ Assessing data quality issues  
✓ Understanding data distribution  
✓ Identifying outliers or anomalies  

## When NOT to Use

✗ Complex statistical analysis (use `run_query` with custom stats)  
✗ Multiple columns at once (call once per column)  
✗ Grouped statistics (use `run_query` with GROUP BY instead)  
✗ Time series analysis (use `run_query` with window functions)  
✗ Just need table overview (use `list_tables`)  
✗ Need schema info (use `describe_schema`)  

## Best Practices

1. **Verify names first**: Always check `describe_schema()` for exact table and column names
2. **Call for each column**: If analyzing multiple columns, make separate calls
3. **Interpret nulls**: High null count indicates potential data quality issues
4. **Type awareness**: 
   - For numeric columns (INTEGER/REAL): All values are meaningful
   - For TEXT columns: Min/Max are alphabetical, Mean is N/A
5. **Quality assessment**: Use statistics to guide data cleaning decisions
6. **Compare across columns**: Get statistics for multiple columns to identify issues

## Common Patterns

### Detect missing data
```
Get statistics → Check "Nulls" count
If high: Consider filtering NULLs in queries or investigating data source
```

### Understand numeric range
```
Get statistics → Check Min/Max/Mean
If Max is much larger than Mean: Possible outliers
If Mean is far from Min: Right-skewed or outliers present
```

### Validate data quality
```
Get statistics for each key column → Check for unexpected nulls
If nulls found: 
  - Use run_query() to find which rows have nulls
  - Determine if data needs cleaning
  - Adjust queries to handle nulls (IS NULL, IS NOT NULL)
```

## Example Usage Sequence

```
User: "Analyze the salary data quality"

1. describe_schema() → Find table 'employees' and column 'salary'
2. get_statistics("employees", "salary") → Get distribution info
3. Results show: 2 nulls, min $35K, max $125K, mean $72.5K
4. Decide next steps:
   - If nulls found: Use run_query() to find which employees have null salary
   - If range seems wrong: Use run_query() to verify
   - If distribution looks good: Proceed to detailed analysis
```

## Statistics Interpretation Guide

| Statistic | What It Means | Action |
|-----------|---|---|
| **High Null Count** | Missing data | Investigate source; filter in queries; document gaps |
| **Min/Max Far Apart** | Wide range | Check for outliers with `run_query()` WHERE |
| **Mean Near Max** | Skewed right | May have outliers; use LIMIT to see extremes |
| **Mean Near Min** | Skewed left | Most values clustered low; check for patterns |
| **Min/Max Alphabetically** | TEXT column | Min/Max less meaningful; use DISTINCT instead |

## Data Quality Checks Using Statistics

### Check 1: Unexpected nulls
```
get_statistics() → If Nulls > expected, investigate
Use run_query(): SELECT * FROM table WHERE column IS NULL
```

### Check 2: Invalid range
```
get_statistics() → Min/Max seem wrong?
Use run_query(): SELECT column, COUNT(*) FROM table GROUP BY column ORDER BY column
```

### Check 3: Data type mismatch
```
get_statistics() for numeric column shows unexpected Min/Max?
Check describe_schema() - may be stored as TEXT
Use run_query() with CAST(): CAST(column AS INTEGER)
```

## Related Tools

- [describe_schema](tool_describe_schema.md) - Find exact table and column names
- [run_query](tool_run_query.md) - Detailed analysis and filtering
- [list_tables](tool_list_tables.md) - See all available tables
- [load_csv](tool_load_csv.md) - Load data before analyzing

## Advanced Usage

For more complex statistics, use `run_query()` instead:

```sql
-- Percentiles (use run_query):
SELECT 
  PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY salary) as q1,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) as median,
  PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY salary) as q3
FROM employees

-- Distribution in buckets:
SELECT 
  CASE 
    WHEN salary < 50000 THEN 'low'
    WHEN salary < 75000 THEN 'medium'
    ELSE 'high'
  END as salary_band,
  COUNT(*) as count
FROM employees
GROUP BY salary_band
```
