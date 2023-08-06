import json
from urllib import parse

import click as click
from click import prompt

from keap import Keap
from keap.settings import api_settings, IN_MEMORY_STORAGE, JSON_STORAGE


@click.group()
def cli():
    """
    Simple CLI for managing Keap API Access
    """
    pass


@cli.command()
def generate_client_config():
    client_id = prompt("What is your client id?", hide_input=True)
    client_secret = prompt("What is your client secret?", hide_input=True)
    redirect_url = prompt("Redirect URL", default=api_settings.REDIRECT_URL)
    app_name = prompt("App Name", default=api_settings.APP_NAME)
    allow_none = prompt("Allow None", default=api_settings.ALLOW_NONE)
    use_datetime = prompt("Use Datetime", default=api_settings.USE_DATETIME)
    storage_class = prompt("Storage Class", default=api_settings.defaults.get('STORAGE_CLASS'),
                           type=click.Choice(api_settings.defaults.get('DEFAULT_STORAGE_CLASSES')),
                           show_choices=True)

    creds = {
        'CLIENT_ID': client_id,
        'CLIENT_SECRET': client_secret,
        'REDIRECT_URL': redirect_url,
        'APP_NAME': app_name,
        'ALLOW_NONE': allow_none,
        'USE_DATETIME': use_datetime,
        'STORAGE_CLASS': storage_class,
    }

    if storage_class == JSON_STORAGE:
        creds['JSON_STORAGE_PATH'] = prompt("Token Storage File", default=api_settings.JSON_STORAGE_PATH,
                                            type=click.Path(readable=True, writable=True))

    save_to_file = prompt("Save settings to file?", default='y', type=click.BOOL, show_choices=True)

    if save_to_file:
        file = prompt("Save settings to file?", default=api_settings.CREDENTIALS_PATH, type=click.File("w", ))
        file.write(json.dumps(creds, indent=4))
    else:
        click.echo(creds)

    return creds


@cli.command()
@click.option('--credentials-file', '--f', type=click.File('r'), default=api_settings.CREDENTIALS_PATH,
              prompt="Path to Credentials File")
@click.pass_context
def get_access_token(ctx, credentials_file):
    """OAuth flow for Keap to obtain an access and refresh token"""
    try:
        creds = json.load(credentials_file)
    except Exception as e:
        return

    creds['APP_NAME'] = prompt("What app is being used?", type=click.STRING, default=creds['APP_NAME'])

    keap = Keap(
        config=creds
    )
    auth_url = keap.get_authorization_url()
    click.echo(f"Visit {auth_url}")
    response_url = prompt("Paste the return url here")
    query_string = dict(parse.parse_qsl(parse.urlsplit(response_url).query))
    code = query_string.get('code')
    if code:
        keap.request_access_token(code)

    if keap.token.access_token:
        if creds.get('STORAGE_CLASS') == IN_MEMORY_STORAGE:
            if prompt("You have chosen memory storage so nothing is saved here. Echo results?", default="y",
                      type=click.BOOL):
                click.echo(keap.token.__dict__)
            else:
                click.echo(f"Saved to {credentials_file}")


@cli.command()
@click.option('--credentials-file', '--cf', type=click.File("r"), default=api_settings.CREDENTIALS_PATH)
@click.option('--app', '--a', type=click.STRING, default='default')
def refresh_access_token(credentials_file, app):
    """Refresh Keap access token"""
    try:
        creds = json.load(credentials_file)
    except Exception as e:
        click.echo("Failed to load credentials file")
        return

    if app:
        creds['APP_NAME'] = app

    keap = Keap(
        config=creds
    )
    keap.refresh_access_token()


if __name__ == "__main__":
    cli()
