# RecipeLab Data Model

## Tables
- `recipes`
  - `id` (UUID)
  - `title` (TEXT)
  - `source` (TEXT)
  - `content` (TEXT)
  - `created_at` (TIMESTAMPTZ)
- `recipe_chunks`
  - `id` (UUID)
  - `recipe_id` (UUID FK)
  - `chunk_index` (INT)
  - `content` (TEXT)
  - `embedding` (VECTOR)
  - `created_at` (TIMESTAMPTZ)
- `ingestion_jobs`
  - `id` (UUID)
  - `recipe_id` (UUID)
  - `source` (TEXT)
  - `status` (TEXT)
  - `detail` (TEXT)
  - `created_at` (TIMESTAMPTZ)
  - `updated_at` (TIMESTAMPTZ)
- `user_preferences`
  - `id` (UUID)
  - `user_id` (TEXT)
  - `rules` (JSONB)
  - `created_at` (TIMESTAMPTZ)
- `pantry_items`
  - `id` (UUID)
  - `user_id` (TEXT)
  - `item` (TEXT)
  - `quantity` (TEXT)
  - `created_at` (TIMESTAMPTZ)
- `chat_sessions`
  - `id` (UUID)
  - `user_id` (TEXT)
  - `context` (JSONB)
  - `created_at` (TIMESTAMPTZ)
- `substitution_history`
  - `id` (UUID)
  - `recipe_id` (UUID)
  - `from_ingredient` (TEXT)
  - `to_ingredient` (TEXT)
  - `created_at` (TIMESTAMPTZ)

## Notes
- `recipe_chunks.embedding` uses `pgvector` with dimension set by `RECIPES_EMBEDDING_DIM`.
- Future schema changes should be managed via migrations.
