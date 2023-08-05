# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['purple_auth_client']
install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'python-jwt>=3.3.0,<4.0.0']

setup_kwargs = {
    'name': 'purple-auth-client',
    'version': '1.0.2',
    'description': 'Client library for Purple Auth',
    'long_description': '# Purple Auth Client\n\nAn async python client for my "Purple Auth" microservice.\n\n## Routes Covered\n\n### initialization\n\n```python\nfrom purple_auth_client import AuthClient\n\nauth_client = AuthClient(\n    host="https://purpleauth.com",\n    app_id="37f9a26d-03c8-4b7c-86ad-132bb82e8e38",\n    api_key="[Key provided by purple auth portal]"\n)\n```\n\n### /otp/request/\n\nStart otp authentication flow with server.\n\n```python\nresult = await auth_client.authenticate(\n    "test@example.com", flow="otp"\n)\n```\n\n### /otp/confirm/\n\nComplete authentication with email and generated code.\n\n```python\nresult = await auth_client.submit_code("test@example.com", "12345678")\n```\n\n### /token/verify/\n\nSend idToken to server for verification.\n\n```python\nresult = await auth_client.verify_token_remote(token_submitted_by_client)\n```\n\n### /token/refresh/\n\nRequest a new ID Token from the server using a refresh token\n\n```python\nnew_token = await auth_client.refresh(refresh_token_from_client)\n```\n\n\n### /app/\n\nGet more info about this app from the server.\n\n```python\ninfo = await auth_client.app_info()\n```\n\n\n### /magic/request/\n\nStart authentication using magic link flow.\n\n```python\nresult = await auth_client.authenticate(\n    "test@example.com", flow="magic"\n)\n```\n\n\n## Local Verification\n\nVerify and decode an ID Token on directly in the app without having to\ncall out every time\n\n```python\nresult = await auth_client.verify(id_token_from_client)\n# {"headers": {"alg": "ES256", "type": "JWT"}, "claims": {"sub": "user@email.com", "exp": "test@example.com"}\n# etc.\n\n```\n\n',
    'author': 'Rick Henry',
    'author_email': 'rickhenry@rickhenry.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
