# Python Standard Library imports
import os
import json
import urllib.request
import re
import http.cookiejar
from datetime import datetime

# Our module imports
from .logging import Logger

# Constants
CONFIG_NAME = "cdoc-config.json"
DEFAULT_SET = "No Set"
ANCHOR_EXTENSION = ".json"
ANCHOR_HOOK = "<&> "
WIKI_API_FILE = "api.php"

# HTTP opener
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))


def create_config(data, override=False):

  # Create config file
  if not override and os.path.isfile(CONFIG_NAME):
    Logger.fatal("configuration file already exists")

  with open(CONFIG_NAME, "w") as output:
    json.dump(data, output, indent=4, separators=(',', ': '), sort_keys=True)


def get_config():
  """Trys to open the config file"""

  # Get the path to the configuration file
  path = find_config_path(os.getcwd())

  if path is None:
    Logger.fatal("not in a CrossDoc project directory")

  with open(path, "r") as file:
    data = json.load(file)

  return data


def find_config_path(base):
  """Recursively find path to the config file if it exists"""

  # Ensure that the given path is a directory
  curr_path = base if os.path.isdir(base) else os.path.dirname(base)

  # Iterate up from the given directory looking for the file
  while True:

    # If we found the config
    curr_check = os.path.join(curr_path, "cdoc-config.json")
    if os.path.isfile(curr_check):
      return curr_check

    # Break when we've hit the root
    if os.path.dirname(curr_path) == curr_path:
      break

    # Pop off a directory
    curr_path = os.path.dirname(curr_path)

  return None


def store_is_remote(store):
  """Determine whether a given store is remote"""

  return store.startswith("http")


def store_is_valid(store):
  """Determine whether a given store is valid"""

  if store_is_remote(store):
    try:
      urllib.request.urlopen(os.path.join(store, WIKI_API_FILE))
      return True
    except urllib.error.HTTPError:
      return False

  return os.path.isdir(store)


def wiki_request(store, **params):
  """Build a network request for a given store"""

  # Default parameter
  params["format"] = "json"

  # Build request
  url = os.path.join(store, WIKI_API_FILE)
  data = urllib.parse.urlencode(params).encode()
  res = opener.open(url, data)

  # Return JSON results
  return json.loads(res.read().decode("utf-8"))


def get_admin_token(store):

  # Get login token
  res_data = wiki_request(store, action="query", meta="tokens", type="login")
  token = res_data["query"]["tokens"]["logintoken"]

  # Login to the account
  # TODO: Fix hard coded bot account
  wiki_request(store, action="login", lgname="Pete@Main",
               lgpassword="7u0e455t0jtcfaalhoh6dubdpjrnmttq",
               lgtoken=token)

  # Get csrf token
  res_data = wiki_request(store, action="query", meta="tokens", type="csrf")
  return res_data["query"]["tokens"]["csrftoken"]


def find_store(store=None, nth_valid=1, raise_errors=False):
  """Find a valid store based on the config file

  Parameters
  ----------
  store : int, optional
    The index of the store to try to fetch

  nth_valid : int, optional
    Which valid store to return with respect to the beginning of the list
    For example, 2 returns the second valid store

  raise_errors : bool, optional
    If True, raises errors rather than handling them

  Raises
  ------
  ValueError: no valid comment stores found
  KeyError: store specified is invalid"""

  config = get_config()

  # Catch no stores
  # TODO: Consider making one here
  if len(config["stores"]) == 0:

    if raise_errors:
      raise ValueError("no valid comment stores found")
    else:
      Logger.fatal("no valid comment stores found")

  # If we were given a specific store to search for
  if store is not None:

    # Ensure that the parameter is an integer
    store = int(store)

    # Find store by index in config list
    if ((store >= 0 and store < len(config["stores"])) and
            store_is_valid(config["stores"][store])):
      return config["stores"][store]
    elif raise_errors:
      raise KeyError("store specified is invalid")
    else:
      Logger.fatal("store specified is invalid")

  # We need to find a valid store via config
  else:

    # Find the nth_valid store
    curr_store = None
    for store in config["stores"]:
      if store_is_valid(store):
        nth_valid -= 1

        if nth_valid == 0:
          curr_store = store
          break

    if curr_store is not None:
      return curr_store
    elif raise_errors:
      raise ValueError("no valid comment stores found")
    else:
      Logger.fatal("no valid comment stores found")


