# Global Entry Notifier
This application can be setup to notify you via text whenever a new Global Entry appointment becomes available at your chosen interview location.

[Twilio](https://www.twilio.com/) is used to send SMS notifications. Signing up for a new account should provide you with a small starting balance that should be more than enough to cover the SMS notifications

```bash
pip install global-entry-notifier
```

# Single run
After install, run the notifier to confirm you successfully receive a text message:

```bash
global-entry-notifier \
    -l 5003 \
    -p <YOUR_PHONE_NUMBER> \
    --twilio-number <TWILIO_PHONE_NUMBER> \
    --twilio-sid <TWILIO_ACCOUNT_SID> \
    --twilio-token <TWILIO_AUTHENTICATION_TOKEN>
```

NOTES:
* Country codes are `required` on all phone numbers
  * e.g If your phone number is `1234567890` and you live in the U.S, pass in `+11234567890`
* The location `5003` seems to always have available slots so it's great for testing. If that doesn't work, try `5004`

# Locations
You can view the full list of interview locations by running:

```bash
global-entry-locations
```

To narrow down the search, you can filter the results using the `-n, --name` and `-s, --state` arguments:

```bash
global-entry-locations -s tx
global-entry-locations -s tx -n laredo
```


# Schedule availability checks with cron (Linux/MacOS)
Scheduling this application via cron is probably the easiest method to start performing automatic appointment availability checks

NOTE: cron requires the full path to the application's entry point. Retrieve the path with:

```bash
which global-entry-notifier
```

Checking once per hour is likely sufficient:

```crontab
0 */1 * * * /home/<USER>/.local/bin/global-entry-notifier -l <LOCATION> -p <YOUR_PHONE_NUMBER> --twilio-number <TWILIO_PHONE_NUMBER> --twilio-sid <TWILIO_ACCOUNT_SID> --twilio-token <TWILIO_AUTHENTICATION_TOKEN>
```

# Miscellaneous
Display the help menu:

```bash
global-entry-notifier -h
global-entry-notifier --help

global-entry-locations -h
global-entry-locations --help
```

Display the version:

```bash
global-entry-notifier -V
global-entry-notifier --version

global-entry-locations -V
global-entry-locations --version
```
