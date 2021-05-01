# [Let's Encrypt](http://letsencrypt.hive.pt)

Simple Let’s Encrypt service for validation implementing the ACME validation process as defines by [RFC 8555](https://datatracker.ietf.org/doc/rfc8555/)

## Inspiration

There are multiple implementation of ACME for multiple programming languages.

A full list of client implementations can be checked [here](https://letsencrypt.org/docs/client-options/).

## Configuration

| Name        | Type  | Default            | Description                                                                          |
| ----------- | ----- | ------------------ | ------------------------------------------------------------------------------------ |
| **LE_PATH** | `str` | `/etc/letsencrypt` | The path to the directory where the Let’s Encrypt data files are going to be stored. |

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
    auth --standalone --preferred-challenges http-01 --domains letsencrypt-test.ngrok.io
```
