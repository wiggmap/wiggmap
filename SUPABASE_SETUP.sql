-- ============================================
-- WiggMap Supabase setup — auth + profiles
-- Run this once in your Supabase SQL Editor
-- ============================================

-- 1. Make sure profiles table has all required columns
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS username TEXT;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS avatar_url TEXT;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS country_origin TEXT;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS country_current TEXT;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS country_target TEXT;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS life_status TEXT;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS sector TEXT;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS languages JSONB DEFAULT '[]'::jsonb;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS onboarding_done BOOLEAN DEFAULT false;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT now();

-- 2. Auto-create profile on signup (Google OAuth + email/password)
-- This trigger guarantees no orphan auth.users rows without a profile
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  INSERT INTO public.profiles (id, username, avatar_url, onboarding_done)
  VALUES (
    NEW.id,
    COALESCE(
      NEW.raw_user_meta_data->>'full_name',
      NEW.raw_user_meta_data->>'name',
      split_part(NEW.email, '@', 1)
    ),
    COALESCE(
      NEW.raw_user_meta_data->>'avatar_url',
      NEW.raw_user_meta_data->>'picture'
    ),
    false
  )
  ON CONFLICT (id) DO NOTHING;
  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_new_user();

-- 3. Useful_count increment RPC (used by widget vote button)
CREATE OR REPLACE FUNCTION public.increment_useful(row_id uuid)
RETURNS void
LANGUAGE sql
AS $$
  UPDATE public.posts SET useful_count = COALESCE(useful_count, 0) + 1 WHERE id = row_id;
$$;

-- 4. Backfill: create profiles for existing auth.users that don't have one yet
INSERT INTO public.profiles (id, username, avatar_url, onboarding_done)
SELECT
  u.id,
  COALESCE(
    u.raw_user_meta_data->>'full_name',
    u.raw_user_meta_data->>'name',
    split_part(u.email, '@', 1)
  ),
  COALESCE(
    u.raw_user_meta_data->>'avatar_url',
    u.raw_user_meta_data->>'picture'
  ),
  false
FROM auth.users u
LEFT JOIN public.profiles p ON p.id = u.id
WHERE p.id IS NULL;

-- 5. Row-Level Security policies (if not already set)
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "profiles_select_all" ON profiles;
CREATE POLICY "profiles_select_all" ON profiles
  FOR SELECT USING (true);

DROP POLICY IF EXISTS "profiles_insert_own" ON profiles;
CREATE POLICY "profiles_insert_own" ON profiles
  FOR INSERT WITH CHECK (auth.uid() = id);

DROP POLICY IF EXISTS "profiles_update_own" ON profiles;
CREATE POLICY "profiles_update_own" ON profiles
  FOR UPDATE USING (auth.uid() = id);