def find_comment(anchor, store=None, raise_errors=False, get_time=False):
  """Find the comment in the specified store or any store"""

  # Remove anchor hook if it exists
  if anchor.startswith(ANCHOR_HOOK):
    anchor = anchor[len(ANCHOR_HOOK):]

  nth_store = 1

  while True:
    if raise_errors:
      curr_store = find_store(store, nth_store, True)

    else:
      try:
        curr_store = find_store(store, nth_store, True)
      except ValueError:
        Logger.fatal("comment anchor not found")

    # Get the matching anchors #

    if not store_is_remote(curr_store):  # If we are looking at a local store

      # Find the matching anchor
      anchors = [os.fsdecode(f) for f in os.listdir(os.fsencode(curr_store))]
      matching_anchors = [f for f in anchors if f.startswith(anchor)]

    else:  # If we are looking at a remote store

      try:
        res_data = wiki_request(curr_store, action="query",
                                list="allpages", apprefix="&")
      except Exception:
        nth_store += 1
        continue

      anchors = res_data["query"]["allpages"]
      matching_anchors = [a for a in anchors
                          if a["title"][1:].startswith(anchor)]

    # If multiple anchors were found
    if len(matching_anchors) > 1:
      Logger.fatal("ambiguous comment anchor, be more specific")

    # If no anchors were found
    if len(matching_anchors) == 0:
      nth_store += 1
      continue

    # Get the anchor's json (or create it if needed) #

    if not store_is_remote(curr_store):  # If we are looking at a local store

      file_path = os.path.join(curr_store, matching_anchors[0])

      # Get json from anchor
      anchor_json = []
      if os.path.isfile(file_path) and os.stat(file_path).st_size != 0:
        with open(file_path) as file:
          time_since = os.path.getmtime(file_path)
          anchor_json = json.load(file)

      if get_time:
        return file_path, anchor_json, time_since

      return file_path, anchor_json

    else:  # If we are looking at a remote store

      pageid = matching_anchors[0]["pageid"]

      try:
        wikitext = wiki_request(curr_store, action="parse", prop="wikitext",
                                pageid=pageid)
        wikitext = wikitext["parse"]["wikitext"]["*"]

        if get_time:
          rev_time = wiki_request(curr_store, action="query", prop="revisions",
                                  pageids=pageid, rvprop="timestamp")
          rev_time = rev_time["query"]["pages"][str(pageid)]["revisions"][0]
          rev_time = datetime.strptime(rev_time["timestamp"],
                                       "%Y-%m-%dT%H:%M:%SZ")
      except Exception:
        nth_store += 1
        continue

      anchor_json = []
      set_id = 1

      # Parse the wikitext into json
      for line in wikitext.split("\n"):

        if line.startswith("=="):
          anchor_json.append({
            "set_id": set_id,
            "set": line.strip("=").strip(),
            "comment": []
          })
          set_id += 1

        elif len(anchor_json):
          anchor_json[-1]["comment"] += [line]

      # Format each comment string (removing \n's that are solo)
      for item in anchor_json:

        # TODO: Consider whether we should consolidate new lines
        item["comment"] = re.sub("(?<!\\n)\\n(?!\\n)", " ",
                                 "\n".join(item["comment"]))

      wiki_tuple = (curr_store, int(pageid))

      if get_time:
        time_since = (rev_time -
                      datetime.utcfromtimestamp(0)).total_seconds() * 1000
        return wiki_tuple, anchor_json, time_since

      return wiki_tuple, anchor_json


def add_anchor_prefix(anchor):
  """Prefix anchor with hook if missing it"""

  if anchor.startswith(ANCHOR_HOOK):
    return anchor
  else:
    return ANCHOR_HOOK + anchor
