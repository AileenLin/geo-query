
<template>
  <div>
    <sticky :z-index="10" class-name="sub-navbar">
      <div style="font-family:Amatic SC; pointer-events:none; position:absolute; top: 0;left:10px; height:10vh; padding:0px; fontSize:50px; color:#fff; align-items:center">
        Geo Passage
      </div>
    </sticky>
    <el-dialog
      title="Passages"
      style="font-family:Amatic SC; fontSize:20px;fontWeight:bold"
      width="550px"
      :visible.sync="dialogTableVisible"
      :append-to-body="true"
    >
      <el-table v-loading="listLoading" :data="gridData" height="300">
        <el-table-column type="expand">
          <template v-slot="scope">
            <span> {{cached_doc[scope.row.pid]}}</span>
          </template>
        </el-table-column>
        <el-table-column type="index" label="ID" width="60" />
        <el-table-column property="pid" label="Passage ID" width="200" />
        <el-table-column property="entity" label="Entity" width="200" />
      </el-table>
    </el-dialog>
<!--    <div id="globeViz" @wheel="handleWheel" />-->
    <canvas id="canvas" width="1000px" height="1000px" />

<!--    <div id="globeViz" @mousedown="handleMouseDown" @mouseup="handleMouseUp" @mousemove="handleMouseMove" >-->
<!--    </div>    -->
    <div id="globeViz" @mousedown="handleMouseDown" @mouseup="handleMouseUp" @mousemove="handleMouseMove" >
    </div>
    <github-corner class="github-corner" />
  </div>

</template>

<script>
// https://codesandbox.io/s/glob-gl-vue-3-6ypsrr?file=/src/components/datasets/test.js:0-433

import { onMounted } from 'vue'
import Globe from 'globe.gl'
import * as d3 from 'd3'
import GithubCorner from '@/components/GithubCorner'
import Sticky from '@/components/Sticky'
import { getEntities } from '@/api/wikidata'
import { getPIDs } from '@/api/mmead'
import { getWikipediaId } from '@/api/dbpedia'
import { fetchDocs } from '@/api/anserini'
const world = Globe()

const weightColor = d3.scaleSequentialSqrt(d3.interpolateYlOrRd).domain([0, 1e4])

const colorScale = d3.scaleSequentialSqrt(d3.interpolateYlOrRd)

