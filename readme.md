## Production Incidents Prevented by Data Contract Tests

1. **`test_data_contract_schema_and_types`**:
   - **Incident Prevented:** An upstream service unexpectedly renames a column or sends incorrect data types, which would crash the inference API and cause widespread 500 Internal Server Errors in production.

2. **`test_data_contract_range_and_null_rate`**:
   - **Incident Prevented:** An upstream data pipeline breaks and injects excessive null values into the feature payload, causing the model to output wildly inaccurate predictions and corrupting downstream business decisions.