import os
import streamlit as st
from supabase import create_client

# ------------------------------------------------------------------ #
#  ONE place where the Supabase client is created.                   #
#  Reads credentials from Streamlit Cloud Secrets (secrets.toml).    #
#  Students: never hard-code keys here.                              #
# ------------------------------------------------------------------ #

def get_secret(key: str) -> str:
    try:
        return st.secrets[key]           # works on Streamlit Cloud + local secrets.toml
    except (KeyError, FileNotFoundError):
        value = os.environ.get(key)      # fallback for Codespaces / env vars
        if not value:
            raise RuntimeError(
                f"Secret '{key}' not found. "
                "Add it to .streamlit/secrets.toml (local) or Streamlit Cloud secrets, "
                "or as a Codespaces environment secret."
            )
        return value

@st.cache_resource          # created once, reused across reruns
def get_supabase():
    url  = st.secrets["SUPABASE_URL"]
    key  = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


# ------------------------------------------------------------------ #
#  Auth helpers                                                       #
# ------------------------------------------------------------------ #

def sign_up(email: str, password: str):
    """Returns (user, error_message)."""
    sb = get_supabase()
    try:
        res = sb.auth.sign_up({"email": email, "password": password})
        return res.user, None
    except Exception as e:
        return None, str(e)

def sign_in(email: str, password: str):
    """Returns (user, error_message)."""
    sb = get_supabase()
    try:
        res = sb.auth.sign_in_with_password({"email": email, "password": password})
        return res.user, None
    except Exception as e:
        return None, str(e)

def sign_out():
    get_supabase().auth.sign_out()


# ------------------------------------------------------------------ #
#  Profile helpers (onboarding data goes in a "profiles" table)      #
# ------------------------------------------------------------------ #

def save_profile(user_id: str, data: dict):
    """Upsert onboarding answers for this user."""
    sb = get_supabase()
    sb.table("profiles").upsert({"user_id": user_id, **data}).execute()

def get_profile(user_id: str):
    """Return the profile row, or None if it doesn't exist yet."""
    sb = get_supabase()
    res = sb.table("profiles").select("*").eq("user_id", user_id).maybe_single().execute()
    return res.data          # dict or None