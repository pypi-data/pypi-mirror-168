import re, sys, json, sqlite3
import requests
from pathlib import Path

from .tools import defaultify
from . import log

class GQLWrapper:
	port = ""
	url = ""
	headers = {
		"Accept-Encoding": "gzip, deflate",
		"Content-Type": "application/json",
		"Accept": "application/json",
		"Connection": "keep-alive",
		"DNT": "1"
	}
	cookies = {}

	def __init__(self):
		return

	def parse_fragments(self, fragments_in):
		fragments = {}
		fragment_matches = re.finditer(r'fragment ([A-Za-z]+) on [A-Za-z]+ {', fragments_in)
		for fagment_match in fragment_matches:
			start = fagment_match.end()
			end = start

			depth = 0
			for i in range(end, len(fragments_in)):
				c = fragments_in[i]
				if c == "{":
					depth += 1
				if c == "}":
					if depth > 0:
						depth -= 1
					else:
						end = i
						break
			fragments[fagment_match.group(1)] = fragments_in[fagment_match.start():end+1]
		self.fragments.update(fragments)
		return fragments

	def __resolveFragments(self, query):
		fragmentReferences = list(set(re.findall(r'(?<=\.\.\.)\w+', query)))
		fragments = []
		for ref in fragmentReferences:
			fragments.append({
				"fragment": ref,
				"defined": bool(re.search("fragment {}".format(ref), query))
			})

		if all([f["defined"] for f in fragments]):
			return query
		else:
			for fragment in [f["fragment"] for f in fragments if not f["defined"]]:
				if fragment not in self.fragments:
					raise Exception(f'GraphQL error: fragment "{fragment}" not defined')
				query += self.fragments[fragment]
			return self.__resolveFragments(query)

	def _callGraphQL(self, query, variables=None):

		query = self.__resolveFragments(query)

		json_request = {'query': query}
		if variables is not None:
			json_request['variables'] = variables

		response = requests.post(self.url, json=json_request, headers=self.headers, cookies=self.cookies)
		result = response.json()

		for error in result.get("errors", []):
			message = error.get("message")
			code = error.get("extensions", {}).get("code", "GRAPHQL_ERROR")
			path = error.get("path", "")
			fmt_error = f"{code}: {message} {path}".strip()
			log.error(fmt_error)

		if response.status_code == 200:
			result_data = defaultify(result.get("data"))
			return result_data['data']
		elif response.status_code == 401:
			log.error(f"401, Unauthorized. Could not access endpoiont {self.url}. Did you provide an API key?")
		else:
			log.error(f"{response.status_code} query failed. {query}. Variables: {variables}")
		sys.exit()

class SQLiteWrapper:
	conn = None

	def __init__(self, db_filepath) -> None:
		# generate uri for read-only connection, all write operations should be done from the API
		p = Path(db_filepath).resolve()
		db_uri = f"{p.as_uri()}?mode=ro"
		self.conn = sqlite3.connect(db_uri, uri=True)

	def query(self, query, args=(), one=False):
		cur = self.conn.cursor()
		cur.execute(query, args)
		r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
		return (r[0] if r else None) if one else r