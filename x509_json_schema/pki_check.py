import json
import sys
import os
import argparse
from datetime import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID, ExtensionOID
import jsonschema

def load_certificate(path):
    with open(path, 'rb') as f:
        cert_data = f.read()
    try:
        # Try loading as PEM-formatted certificate
        cert = x509.load_pem_x509_certificate(cert_data, default_backend())
    except ValueError:
        # Otherwise, try DER
        cert = x509.load_der_x509_certificate(cert_data, default_backend())
    return cert

def cert_to_dict(cert):
    # Extract issuer as a string
    issuer = cert.issuer.rfc4514_string()
    # Extract validity dates in ISO format
    valid_from = cert.not_valid_before.isoformat()
    valid_to = cert.not_valid_after.isoformat()
    # Extract subject information
    common_name = None
    organization = None
    for attribute in cert.subject:
        if attribute.oid == NameOID.COMMON_NAME:
            common_name = attribute.value
        elif attribute.oid == NameOID.ORGANIZATION_NAME:
            organization = attribute.value
    subject = {
        "commonName": common_name,
        "organization": organization
    }
    # Extract the basicConstraints extension (if available)
    try:
        basic_constraints = cert.extensions.get_extension_for_oid(ExtensionOID.BASIC_CONSTRAINTS).value
        basic_constraints_dict = {"ca": basic_constraints.ca}
    except x509.ExtensionNotFound:
        basic_constraints_dict = {"ca": False}
    return {
        "issuer": issuer,
        "validFrom": valid_from,
        "validTo": valid_to,
        "subject": subject,
        "extensions": {
            "basicConstraints": basic_constraints_dict
        }
    }

def load_schema(path=None):
    # If a specific path is not provided, load the schema from package data.
    if path is None:
        base_path = os.path.dirname(__file__)
        path = os.path.join(base_path, 'x509-schema.json')
    with open(path, 'r') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description='Validate certificate against a JSON schema.')
    parser.add_argument('certfile', help='Path to the certificate file (CER format).')
    parser.add_argument('--output', '-o', help='Optional output file to save JSON representation of the certificate.')
    args = parser.parse_args()

    cert = load_certificate(args.certfile)
    cert_json = cert_to_dict(cert)
    schema = load_schema()  # load schema from package data

    try:
        jsonschema.validate(instance=cert_json, schema=schema)
        print("Certificate is valid according to the JSON schema.")
    except jsonschema.ValidationError as e:
        print("Validation error:", e.message)
        sys.exit(1)

    if args.output:
        with open(args.output, 'w') as out_file:
            json.dump(cert_json, out_file, indent=4)
        print(f"Certificate JSON representation saved to {args.output}")

if __name__ == "__main__":
    main()