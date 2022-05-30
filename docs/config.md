If you've come here looking for a config template, copy the one below
into your `config.cfg` file, and modify it appropriately.

It does not support inline comments, so if you do `api_key = 'foo' # comment`, it will think that your API
key is `'foo' # comment`.
It also does not support `''` or `""`, so keep your strings bare.

```
# Example Configuration Template
api_key = abcd1234
telegram_secret = abcd1234
telegram_id = 1234567890
useragent = A clever and descriptive useragent, explaining who you are
# It is suggested to include your main nation name, and your email.

# Campaign Configuration
campaign_file = /path/to/campaigns.json
```