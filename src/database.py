"""
FerreRAP — Conexión a Supabase
IS2 · UCP · 2026
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from postgrest import SyncPostgrestClient
import httpx

# Cargar .env desde la raíz del proyecto
load_dotenv(Path(__file__).resolve().parent.parent / '.env')

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
MARGEN_GANANCIA = float(os.getenv("MARGEN_GANANCIA", 50)) / 100  # 0.5

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Faltan SUPABASE_URL o SUPABASE_KEY en el archivo .env")


class SupabaseDB:
    """
    Cliente ligero de Supabase que usa PostgREST directamente.
    Evita dependencias pesadas (pyiceberg/storage) que no necesitamos.
    """
    def __init__(self, url, key):
        self.rest_url = f"{url}/rest/v1"
        self.key = key
        self.headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
        }
        # Timeout de 10s para evitar cuelgues en cold-start de Supabase
        _http_client = httpx.Client(
            timeout=httpx.Timeout(10.0, connect=10.0),
            headers=self.headers,
        )
        self._client = SyncPostgrestClient(
            self.rest_url,
            headers=self.headers,
            http_client=_http_client,
        )

    def table(self, name):
        return self._client.from_(name)


supabase = SupabaseDB(SUPABASE_URL, SUPABASE_KEY)
