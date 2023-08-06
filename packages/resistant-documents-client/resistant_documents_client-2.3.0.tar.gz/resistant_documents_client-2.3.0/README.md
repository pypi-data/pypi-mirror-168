# Resistant documents client

This library provides a Python client for a [Resistant.ai document forgery analysis service](https://resistant.ai/products/documents/).
For a detailed description of the API please see [API reference docs](https://documents.testing.resistant.ai/docs/v2.html).

## Prerequisites

During the customer onboarding process, you should be provided with the following:

- CLIENT_ID : str
- CLIENT_SECRET : str

Note: Those credentials are connected with specific environment (e.g. test, production etc.). Together with secret credentials for 
non-production environment you should be provided with url links:
- api_url
- token_url

## Basic usage

Submit a document for analysis with default pipeline configuration.

```python
from resistant_documents_client.client import ResistantDocumentsClient

client = ResistantDocumentsClient(client_id="CLIENT_ID", client_secret="CLIENT_SECRET")
with open("local_file.pdf", "rb") as fp:
    report = client.analyze(fp.read(), query_id="local_file.pdf")
print(report["score"])
``` 
For non-production environment, provide `api_url` and `token_url` provided together with client secrets to client creation (`ResistantDocumentsClient`).

## Customized usage

Submit a document for analysis with customized process parameters or select a different type of analysis. 

### Step 1: Create a client with your credentials

```python
client = ResistantDocumentsClient(client_id="CLIENT_ID", client_secret="CLIENT_SECRET")
```

Note: If your client secrets are for different environment than production you have to provide following `api_url` `token_url`. To setup proxy server URL, you can provide optional `proxy`.

### Step 2: Create submission with pipeline setup

```python
with open("local_file.pdf", "rb") as fp:
    my_submission_id = client.submit(fp.read(), query_id="local_file.pdf", pipeline_configuration="CONTENT_AFTER_FRAUD_AFTER_QUALITY")
```

Possible pipeline configurations are listed in [REST API docs](https://documents.testing.resistant.ai/docs/v2-preview.html#operation/createSubmission)

### Step 3: Retrieve analysis result
You can retrieve only those types of analysis which were requested in the previous step as `pipeline_configuration` option.

```python
result_content = client.content(submission_id=submission_id)
result_fraud = client.content(submission_id=submission_id)
result_quality = client.quality(submission_id=submission_id)

print(result_content)
print(result_fraud)
print(result_quality)
```
These methods also accept `max_num_retries`, which represents how many times the client will poll the server before failing (because the communication is asynchronous). It might be customized but has a default
value. Other parameters correspond to the ones in the REST API docs.