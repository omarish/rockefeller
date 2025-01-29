import json
import os
import pickle
from typing import Optional

import google.auth.exceptions
import googleapiclient.discovery
import typer
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

app = typer.Typer(help="Commands related to Gmail.")

SCOPES = ["https://www.googleapis.com/auth/gmail.labels"]


def get_gmail_service(
    credentials_file: str = "credentials.json", token_file: str = "token.json"
):
    """
    Returns an authorized Gmail API client service instance, automatically prompting
    for OAuth authentication in a browser if there are no valid credentials.
    """

    creds = None

    # Load existing tokens if they exist
    if os.path.exists(token_file):
        with open(token_file, "rb") as token:
            creds = pickle.load(token)

    # If there are no valid credentials available, automatically prompt the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except google.auth.exceptions.RefreshError:
                creds = None
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            # Explicitly open the user’s default browser
            creds = flow.run_local_server(port=0, open_browser=True)

        # Save the credentials for the next run
        with open(token_file, "wb") as token:
            pickle.dump(creds, token)

    service = googleapiclient.discovery.build("gmail", "v1", credentials=creds)
    return service


def upsert_gmail_labels(service, user_id: str, labels_data: list):
    """
    Upsert each label from labels_data for the given user_id.
    - If label exists (by name), update it.
    - If it doesn't exist, create it.
    """
    existing_labels_response = service.users().labels().list(userId=user_id).execute()
    existing_labels = existing_labels_response.get("labels", [])
    existing_labels_map = {label["name"]: label["id"] for label in existing_labels}

    for label_def in labels_data:
        label_name = label_def.get("name")
        if not label_name:
            typer.echo("Skipping a label without 'name' field.")
            continue

        label_body = {
            "name": label_name,
            "color": label_def.get("color"),
            "messageListVisibility": label_def.get("messageListVisibility", "show"),
            "labelListVisibility": label_def.get("labelListVisibility", "labelShow"),
        }

        if label_name in existing_labels_map:
            label_id = existing_labels_map[label_name]
            typer.echo(f"Updating label '{label_name}' (ID: {label_id})")
            service.users().labels().update(
                userId=user_id, id=label_id, body=label_body
            ).execute()
        else:
            typer.echo(f"Creating label '{label_name}'")
            service.users().labels().create(userId=user_id, body=label_body).execute()


@app.command("upsert-labels")
def upsert_labels(
    email: str = typer.Argument(..., help="The Gmail address to operate on."),
    from_file: Optional[str] = typer.Option(
        None, "--from-file", "-f", help="Path to the JSON labels file."
    ),
    credentials_file: str = typer.Option(
        "credentials.json", "--credentials-file", help="Path to your OAuth2 creds."
    ),
    token_file: str = typer.Option(
        "token.json", "--token-file", help="Path to store your OAuth tokens."
    ),
):
    """
    Upsert labels for the specified Gmail account.
    Automatically prompts for authentication if no valid credentials are found.
    """
    import os

    # Convert from_file into an absolute path
    if from_file:
        from_file = os.path.expanduser(from_file)
        from_file = os.path.abspath(from_file)

    # Check that the file exists
    if not from_file or not os.path.exists(from_file):
        typer.echo("You must specify a valid --from-file path to a JSON file.")
        raise typer.Exit(code=1)

    with open(from_file, "r") as f:
        labels_data = json.load(f)

    service = get_gmail_service(
        credentials_file=credentials_file, token_file=token_file
    )
    upsert_gmail_labels(service, email, labels_data)
    typer.echo("Done upserting labels.")
