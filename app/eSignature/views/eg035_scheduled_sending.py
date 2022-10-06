
""" Example 035: Scheduled sending and delayed routing """

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint, request

from ..examples.eg035_scheduled_sending import Eg035ScheduledSendingController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import pattern

example_number = 35
eg = f"eg0{example_number}"  # reference (and url) for this example
eg035 = Blueprint(eg, __name__)

def get_args():
    """Get request and session arguments"""

    # More data validation would be a good idea here
    # Strip anything other than characters listed
    signer_email = pattern.sub("", request.form.get("signer_email"))
    signer_name = pattern.sub("", request.form.get("signer_name"))
    resume_date = request.form.get("resume_date")
    envelope_args = {
        "signer_email": signer_email,
        "signer_name": signer_name,
        "resume_date": resume_date,
        "status": "sent",
    }
    args = {
        "account_id": session["ds_account_id"],
        "base_path": session["ds_base_path"],
        "access_token": session["ds_access_token"],
        "envelope_args": envelope_args
    }
    return args

@eg035.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["esign_manifest_url"])
@authenticate(eg=eg)
def sign_by_email():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response with envelopeId
    """
    example = get_example_by_number(session["manifest"], example_number)

    # 1. Get required arguments
    args = get_args()
    try:
        # 1. Call the worker method
        results = Eg035ScheduledSendingController.worker(args)
        print(results)
    except ApiException as err:
        return process_error(err)

    # 2. Render success response with envelopeId
    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message=f"The envelope has been created and scheduled!<br/>Envelope ID: {results['envelope_id']}."
    )


@eg035.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["esign_manifest_url"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number)

    return render_template(
        "eg035_scheduled_sending.html",
        title=example["ExampleName"],
        example=example,
        source_file="eg035_scheduled_sending.py",
        source_url=DS_CONFIG["github_example_url"] + "eg035_scheduled_sending.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )
