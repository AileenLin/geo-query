import request from '@/utils/request'
var querystring = require('querystring')

export function getEntities(data) {
  const formData = querystring.stringify({ query: data })
  return request({
    url: 'https://cors-anywhere.herokuapp.com/http://ming-gpu-3.cs.uwaterloo.ca:7001',
    method: 'post',
    headers: {
      'Accept': 'application/sparql-results+json',
      'Content-type': 'application/x-www-form-urlencoded'
    },
    data: formData
  })
}

