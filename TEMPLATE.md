# API‑Sprawl scan of {{ cidr }} — {{ ts }}

{% if not hosts %}
_No web services detected on ports {{ ports|join(', ') }}._
{% endif %}

{% for h in hosts %}
## {{ h.ip }}

| Port | Service | Product / Version |
|------|---------|-------------------|
{% for p in h.ports %}
| {{ p.port }} | {{ p.service }} | {{ p.product }} {{ p.version }} |
{% endfor %}

{% for p in h.ports if p.script %}
<details><summary>http-enum (port {{ p.port }})</summary>

{{ p.script }}

</details>

{% endfor %}
{% endfor %}