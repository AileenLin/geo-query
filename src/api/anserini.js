import request from '@/utils/request'

export function fetchDocs(data) {
  return request({
    url: 'https://cors-anywhere.herokuapp.com/http://ming-gpu-3.cs.uwaterloo.ca:9527/doc',
    method: 'post',
    headers: {
      'Content-type': 'application/json'
    },
    data
  })
}
