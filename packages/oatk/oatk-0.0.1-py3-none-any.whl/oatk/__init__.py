__version__ = "0.0.1"

import logging
logger = logging.getLogger(__name__)

import jwt
import json

try:
  from AppKit import NSPasteboard, NSStringPboardType
  pb = NSPasteboard.generalPasteboard()
except ModuleNotFoundError:
  logger.debug("No AppKit installed, so no MacOS clipboard support!")
  pb = None


class OAuthToolkit():
  """
  % python -m oatk from_clipboard jwks jwks_uri-certs.json header  
  alg: RS256
  typ: JWT
  kid: deHeFbw74Qunnoq524B8FCeAB5tk_1LrEWuo8yseBuc
  % python -m oatk from_clipboard jwks jwks_uri-certs.json show  
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
  % python -m oatk from_clipboard jwks jwks_uri-certs.json validate
  True
  """

  def __init__(self):
    self._encoded = None
    self._certs   = {}

  @property
  def version(self):
    return __version__

  def jwks(self, path):
    with open(path) as fp:
      jwks = json.load(fp)
    for jwk in jwks["keys"]:
      kid = jwk['kid']
      logger.debug(f"🔑 loading {kid}")
      self._certs[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
    return self
  
  def from_clipboard(self):
    encoded = pb.stringForType_(NSStringPboardType)
    if encoded[:6] == "Bearer":
      encoded = clip[7:]
    self._encoded = encoded
    return self

  def header(self):
    return jwt.get_unverified_header(self._encoded)

  def show(self):
    alg = self.header()["alg"]
    return jwt.decode(
      self._encoded,
      options={"verify_signature": False},
      algorithms=[alg]
    )

  def validate(self):
    kid = self.header()["kid"]
    alg = self.header()["alg"]
    logger.debug(f"🔑 using {kid}")
    try:
      jwt.decode(
        self._encoded,
        self._certs[kid],
        algorithms=[alg]
      )
    except jwt.exceptions.ExpiredSignatureError:
      logger.error("token has expired")
      return False
    return True
