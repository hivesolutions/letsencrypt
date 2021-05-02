# [Let's Encrypt](http://letsencrypt.hive.pt)

Simple Let’s Encrypt service for validation implementing the ACME validation process as defines by [RFC 8555](https://datatracker.ietf.org/doc/rfc8555/)

## Inspiration

There are multiple implementation of ACME for multiple programming languages.

A full list of client implementations can be checked [here](https://letsencrypt.org/docs/client-options/).

## Configuration

| Name             | Type  | Default                        | Description                                                                                         |
| ---------------- | ----- | ------------------------------ | --------------------------------------------------------------------------------------------------- |
| **MODE**         | `str` | `standalone`                   | The execution mode to be used when handling "wellknown" routes (eg: `standalone`, `webroot`, etc.). |
| **LE_PATH**      | `str` | `/etc/letsencrypt`             | The path to the directory where the Let’s Encrypt data files are going to be stored.                |
| **WEBROOT_PATH** | `str` | `/var/lib/letsencrypt/webroot` | The path to the "webroot" directory where the "wellknown" files should be stored.                   |

## Example

Assuming that the location for the data files is `/data/letsencrypt`.

To be able to test the certificate generation process just go ahead and create an ngrok tunnel using:

```bash
ngrok http 8080 -hostname=letsencrypt-test.ngrok.io
```

Then try to issue a certificate for that same domain using:

```bash
docker run \
    -i -t --rm \
    --name letsencrypt-sign \
    -v /data/letsencrypt/etc:/etc/letsencrypt \
    -v /data/letsencrypt/var:/var/lib/letsencrypt \
    certbot/certbot:v0.31.0 \
    auth \
    --standalone \
    --register-unsafely-without-email \
    --preferred-challenges http-01 \
    --domains letsencrypt-test.ngrok.io
```

If you want to use the webroot version for testing use instead:

```bash
docker run \
    -i -t --rm \
    --name letsencrypt-sign \
    -v /data/letsencrypt/etc:/etc/letsencrypt \
    -v /data/letsencrypt/var:/var/lib/letsencrypt \
    certbot/certbot:v0.31.0 \
    auth \
    --webroot -w /var/lib/letsencrypt/webroot \
    --register-unsafely-without-email \
    --preferred-challenges http-01 \
    --domains letsencrypt-test.ngrok.io
```
