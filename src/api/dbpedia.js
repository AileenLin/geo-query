import request from '@/utils/request'

export function getWikipediaId(data) {
  // data = 'PREFIX wikibase: <http://wikiba.se/ontology#>\n' +
  //     'PREFIX wd: <http://www.wikidata.org/entity/>\n' +
  //     'PREFIX bd: <http://www.bigdata.com/rdf#>\n' +
  //     'PREFIX owl: <http://www.w3.org/2002/07/owl#> \n' +
  //     'PREFIX dbo: <http://dbpedia.org/ontology/> \n' +
  //     'PREFIX wd: <http://www.wikidata.org/entity/> \n' +
  //     'SELECT ?wikipedia_id WHERE {\n' +
  //     '    ?dbpedia_id owl:sameAs ?wikidata_id .\n' +
  //     '    ?dbpedia_id dbo:wikiPageID ?wikipedia_id .\n' +
  //     '    VALUES ?wikidata_id { wd:Q123 wd:Q321 } \n' +
  //     '}'
  const formData = new FormData()
  formData.append('query', data)
  formData.append('format', 'application/sparql-results+json')
  return request({
    url: 'https://dbpedia.org/sparql',
    method: 'post',
    data: formData
  })
}

