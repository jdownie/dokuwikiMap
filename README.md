# dokuwikiMap

Small web app to help visualise a wiki's existing layout.

This is a quick and dirty way to get a "birds eye view" of an existing [docuwiki](https://www.dokuwiki.org/dokuwiki) instance. This was built to inform a restructuring of the [HSBNE Wiki](https://wiki.hsbne.org/) which is running on [docuwiki](https://www.dokuwiki.org/dokuwiki). There is a lot of valuable content in that wiki, so the objective was to restructure the "connecting roads" rather than interfere with the "towns and cities".

There will be some code in there that you'll want to tailor if you want this 

# Updating `wiki.json`

Basically this is just a matter of running...

`python3 http2json`

...but you might need to run...

`pip3 install -r requirements.txt`

...first. This will hit the wiki a bunch of times, and discover links in all of the pages. `wiki.json` (stored in the `static` folder) is just a dictionary with relative page paths for keys, and lists of page paths found in that page as "values".

That python script is pretty ugly in terms of disk I/O because it writes to `wiki.json` every time it learns something new. It only does this because i'm impatient and like to watch the file grow in another window as it's running.

With an up to date `wiki.json` you can do two things. You can convert it into a digraph file with `json2digraph`, and then turn that digraph file into an SVG file with `digraph2svg`. That was my original goal, but when I saw the result I changed my approach, which brings us to the web interface.

# Running the Web Interface

This web interface is written in [Flask](https://flask.palletsprojects.com/en/2.0.x/) (for the back end) and [Vue.js](https://vuejs.org/) for the front end (with a splash of [Bootstrasp](https://getbootstrap.com/) for aesthetics).

With docker installed on your workstation, you should be able to issue a simple...

```
docker-compose up
```

...to get started. With that running you can browse to...

```
http://localhost:5000/
```

...to explore the information collected in `static/wiki.json`.

I found that the menu that appeared on every page was making the digraphs overly complicated, so I listed them in `static/menu.json` so that they could be rendered as yellow buttons in the lists and omitted altogether from the digraphs. Come to think of it, perhaps that would have made the SVG idea less of a failure.
