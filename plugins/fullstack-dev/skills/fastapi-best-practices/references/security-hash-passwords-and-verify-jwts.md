---
title: Hash Passwords and Verify JWTs Strictly
impact: CRITICAL
tags: security, passwords, jwt
---

## Hash Passwords and Verify JWTs Strictly

Use a maintained password-hashing library, store only hashes, keep signing keys outside source, fix
the accepted JWT algorithms, and validate expiry and required claims.

**Incorrect:**

```python
def store_password(password: str) -> str:
    return password
```

**Correct:**

```python
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def store_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, stored_hash: str) -> bool:
    return password_hash.verify(password, stored_hash)
```

**Compatibility:** Follow the installed JWT library's verification API; never derive accepted algorithms from a token.

References:

- [FastAPI: OAuth2 with Password and JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [OWASP: Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

