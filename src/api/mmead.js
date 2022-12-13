import request from '@/utils/request'

export function getPIDs(data) {
  // data = 'PREFIX e: <\http://example.com/test#> SELECT ?psid ?ename WHERE { ?entity e:entity_id 965751 . ?entity e:entity ?ename . ?p e:passage ?entity . ?p e:pid ?psid . }'
  return request({
    url: 'https://cors-anywhere.herokuapp.com/http://ming-gpu-4.cs.uwaterloo.ca:7015',
    method: 'post',
    headers: {
      // 'Accept': 'text/tab-separated-values',
      'Accept': 'application/sparql-results+json',
      'Content-type': 'application/sparql-query'
    },
    data
  })
}
