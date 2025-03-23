# An JSON Schema for X.509 certificates

JSON Schema plays a critical role in ensuring that JSON data complies with predefined standards and rules. As organizations increasingly rely on JSON for data interchange, establishing a clear, machine-readable contract for data structures becomes essential for maintaining consistency, accuracy, and interoperability between systems.

JSON Schema allows developers to define and enforce the expected format, data types, and constraints of JSON documents. This not only enables effective validation and error handling but also aids in documentation and future-proofing applications as business requirements evolve. By using JSON Schema for compliance validation, organizations can streamline data governance, reduce integration issues, and ensure that all data exchanges meet necessary compliance standards.

You can validate digital certificates compliance using JSON Schema by representing the key certificate attributes—like issuer, validity period, subject details, and extensions—as a JSON object. Then, you define a JSON Schema that prescribes the expected structure, data types, and constraints. You can feed your extracted certificate data into a JSON Schema validator to confirm that the certificate meets all defined compliance rules.

To use this work in practice, you would simply extract the certificate details into a JSON object, validate the JSON object against the proposed schema using a validator library (for instance, Ajv in JavaScript or jsonschema in Python) and finally use the validation results to enforce compliance rules. This approach ensures that digital certificates are programmatically verified for consistency with the expected compliance format.

## Explanation of the Schema

The proposed schema is quite simple and focuses on the core definitions for X.509 certificates. Here's the main elements of the schema that are of interest to better understand its usage and how to extend it, if needed:

* $schema: Specifies the JSON Schema draft used.
* title and description: Provide human-readable information about the schema.
* type: Defines the data type for the schema (object).
* properties: Lists the various fields within an X.509 certificate.
  * version: Integer representing the X.509 version.
  * serialNumber: A unique identifier for the certificate.
  * issuer and subject: Distinguished Names (DNs) of the issuer and subject.
    * Includes fields for country (using the ISO 3166 standard), organization, organizational unit, and common name.
  * validity: Period during which the certificate is valid.
    * Uses date-time format for notBefore and notAfter.
  * publicKeyInfo: Details the public key algorithm and parameters.
    * algorithm is an enumeration of the allowed algorithms in the document.
  * signatureAlgorithm: Algorithm used to sign the certificate.
  * extensions: An array of certificate extensions.
    * Each extension includes its OID, criticality flag, and value (represented as a DER-encoded string).
* required: Specifies the mandatory fields for a valid X.509 certificate.

## Examples of X.509 Certificates in JSON

Here are a few examples of X.509 certificates represented in JSON format, based on the generic certificate profiles.

### Example 1: Root CA Certificate

```json
{
  "version": 3,
  "serialNumber": "12345",
  "issuer": {
    "country": "US",
    "organization": "Organization",
    "organizationalUnit": "Root CA01",
    "commonName": "Organization Root Certification Authority"
  },
  "subject": {
    "country": "US",
    "organization": "Organization",
    "organizationalUnit": "Root CA01",
    "commonName": "Organization Root Certification Authority"
  },
  "validity": {
    "notBefore": "2024-02-21T00:00:00Z",
    "notAfter": "2074-02-21T00:00:00Z"
  },
  "publicKeyInfo": {
    "algorithm": "RSA",
    "keyLength": 4096,
    "parameters": "NONE"
  },
  "signatureAlgorithm": "Sha512WithRSAEncryption",
  "extensions": [
    {
      "oid": "2.5.29.15",
      "critical": true,
      "value": "03020780"
    },
    {
      "oid": "2.5.29.19",
      "critical": true,
      "value": "30060101ff020100"
    },
    {
      "oid": "2.5.29.14",
      "critical": false,
      "value": "0414..."
    }
  ]
}
```


### Example 2: Device CA Certificate

```json
{
  "version": 3,
  "serialNumber": "67890",
  "issuer": {
    "country": "US",
    "organization": "Organization",
    "organizationalUnit": "Root CA01",
    "commonName": "Organization Root Certification Authority"
  },
  "subject": {
    "country": "US",
    "organization": "Organization",
    "organizationalUnit": "Device CA01",
    "commonName": "Organization Device Certification Authority"
  },
  "validity": {
    "notBefore": "2024-02-21T00:00:00Z",
    "notAfter": "2054-02-21T00:00:00Z"
  },
  "publicKeyInfo": {
    "algorithm": "RSA",
    "keyLength": 2048,
    "parameters": "NONE"
  },
  "signatureAlgorithm": "Sha256WithRSAEncryption",
  "extensions": [
    {
      "oid": "2.5.29.15",
      "critical": true,
      "value": "03020780"
    },
    {
      "oid": "2.5.29.19",
      "critical": true,
      "value": "30060101ff020100"
    },
    {
      "oid": "2.5.29.14",
      "critical": false,
      "value": "0414..."
    },
    {
      "oid": "2.5.29.35",
      "critical": false,
      "value": "0414..."
    }
  ]
}
```


### Example 3: Code Verification Certificate

```json
{
  "version": 3,
  "serialNumber": "11223",
  "issuer": {
    "country": "US",
    "organization": "Organization",
    "organizationalUnit": "CVC CA01",
    "commonName": "Organization CVC Certification Authority"
  },
  "subject": {
    "country": "US",
    "organization": "Example Company",
    "organizationalUnit": "DPoE",
    "commonName": "Code Verification Certificate"
  },
  "validity": {
    "notBefore": "2024-02-21T00:00:00Z",
    "notAfter": "2034-02-21T00:00:00Z"
  },
  "publicKeyInfo": {
    "algorithm": "RSA",
    "keyLength": 2048,
    "parameters": "NONE"
  },
  "signatureAlgorithm": "Sha256WithRSAEncryption",
  "extensions": [
    {
      "oid": "2.5.29.37",
      "critical": true,
      "value": "300906052b0e03021a0500"
    },
    {
      "oid": "2.5.29.35",
      "critical": false,
      "value": "0414..."
    },
    {
       "oid": "2.5.29.15",
       "critical": false,
       "value": "03020080"
    }
  ]
}
```


## Notes on Examples

The value fields in the extensions array are placeholders. In a real-world scenario, these would contain the DER-encoded values of the respective extensions. These examples are based on the profiles for Root CA, Device CA, and Code Verification certificates.

This schema and the examples should give you a solid foundation for working with X.509 certificates in JSON format.
