# Database Portability: Migrating from Supabase to Standard PostgreSQL

The Faculty Appraisal System is designed to be highly portable. While it currently uses Supabase for convenience (Auth, Storage, and Hosted Postgres), it can be transitioned back to a self-hosted or standard PostgreSQL environment with minimal changes.

## 1. Database Configuration
The application uses SQLAlchemy, which is database-agnostic.
- **Current Setup:** Uses Supabase connection string in `.env`.
- **Migration:** Update `DATABASE_URL` in `.env` to point to your standard PostgreSQL instance.
  ```dotenv
  DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
  ```
- **Schema:** The schema uses standard PostgreSQL types (including UUIDs). You can use `Base.metadata.create_all(bind=engine)` in `main.py` (temporarily uncommented) to recreate the tables on a new instance.

## 2. Authentication Replacement
Supabase Auth provides JWT verification. In a standard Postgres setup, you would need to:
- **Implement Local Auth:** Add endpoints for Login/Signup.
- **JWT Handling:** Use a library like `python-jose` to sign and verify your own tokens.
- **Update Dependency:** Modify `src/setup/dependencies.py` to verify your local JWTs instead of calling `supabase.auth.get_user()`.

## 3. File Storage Replacement
Currently, proofs are stored in Supabase Storage buckets.
- **Requirement:** Standard Postgres does not provide object storage.
- **Options:**
    - **Local Disk:** Save files to a directory on the server. Update `src/setup/storage_utils.py` to use `shutil` or `aiofiles` to save locally.
    - **S3-Compatible Storage:** Use AWS S3, DigitalOcean Spaces, or MinIO. Update `storage_utils.py` to use `boto3`.
- **Database:** The `document` column in the database stores the file path/URL, so the database schema remains unchanged.

## 4. Networking & Access
If using a local Postgres server on a different machine:
- Ensure the Postgres server is listening on the network interface (`listen_addresses = '*'` in `postgresql.conf`).
- Update `pg_hba.conf` to allow the backend server's IP address.
- Ensure port `5432` is open in the firewall.
