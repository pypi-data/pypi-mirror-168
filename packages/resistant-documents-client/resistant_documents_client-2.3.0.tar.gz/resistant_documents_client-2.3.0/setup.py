# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['resistant_documents_client', 'resistant_documents_client.tests']

package_data = \
{'': ['*']}

install_requires = \
['requests-oauthlib>=1.3.0,<2.0.0', 'requests>=2.22.0,<3.0.0']

setup_kwargs = {
    'name': 'resistant-documents-client',
    'version': '2.3.0',
    'description': 'Resistant.ai document forjerry python client for convenient integration with REST API service.',
    'long_description': '# Resistant documents client\n\nThis library provides a Python client for a [Resistant.ai document forgery analysis service](https://resistant.ai/products/documents/).\nFor a detailed description of the API please see [API reference docs](https://documents.testing.resistant.ai/docs/v2.html).\n\n## Prerequisites\n\nDuring the customer onboarding process, you should be provided with the following:\n\n- CLIENT_ID : str\n- CLIENT_SECRET : str\n\nNote: Those credentials are connected with specific environment (e.g. test, production etc.). Together with secret credentials for \nnon-production environment you should be provided with url links:\n- api_url\n- token_url\n\n## Basic usage\n\nSubmit a document for analysis with default pipeline configuration.\n\n```python\nfrom resistant_documents_client.client import ResistantDocumentsClient\n\nclient = ResistantDocumentsClient(client_id="CLIENT_ID", client_secret="CLIENT_SECRET")\nwith open("local_file.pdf", "rb") as fp:\n    report = client.analyze(fp.read(), query_id="local_file.pdf")\nprint(report["score"])\n``` \nFor non-production environment, provide `api_url` and `token_url` provided together with client secrets to client creation (`ResistantDocumentsClient`).\n\n## Customized usage\n\nSubmit a document for analysis with customized process parameters or select a different type of analysis. \n\n### Step 1: Create a client with your credentials\n\n```python\nclient = ResistantDocumentsClient(client_id="CLIENT_ID", client_secret="CLIENT_SECRET")\n```\n\nNote: If your client secrets are for different environment than production you have to provide following `api_url` `token_url`. To setup proxy server URL, you can provide optional `proxy`.\n\n### Step 2: Create submission with pipeline setup\n\n```python\nwith open("local_file.pdf", "rb") as fp:\n    my_submission_id = client.submit(fp.read(), query_id="local_file.pdf", pipeline_configuration="CONTENT_AFTER_FRAUD_AFTER_QUALITY")\n```\n\nPossible pipeline configurations are listed in [REST API docs](https://documents.testing.resistant.ai/docs/v2-preview.html#operation/createSubmission)\n\n### Step 3: Retrieve analysis result\nYou can retrieve only those types of analysis which were requested in the previous step as `pipeline_configuration` option.\n\n```python\nresult_content = client.content(submission_id=submission_id)\nresult_fraud = client.content(submission_id=submission_id)\nresult_quality = client.quality(submission_id=submission_id)\n\nprint(result_content)\nprint(result_fraud)\nprint(result_quality)\n```\nThese methods also accept `max_num_retries`, which represents how many times the client will poll the server before failing (because the communication is asynchronous). It might be customized but has a default\nvalue. Other parameters correspond to the ones in the REST API docs.',
    'author': 'Resistant.ai',
    'author_email': 'sales@resistant.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
