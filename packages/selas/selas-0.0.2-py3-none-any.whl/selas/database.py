
import hashlib
import json
import os
from datetime import datetime, timedelta
from tokenize import Number
from typing import List, Optional
from enum import Enum

from dotenv import load_dotenv
import httpx
from postgrest import APIResponse
from pydantic import BaseModel
from supabase import Client, create_client

load_dotenv()

class Scope(Enum):
    USER = "user"
    ORGANISATION = "organisation"
    PUBLIC = "public"


def get_supabase() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)

    return supabase

def sign_in(email: str, password: str) -> Client:
    supabase = get_supabase()
    
    try:
        print("Signing in...")
        supabase.auth.sign_in(
            email=email,
            password=password,
        )
        supabase.postgrest.session.headers["Authorization"] = "Bearer " + supabase.auth.session().access_token
        print("Signed in!")
    except httpx.HTTPStatusError:
        raise ValueError("Something is wrong with you email and/or password.")

    return supabase


def close_session(supabase: Client):
    supabase.auth.sign_out()
    supabase.auth.close()


def create_token(supabase: Client, scope: Scope = Scope.USER, quota: float = 1) -> str:
    # supabase = get_supabase()
    user = supabase.auth.current_user
    # print(user.id)
    # user_data = supabase.table("profiles").select("*").eq("id", user.id).execute()
    # print(user_data)

    ttl = str(datetime.now() + timedelta(days=1))
    # token_name = #'uniqueusername456'

    # print('--> user_id: {', str(user.id), '}')
    # print('--> dateTime: ', str(datetime.now()))
    token_data = supabase.table("tokens").insert({'user_id': str(user.id), 'ttl': ttl, 'scope': scope.value, 'quota': quota}).execute()
    if len(token_data.data) > 0:
        print('--> new token added: ', token_data.data[0]['id'])
        return token_data.data[0]
    else:
        print('--> Error token not added')
        return None


def create_job(supabase: Client, token_key: str, config: json):
    user = supabase.auth.current_user
    job_data = supabase.table("jobs").insert({'user_id': str(user.id), 'configs': [config], 'token_key': token_key}).execute()
    if len(job_data.data) > 0:
        print('--> new job added: ', job_data.data[0]['id'])
        return job_data.data[0]
    else:
        print('--> Error job not added')
        return None

# create token
#create image
#post un job a partir d'un prompt