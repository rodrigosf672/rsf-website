<?xml version="1.0" encoding="UTF-8"?>
<!--
  Human-friendly rendering of rss.xml. Browsers apply this stylesheet when a
  person opens /rss.xml; feed readers ignore it and parse the XML directly, so
  the feed stays valid RSS 2.0. Kept self-contained (inline CSS) on purpose.
-->
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:atom="http://www.w3.org/2005/Atom"
  xmlns:dc="http://purl.org/dc/elements/1.1/">
  <xsl:output method="html" encoding="UTF-8" indent="yes" doctype-system="about:legacy-compat"/>

  <xsl:template match="/rss/channel">
    <html lang="en">
      <head>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <title><xsl:value-of select="title"/> · RSS feed</title>
        <style>
          :root {
            --bg:#0a0e16; --raised:#101624; --border:#1e2637; --text:#e8ecf4;
            --muted:#98a2b8; --faint:#6b7690; --moss:#54d148; --pine:#1e3d2f;
            --mono:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
            --sans:"Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
          }
          @media (prefers-color-scheme: light) {
            :root { --bg:#f7f8fa; --raised:#fff; --border:#e0e5ed; --text:#182033;
                    --muted:#505b72; --faint:#7a849b; --moss:#2e7d1f; }
          }
          * { box-sizing:border-box; }
          body { margin:0; background:var(--bg); color:var(--text);
                 font-family:var(--sans); line-height:1.6; -webkit-font-smoothing:antialiased; }
          .wrap { max-width:44rem; margin:0 auto; padding:2.5rem 1.25rem 4rem; }
          .kicker { font-family:var(--mono); font-size:.72rem; letter-spacing:.18em;
                    text-transform:uppercase; color:var(--moss); }
          h1 { font-size:1.9rem; font-weight:800; margin:.4rem 0 .3rem; line-height:1.2; }
          .desc { color:var(--muted); margin:0 0 1.5rem; }
          .subscribe { background:linear-gradient(135deg,var(--pine),#2e5d24);
                       border-radius:12px; padding:16px 18px; margin-bottom:2rem; }
          .subscribe p { margin:0 0 .6rem; color:#dff0d5; font-size:.95rem; }
          .subscribe code { display:block; font-family:var(--mono); font-size:.85rem;
                            background:rgba(0,0,0,.28); color:#9fd48a; padding:9px 12px;
                            border-radius:8px; word-break:break-all; }
          h2 { font-family:var(--mono); font-size:.8rem; letter-spacing:.1em;
               text-transform:uppercase; color:var(--faint); margin:2rem 0 .5rem; }
          article { border-top:1px solid var(--border); padding:1.1rem 0; }
          .pt { font-size:1.12rem; font-weight:700; color:var(--text); text-decoration:none; }
          .pt:hover { color:var(--moss); }
          .meta { font-family:var(--mono); font-size:.75rem; color:var(--faint); margin:.2rem 0 .5rem; }
          article p { color:var(--muted); margin:0 0 .6rem; font-size:.95rem; }
          .cat { display:inline-block; font-family:var(--mono); font-size:.7rem;
                 color:var(--moss); border:1px solid var(--border); border-radius:99px;
                 padding:2px 10px; margin-right:6px; }
          footer { margin-top:2.5rem; border-top:1px solid var(--border); padding-top:1.25rem;
                   font-family:var(--mono); font-size:.82rem; color:var(--faint); }
          footer a { color:var(--moss); text-decoration:none; }
        </style>
      </head>
      <body>
        <div class="wrap">
          <div class="kicker">RSS feed</div>
          <h1><xsl:value-of select="title"/></h1>
          <p class="desc"><xsl:value-of select="description"/></p>

          <div class="subscribe">
            <p>You are looking at an RSS feed. Paste this address into your feed reader
               (NetNewswire, Feedly, Inoreader, Thunderbird, …) to get new posts automatically:</p>
            <code><xsl:value-of select="atom:link/@href"/></code>
          </div>

          <h2>Latest posts</h2>
          <xsl:for-each select="item">
            <article>
              <a class="pt" href="{link}"><xsl:value-of select="title"/></a>
              <div class="meta"><xsl:value-of select="pubDate"/></div>
              <p><xsl:value-of select="description"/></p>
              <div>
                <xsl:for-each select="category">
                  <span class="cat"><xsl:value-of select="."/></span>
                </xsl:for-each>
              </div>
            </article>
          </xsl:for-each>

          <footer>
            <xsl:text>Back to </xsl:text><a href="/blog/">the blog</a>
            <xsl:text> · </xsl:text><a href="/">rodrigosf.com</a>
          </footer>
        </div>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
