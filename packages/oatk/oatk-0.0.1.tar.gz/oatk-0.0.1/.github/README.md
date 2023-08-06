# OAuthToolKit

> A collection of useful functions for dealing with OAuth

[![Latest Version on PyPI](https://img.shields.io/pypi/v/oatk.svg)](https://pypi.python.org/pypi/oatk/)
[![Supported Implementations](https://img.shields.io/pypi/pyversions/oatk.svg)](https://pypi.python.org/pypi/oatk/)
[![Build Status](https://secure.travis-ci.org/christophevg/oatk.svg?branch=master)](http://travis-ci.org/christophevg/oatk)
[![Documentation Status](https://readthedocs.org/projects/oatk/badge/?version=latest)](https://oatk.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/christophevg/oatk/badge.svg?branch=master)](https://coveralls.io/github/christophevg/oatk?branch=master)
[![Built with PyPi Template](https://img.shields.io/badge/PyPi_Template-v0.2.0-blue.svg)](https://github.com/christophevg/pypi-template)



## Documentation

Minimal survival command...

```
% pip install oatk
```

Using it from the command line with a token in your clipboard (on MacOS)...

```console
  % oatk from_clipboard jwks jwks_uri-certs.json header  
  alg: RS256
  typ: JWT
  kid: deHeFbw74Qunnoq524B8FCeAB5tk_1LrEWuo8yseBuc
  % oatk from_clipboard jwks jwks_uri-certs.json show  
  exp:                1663771219
  iat:                1663770919
  jti:                74dfe057-88ff-4fae-ebc2-6e65ac3d463b
  iss:                https://login.company.com/auth/realms/TST
  sub:                cd521946-4c009688-298b-239d1-449e-5aa
  typ:                Bearer
  azp:                user
  acr:                1
  scope:              openid identification_type language alias_name email user_code action_codes permission_groups profile
  clientId:           user
  clientHost:         1.11.11.1
  identification:     simple
  email_verified:     false
  user_code:          user
  preferred_username: service-account-user
  clientAddress:      1.11.11.1
  % oatk from_clipboard jwks jwks_uri-certs.json validate
  True
```


