#!/bin/bash
/opt/mssql-tools/bin/sqlcmd \
  -S localhost -U SA -P "${MSSQL_SA_PASSWORD}" \
  -i /init-db/init.sql
