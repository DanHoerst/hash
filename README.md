Usage:

Build docker:

```
docker build -t dhoerst/hash:v1.0 .
```

Run docker:

```
docker run -it -p 443:443 hash:v1.0
```

Post to app:

```
(hash)DAN:hash dhoerst$ curl -X POST -k -H "Content-Type: application/json" -d '{"message": "foo"}' https://localhost/messages
{
  "digest": "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae"
}

```

Retrive from app:

```
(hash)DAN:hash dhoerst$ curl -k https://localhost/messages/2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae
{
  "meesage": "foo"
}

```

If the hash doesn't exist, 404:

```
(hash)DAN:hash dhoerst$ curl -i -k https://localhost/messages/aaaaaaaaaaaaaaaaaaaaaaaaaaaaa
HTTP/1.0 404 NOT FOUND
Content-Type: text/html
Content-Length: 233
Server: Werkzeug/0.11.15 Python/2.7.13
Date: Fri, 24 Feb 2017 00:37:58 GMT

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.</p>
```
