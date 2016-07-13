# strava-mv

On a random boring Friday evening I ended up writing this thing that I
was thinking of for a while - tired of renaming and tagging my commutes
on Strava all the time, I've written a script that will do most of it
for me.

Looking around, I noticed nothing like this existed and there did seem
to be some people looking for ways to change the standard names, etc.
Throw this script into your crontab to get just that.

## How?

Update the script to whatever makes sense to me. Config and code are
mixed because I couldn't be bothered to do that part the right way since
I don't expect this to pick up many or any users. :-)

The `build_updates()` functions gets fed a full stravalib `Activity`
object. Inspect it all you want, see my current implementation for
examples of what you can do. Then fill a hash with updates you'd like to
apply (using `[update_activity](https://github.com/hozn/stravalib/blob/master/stravalib/client.py)`
arguments as keys) and return it. Done.

To start using it, just run `login.py` once first to create your
`access_token` file, then you're done.
