import asyncio
import os
import signal
import time
import sys
from pathlib import Path

import typer
from dotenv import load_dotenv

from selas.database import (sign_in, create_token)


app = typer.Typer()

@app.command()
def login():
    email = typer.prompt("Enter your email")
    password = typer.prompt("Enter your password", hide_input=True)
    supabase = sign_in(email, password)
    supabase.auth.sign_out()
    


@app.command()
def create_token():
    create_token()


if __name__ == "__main__":
    app()