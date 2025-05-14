USE yumlsschooldb;
GO

PRINT '=== PRIMARY KEYS ===';
SELECT 
    t.name AS TableName,
    kc.name AS ConstraintName,
    c.name AS ColumnName
FROM 
    sys.key_constraints kc
JOIN 
    sys.tables t ON kc.parent_object_id = t.object_id
JOIN 
    sys.index_columns ic ON kc.unique_index_id = ic.index_id AND kc.parent_object_id = ic.object_id
JOIN 
    sys.columns c ON ic.column_id = c.column_id AND c.object_id = t.object_id
WHERE 
    kc.type = 'PK'
ORDER BY 
    t.name, kc.name;
GO

PRINT '';
PRINT '=== UNIQUE CONSTRAINTS ===';
SELECT 
    t.name AS TableName,
    i.name AS ConstraintName,
    c.name AS ColumnName
FROM 
    sys.indexes i
JOIN 
    sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
JOIN 
    sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
JOIN 
    sys.tables t ON i.object_id = t.object_id
WHERE 
    i.is_unique = 1 AND i.is_primary_key = 0
ORDER BY 
    t.name, i.name;
GO