export default {
  components: {
    GithubCorner,
    Sticky
  },
  data() {
    return {
      listLoading: false,
      mouse: {
        current: {
          x: 0,
          y: 0
        },
        previous: {
          x: 0,
          y: 0
        },
        down: false
      },
      rect: {
        startX: 0,
        startY: 0,
        w: 0,
        h: 0
      },
      geobox: {
        point1: {
          lat: 0,
          lng: 0
        },
        point2: {
          lat: 0,
          lng: 0
        }
      },
      drawFlag: false,
      loaded: false,
      selectedValue: '',
      dialogTableVisible: false,
      gridData: [],
      cached_doc: {},
      detailVisible: false
    }
  },
  computed: {
  },
  setup() {
    onMounted(() => {
      const getVal = feat => feat.properties.GDP_MD_EST / Math.max(1e5, feat.properties.POP_EST)
      // const getVal = feat => feat.properties.POP_EST
      fetch('/geo-query/countries.geojson').then(res => res.json()).then(countries => {
        const maxVal = Math.max(...countries.features.map(getVal))
        colorScale.domain([0, maxVal])

        world.globeImageUrl('//unpkg.com/three-globe/example/img/earth-night.jpg')
          .bumpImageUrl('//unpkg.com/three-globe/example/img/earth-topology.png')
          .backgroundImageUrl('//unpkg.com/three-globe/example/img/night-sky.png')
          .lineHoverPrecision(0)
          .polygonsData(countries.features.filter(d => d.properties.ISO_A2 !== 'AQ'))
          .polygonAltitude(0.06)
          .polygonCapColor(feat => colorScale(getVal(feat)))
          .polygonSideColor(() => 'rgba(0, 100, 0, 0.15)')
          .polygonStrokeColor(() => '#111')
          .polygonLabel(({ properties: d }) => `
            <b>${d.ADMIN} (${d.ISO_A2}):</b> <br />
            GDP: <i>${d.GDP_MD_EST}</i> M$<br/>
            Population: <i>${d.POP_EST}</i>
          `)
          .onPolygonHover(hoverD => world
            .polygonAltitude(d => d === hoverD ? 0.12 : 0.06)
            .polygonCapColor(d => d === hoverD ? 'rgba(70, 130, 180,0.5)' : colorScale(getVal(d)))
          )
          .polygonsTransitionDuration(300)
          .hexBinPointWeight('pop')
          .hexAltitude(d => d.sumWeight * 6e-4)
          .hexBinResolution(4)
          .hexTopColor(d => weightColor(d.sumWeight))
          .hexSideColor(d => weightColor(d.sumWeight))
          .hexBinMerge(true)(document.getElementById('globeViz'))
        world.controls().autoRotate = true
        world.controls().autoRotateSpeed = 0.6
        world.controls().mouseButtons.LEFT = -1
        world.controls().mouseButtons.RIGHT = 0
        // world.controls().enableRotate = false
      })
    })
  },
  async created() {
    window.addEventListener('resize', (event) => {
      world.width([event.target.innerWidth])
      world.height([event.target.innerHeight])
    })
    this.ready()
  },
  destroyed() {
    window.removeEventListener('resize', (event) => {
      world.width([event.target.innerWidth])
      world.height([event.target.innerHeight])
    })
  },
  // async mounted() {
  //   // world.onPolygonClick((d, event, { lat, lng, altitude }) => this.polygonClick(d, event, lat, lng, altitude))
  //   // world.onGlobeClick(({ lat, lng }, event) => this.globeClick(lat, lng, event))
  //   world.controls().mouseButtons.LEFT = -1
  //   world.controls().mouseButtons.RIGHT = 0
  //   this.$forceUpdate()
  // },
  methods: {
    computePoint() {
      let maxlat; let minlat; let maxlng; let minlng = 0
      if (this.geobox.point1.lat > this.geobox.point2.lat) {
        maxlat = this.geobox.point1.lat
        minlat = this.geobox.point2.lat
      } else {
        maxlat = this.geobox.point2.lat
        minlat = this.geobox.point1.lat
      }
      if (this.geobox.point1.lng > this.geobox.point2.lng) {
        maxlng = this.geobox.point1.lng
        minlng = this.geobox.point2.lng
      } else {
        maxlng = this.geobox.point2.lng
        minlng = this.geobox.point1.lng
      }
      return {
        'lat': {
          'max': maxlat,
          'min': minlat
        },
        'lng': {
          'max': maxlng,
          'min': minlng
        }
      }
    },
    makeWikidata() {
      const points = this.computePoint()
      const rqt = 'PREFIX wdt: <http://www.wikidata.org/prop/direct/> ' +
      'PREFIX wikibase: <http://wikiba.se/ontology#> ' +
      'PREFIX wd: <http://www.wikidata.org/entity/> ' +
      'PREFIX p: <http://www.wikidata.org/prop/> ' +
      'PREFIX ps: <http://www.wikidata.org/prop/statement/> ' +
      'PREFIX psv: <http://www.wikidata.org/prop/statement/value/> ' +
      'SELECT ?item ?lon ?lat WHERE { ' +
      '  values ?prop { psv:P625 psv:1332 psv:1334 psv:1333 psv:1335 } ' +
      '  ?item ?prop ?coordinate_node . ' +
      '  ?coordinate_node wikibase:geoLongitude ?lon. ' +
      '  ?coordinate_node wikibase:geoLatitude ?lat.  ' +
      '    FILTER ( ?lon >' + points.lng.min + ' && ?lon < ' + points.lng.max + ' && ?lat > ' + points.lat.min + ' && ?lat < ' + points.lat.max + ') ' +
      '} LIMIT 100'
      return rqt
    },
    makeDBpedia(d) {
      const rst = 'PREFIX wikibase: <http://wikiba.se/ontology#>\n' +
          'PREFIX wd: <http://www.wikidata.org/entity/>\n' +
          'PREFIX bd: <http://www.bigdata.com/rdf#>\n' +
          'PREFIX owl: <http://www.w3.org/2002/07/owl#> \n' +
          'PREFIX dbo: <http://dbpedia.org/ontology/> \n' +
          'PREFIX wd: <http://www.wikidata.org/entity/> \n' +
          'SELECT DISTINCT ?wikipedia_id WHERE {\n' +
          '    VALUES ?wikidata_id { ' + d + ' } ' +
          '    ?dbpedia_id owl:sameAs ?wikidata_id .\n' +
          '    ?dbpedia_id dbo:wikiPageID ?wikipedia_id .\n' +
          '}'
      return rst
    },
    makeMmead(d) {
      const rst = 'PREFIX e: <http://example.com/test#>\n' +
          'SELECT ?psid ?ename WHERE { \n' +
          'VALUES ?ids { ' + d + ' } ' +
          '?entity e:entity_id ?ids . ?entity e:entity ?ename . ?p e:passage ?entity . ?p e:pid ?psid . } LIMIT 100'
      return rst
    },
    getIdFromURL(url) {
      return 'wd:' + url.split('/').pop().split('-')[0]
    },
    draw(event) {
      if (this.mouse.down) {
        this.drawFlag = true
        var c = document.getElementById('canvas')
        var ctx = c.getContext('2d')
        world.controls().autoRotate = false
        // ctx.drawImage(this.img, 0, 0) // ctx.clearRect(0,0,800,800);
        ctx.clearRect(0, 0, c.width, c.height)
        ctx.setLineDash([6])
        ctx.strokeStyle = '#00688B'
        ctx.strokeRect(this.rect.startX, this.rect.startY, this.rect.w, this.rect.h)
      }
    },
    clearRec() {
      var c = document.getElementById('canvas')
      var ctx = c.getContext('2d')
      ctx.clearRect(0, 0, c.width, c.height)
    },
    handleMouseDown(event) {
      if (event.button === 0) {
        const point = world.toGlobeCoords(event.offsetX, event.offsetY)
        if (point !== null) {
          const { lat, lng } = point
          this.mouse.down = true
          this.mouse.current = {
            // x: event.pageX,
            // y: event.pageY
            x: event.offsetX,
            y: event.offsetY
          }
          this.geobox.point1.lat = lat
          this.geobox.point1.lng = lng
          this.rect.startX = this.mouse.current.x
          this.rect.startY = this.mouse.current.y
        }
      }
    },
    handleMouseUp(event) {
      const point = world.toGlobeCoords(event.offsetX, event.offsetY)
      if (point !== null) {
        const { lat, lng } = point
        this.geobox.point2.lat = lat
        this.geobox.point2.lng = lng
        this.mouse.down = false
        if (!this.drawFlag) {
          this.clearRec()
          world.controls().autoRotate = true
        } else {
          this.dialogTableVisible = true
          this.listLoading = true
          this.cached_doc = {}
          this.gridData = []
          getEntities(this.makeWikidata()).then(resData => {
            if (resData.data) {
              if (resData.data.results.bindings) {
                const wikidata_ids = resData.data.results.bindings.map(d => {
                  return this.getIdFromURL(d.item.value)
                })
                if (wikidata_ids) {
                  const wikidata_ids_str = wikidata_ids.join(' ')
                  getWikipediaId(this.makeDBpedia(wikidata_ids_str)).then(resData2 => {
                    if (resData2.data) {
                      if (resData2.data.results.bindings) {
                        const wikipedia_ids = resData2.data.results.bindings.map(d => {
                          return d.wikipedia_id.value
                        })
                        if (wikipedia_ids && wikipedia_ids.length > 0) {
                          const wikipedia_ids_str = wikipedia_ids.join(' ')
                          getPIDs(this.makeMmead(wikipedia_ids_str)).then(resData3 => {
                            if (resData3.data) {
                              if (resData3.data.results.bindings) {
                                this.gridData = resData3.data.results.bindings.map(d => {
                                  return { 'pid': d.psid.value, 'entity': d.ename.value }
                                })
                                const doc_ids = resData3.data.results.bindings.map(d => {
                                  return d.psid.value
                                })
                                if (doc_ids && doc_ids.length > 0) {
                                  fetchDocs({ 'ids': doc_ids }).then(resData4 => {
                                    this.listLoading = false
                                    this.cached_doc = resData4.data.result
                                  })
                                } else {
                                  this.listLoading = false
                                }
                              } else {
                                this.listLoading = false
                              }
                            } else {
                              this.listLoading = false
                            }
                          })
                        } else {
                          this.listLoading = false
                        }
                      } else {
                        this.listLoading = false
                      }
                    } else {
                      this.listLoading = false
                    }
                  })
                } else {
                  this.listLoading = false
                }
              } else {
                this.listLoading = false
              }
            } else {
              this.listLoading = false
            }
          })
        }
      } else {
        this.clearRec()
        world.controls().autoRotate = true
      }
      this.drawFlag = false
      this.mouse.down = false
    },
    handleMouseMove(event) {
      this.mouse.current = {
        // x: event.pageX,
        // y: event.pageY
        x: event.offsetX,
        y: event.offsetY
      }
      if (this.mouse.down) {
        const point = world.toGlobeCoords(event.offsetX, event.offsetY)
        if (point !== null) {
          this.rect.w = this.mouse.current.x - this.rect.startX
          this.rect.h = this.mouse.current.y - this.rect.startY
          // ctx.clearRect(0,0,canvas.width,canvas.height);
          this.draw(event)
        } else {
          this.clearRec()
        }
      }
    },
    ready() {
      var c = document.getElementById('canvas')
      var ctx = c.getContext('2d')
      ctx.translate(0.5, 0.5)
      ctx.imageSmoothingEnabled = false
      // var img = document.getElementById("imageRef");
      // ctx.drawImage(img);
      c.width = window.innerWidth
      c.height = window.innerHeight
      ctx.clearRect(0, 0, c.width, c.height)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

@import url("https://fonts.googleapis.com/css?family=Amatic+SC:wght@700&display=swap");
.github-corner {
  position: absolute;
  top: 50px;
  border: 0;
  right: 0;
}
.components-container div {
  margin: 10px;
}

.time-container {
  display: inline-block;
}

.chart-wrapper {
  background: #fff;
  padding: 16px 16px 0;
  margin-bottom: 32px;
}

.el-option {
  overflow-y: auto;
  max-height: 300px;
  width: 200px;
}
.el-table {
  overflow-y: scroll;
  max-height: 300px;
}

.el-select {
  background: transparent;
}

.clear-bk {
  background: transparent;
}

.chart-container{
  position: relative;
  width: 100%;
  height: calc(100vh - 100px);
}
#canvas{
  position: absolute;
  pointer-events:none;
  z-index: 999;
}
</style>
