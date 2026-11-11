# kayenn.org – website

A static page (`site/`) served by nginx in Docker, **behind Nginx Proxy Manager** (NPM), which handles the domain,
HTTPS and the Let's Encrypt certificate.

## Setup

1. **Copy this folder** to the server.
2. **Find the Docker network of NPM:** `docker network ls` (often `npm_default`, or the name of the NPM
   project followed by `_default`). If it is not `npm_default`, create a `.env` file next to the compose file:
   ```
   NPM_NETWORK=name_of_the_network
   ```
   (alternatively attach NPM to the network created by this compose, or publish a port – see below).
3. **Start:** `docker compose up -d` (check: `docker compose ps`).
4. **DNS** at the registrar of kayenn.org: `A` records for `@` and `www` → the public IP of your home connection
   (dynamic IP → DDNS). The router already forwards 80/443 to NPM.
5. **In NPM → Hosts → Proxy Hosts → Add Proxy Host:**
   - *Domain Names:* `kayenn.org`, `www.kayenn.org`
   - *Scheme:* `http`, *Forward Hostname / IP:* `kayenn-web`, *Forward Port:* `80`
   - enable *Block Common Exploits*
   - tab **SSL:** *Request a new SSL Certificate*, enable *Force SSL*, *HTTP/2 Support*, *HSTS Enabled*
     and accept the Let's Encrypt terms.
6. Redirect `www` → the bare domain (optional): Hosts → **Redirection Hosts** → `www.kayenn.org` →
   `https://kayenn.org` (with its own certificate) – and remove `www` from the proxy host.

Open <https://kayenn.org>.

### If NPM and this container cannot share a network

Add to the `web` service `ports: ["8081:80"]`, remove the `networks` section, and in NPM forward to the
server's LAN address and port 8081 (e.g. `192.168.1.10:8081`). Do not forward 8081 on the router.

## Updating

The server folder `kayenn` is a sparse clone of the repository (only `website/`):

```
git clone --filter=blob:none --sparse https://github.com/damiankozuszek/kayenn.git kayenn
cd kayenn && git sparse-checkout set website
cd website && docker compose up -d        # .env (NPM_NETWORK) stays only on the server
```

A cron job pulls the changes (`crontab -e`):

```
*/5 * * * * cd /full/path/kayenn && git pull -q
```

The page is in English (`site/index.html`, the default) and Polish (`site/pl/index.html`); both share
`site/style.css` and the images in `site/img/` – change the content of both pages together. The PL / EN link
remembers the visitor's choice (localStorage). The page has its own dark theme (`prefers-color-scheme`,
`color-scheme: light dark` – browsers do not darken it themselves); the wordmark keeps its colours.

So: edit `site/` in the repository, commit and push – the page is live within 5 minutes (nginx serves the
files at once, no restart). After a change of `nginx.conf`: `docker compose restart` in `kayenn/website`.
New nginx image: `docker compose pull && docker compose up -d`.

## Notes

- Only the static page is exposed; files are mounted read-only.
- The page loads nothing from third parties except the GitHub API call for the latest version number
  (it works without it).
- The security headers are set in `nginx.conf` (Content-Security-Policy etc.); do not duplicate them in the
  NPM *Advanced* tab.
