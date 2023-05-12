# User Auth Services

## Description

This service is used to authenticate users and to provide a session token for the user to use in subsequent requests.

## Usage

### Authenticate User

#### Request

```json
{
  "method": "POST",
  "path": "/user/authenticate",
  "headers": {
	"Content-Type": "application/json"
  },
  "body": {
	"username": "user",
	"password": "password"
  }
}
```

