# Reflection: Automated API Data Fetcher

## Why Use jq?
`jq` allows powerful and clean extraction and transformation of JSON data. Instead of reading through complex nested structures manually, we can filter, reshape, and extract fields directly.

## What Did the Script Do?
The script:
- Fetched user data from a public API
- Processed the data using jq
- Saved a simplified JSON (id, name, email) to a file
This replicates a typical backend job to clean and store API results.

## Why is this Useful?
Automating such processes saves time and ensures consistency. It also builds muscle memory for scripting, API handling, and data transformation — all critical for DevOps and data engineering roles.

## Difference Between curl and wget?
- `curl` is used for data transfer and supports piping directly into tools like `jq`
- `wget` is more for downloading files to disk

## Tools Installed
- `jq` — JSON processing
- `tree` — visualize directory
- `ripgrep (rg)` — super-fast search within files
