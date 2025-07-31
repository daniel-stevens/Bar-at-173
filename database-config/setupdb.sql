-- 1️⃣  create a login role the app will use
CREATE ROLE baruser
  WITH LOGIN
  PASSWORD 'password';      -- ← pick a strong password

-- 2️⃣  create the database owned by that role
CREATE DATABASE barat173
  OWNER baruser
  ENCODING 'UTF8';

-- 3️⃣  give the role full rights on that DB (redundant but explicit)
GRANT ALL PRIVILEGES ON DATABASE barat173 TO baruser;
