import os
import subprocess
from datetime import datetime
from getpass import getpass
import pyperclip as clip
import cryptocode
import pymongo
import pytz
import typer

cluster = pymongo.MongoClient("localhost")
db = cluster.PasswordManager
collections = db.PasswordManager
SECRET_KEY = os.getenv("SECRET_KEY", "Password")
IST = pytz.timezone('Asia/Kolkata')


def is_root() -> bool:
    if os.geteuid() == 0:
        return True
    args = "sudo -S echo OK".split()
    kwargs = dict(stdout=subprocess.PIPE,
                  encoding="ascii")
    cmd = subprocess.run(args, **kwargs)
    return "OK" in cmd.stdout


app = typer.Typer()


@app.command()
def add(key: str):
    value = getpass(prompt="[*] Enter Password: ")
    password = cryptocode.encrypt(value.strip(), SECRET_KEY)
    data = {
        "name": key.lower(),
        "password": password,
        "last_modified": datetime.now(IST)
    }
    query = collections.find_one({"name": key.lower()})
    if query is None:
        _ = collections.insert_one(data)
        msg = typer.style("Added password successfully!", fg=typer.colors.GREEN, bold=True)
    else:
        msg = typer.style(f"{key} already exist!!", fg=typer.colors.RED, bold=True)
    typer.echo(msg)


@app.command()
def list():
    if is_root():
        data = collections.find({})
        data = [{"key": i["name"], "last modified": i["last_modified"]} for i in data]
        msg = """"""
        for i in data:
            val = f"{i['key']}\t\t{i['last modified']}\n"
            msg += val
        msg = "Keys\t\t\tlast modified\n" + msg
        typer.echo(msg)
    else:
        msg = typer.style("\n\nAuthentication Failed!", fg=typer.colors.RED, bold=True)
        typer.echo(msg)


@app.command()
def get(key: str, copy: bool = False):
    if is_root():
        data = collections.find_one({"name": key.lower()})
        if data is not None:
            password = cryptocode.decrypt(data["password"], SECRET_KEY)
            if copy:
                clip.copy(password.strip())
                msg = typer.style("Copied to your clipboard!", fg=typer.colors.GREEN, bold=True)
            else:
                msg = typer.style("Your password is: ", fg=typer.colors.GREEN, bold=True)
                msg = msg + password
        else:
            msg = typer.style("key not found!", fg=typer.colors.RED, bold=True)
        typer.echo(msg)
    else:
        msg = typer.style("\n\nAuthentication Failed!", fg=typer.colors.RED, bold=True)
        typer.echo(msg)


@app.command()
def update(key: str):
    if is_root():
        password = getpass(prompt="[*]Enter Password: ")
        password = cryptocode.encrypt(password, SECRET_KEY)
        _ = collections.update_one({"name": key.lower()}, {"$set": {"password": password, "last_modified": datetime.now(IST)}})
        msg = typer.style("Password updated successfully!!", fg=typer.colors.GREEN, bold=True)
    else:
        msg = typer.style("\n\nAuthentication Failed!", fg=typer.colors.RED, bold=True)
    typer.echo(msg)


@app.command()
def delete(key: str):
    if is_root():
        key = collections.find_one({"name": key.lower()})
        if key is not None:
            key = key["name"]
        else:
            msg = typer.style(f"{key} not found!!", fg=typer.colors.RED, bold=True)
            typer.echo(msg)
            raise typer.Abort()
        action = typer.confirm("Are you sure you want to delete it?")
        if not action:
            msg = typer.style("Operation Canceled!!", fg=typer.colors.BRIGHT_BLUE, bold=True)
            typer.echo(msg)
            raise typer.Abort()
        _ = collections.delete_one({"name": key})
        msg = typer.style("Deleted Successfully!!", fg=typer.colors.CYAN, bold=True)
        typer.echo(msg)
    else:
        msg = typer.style("\n\nAuthentication Failed!", fg=typer.colors.RED, bold=True)
        typer.echo(msg)


if __name__ == "__main__":
    app()
