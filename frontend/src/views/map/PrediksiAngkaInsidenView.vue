<template>
  <div class="relative z-0">
    <div id="map1" style="height: 500px; width: 500px"></div>
  </div>
</template>

<script>
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

export default {
  name: 'PrediksiAngkaInsiden',
  data() {
    return {
      // selectedMonth: 'Januari 2025',
      map: null,
      subdistrictLayers: {},
      valueMarkers: {},
      monthValues: {},
    }
  },
  mounted() {
    this.fetchPrediction().then(() => {
      this.initMap()
      this.loadGeoJSON()
  })
  },
  methods: {
    async fetchPrediction() {
      try {
        const response = await fetch('http://localhost:5000/predictions/kapanewon')
        const data = await response.json()

        this.allPredictions = data
        this.monthValues = {}

        data.forEach(item => {
          const monthLabel = this.formatMonthToIndonesian(item.date)

          if (
            item.sub_district &&
            typeof item.sub_district === 'string' &&
            monthLabel &&
            item.incidence_rate != null
          ) {
            const key = `${item.sub_district.toLowerCase()}_${monthLabel}`
            this.monthValues[key] = parseFloat(item.incidence_rate).toFixed(2)
          } else {
            console.warn('Data prediksi tidak lengkap atau rusak:', item)
          }
        })

        // Default
        this.selectedMonth = 'Agustus 2025'

      } catch (err) {
        console.log('monthValues:', this.monthValues)
        console.error('Gagal mengambil prediksi:', err)
      }
    },

    formatMonthToIndonesian(dateStr) {
      const bulanIndo = [
        'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
        'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
      ]
      const date = new Date(dateStr)
      return `${bulanIndo[date.getMonth()]} ${date.getFullYear()}`
    },

    initMap() {
      this.map = L.map('map1').setView([-7.6896, 110.3831], 10.5)

      L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
      }).addTo(this.map)

      this.createDropdownControl()
      this.addKeterangan()
    },

    createDropdownControl() {
      const MonthControl = L.Control.extend({
        onAdd: () => {
          const container = L.DomUtil.create('div', 'month-control')
          L.DomEvent.disableClickPropagation(container)

          const select = L.DomUtil.create('select', 'month-select', container)

          let optionsHtml = `<option value="">Pilih Bulan</option>`
          const filteredMonths = [...new Set(
            Object.keys(this.monthValues)
              .map(key => key.split('_')[1])
              .filter(m => m.includes('2025'))
          )]

          for (const month of filteredMonths) {
            const selected = month === this.selectedMonth ? 'selected' : ''
            optionsHtml += `<option value="${month}" ${selected}>${month}</option>`
          }

          select.innerHTML = optionsHtml
          select.value = this.selectedMonth

          select.addEventListener('change', e => {
            this.selectedMonth = e.target.value
            this.updateSubdistrictValues()
          })

          return container
        }
      })

      new MonthControl({ position: 'topright' }).addTo(this.map)
    },

    addKeterangan() {
      const Keterangan = L.Control.extend({
        onAdd: () => {
          const container = L.DomUtil.create('div', 'image-control')
          const img = L.DomUtil.create('img', '', container)
          img.src = 'images/keterangan.png'
          img.style.width = '200px'
          img.style.height = 'auto'
          img.style.borderRadius = '4px'
          return container
        },
      })

      new Keterangan({ position: 'bottomright' }).addTo(this.map)
    },

    createValueIcon(value) {
      const num = parseFloat(value) || 0
      let bgColor = '#ffffff'

      if (num < 3)
        bgColor = '#4CAF50' // Green
      else if (num < 10)
        bgColor = '#FFC107' // Yellow
      else bgColor = '#F44336' // Red

      return L.divIcon({
        html: `<div style="
          background: ${bgColor};
          border-radius: 50%;
          width: 40px;
          height: 40px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: bold;
          border: 2px solid #ff7800;
          font-size: 14px;
          box-shadow: 0 0 10px rgba(0,0,0,0.2);
          color: ${num >= 10 ? 'white' : 'black'};
        ">${value}</div>`,
        className: '',
        iconSize: [40, 40],
        iconAnchor: [20, 20],
      })
    },

    updateSubdistrictValues() {
      if (!this.selectedMonth) return

      Object.keys(this.subdistrictLayers).forEach(name => {
        const key = `${name.toLowerCase()}_${this.selectedMonth}`
        const value = parseFloat(this.monthValues[key]) || 0

        console.log('Updating:', key, 'Value:', value)

        const color = this.getColorForValue(value)
        this.subdistrictLayers[name].setStyle({
          fillColor: color,
          color: this.darkenColor(color),
          fillOpacity: 0.7,
        })

        if (this.valueMarkers[name]) {
          this.valueMarkers[name]
            .setIcon(this.createValueIcon(value))
            .setLatLng(this.getSubdistrictCenter(this.subdistrictLayers[name]))
        } else {
          this.valueMarkers[name] = L.marker(
            this.getSubdistrictCenter(this.subdistrictLayers[name]),
            {
              icon: this.createValueIcon(value),
              zIndexOffset: 1000,
            },
          ).addTo(this.map)
        }

        const popupContent = `
          <b>${name}</b><br>
          Bulan: <b>${this.selectedMonth}</b><br>
          Angka Insiden: <b>${value}</b><br>
          Keterangan: <b>${value < 3 ? 'Aman' : value < 10 ? 'Waspada' : 'Awas'}</b>
        `
        this.subdistrictLayers[name].bindPopup(popupContent)
      })
    },

    getSubdistrictCenter(layer) {
      const bounds = layer.getBounds()
      return bounds.getCenter()
    },

    getColorForValue(value) {
      if (value < 3)
        return '#4CAF50' // Green
      else if (value >= 3 && value < 10)
        return '#FFC107' // Yellow
      else if (value >= 10) return '#F44336' // Red
    },

    darkenColor(color) {
      const factor = 0.7
      const r = parseInt(color.substr(1, 2), 16) * factor
      const g = parseInt(color.substr(3, 2), 16) * factor
      const b = parseInt(color.substr(5, 2), 16) * factor
      return `rgb(${Math.round(r)}, ${Math.round(g)}, ${Math.round(b)})`
    },

    loadGeoJSON() {
      const subdistricts = [
        { name: 'Gamping', url: '/gamping.geojson' },
        { name: 'Godean', url: '/godean.geojson' },
        { name: 'Moyudan', url: '/moyudan.geojson' },
        { name: 'Minggir', url: '/minggir.geojson' },
        { name: 'Seyegan', url: '/seyegan.geojson' },
        { name: 'Mlati', url: '/mlati.geojson' },
        { name: 'Depok', url: '/depok.geojson' },
        { name: 'Berbah', url: '/berbah.geojson' },
        { name: 'Prambanan', url: '/prambanan.geojson' },
        { name: 'Kalasan', url: '/kalasan.geojson' },
        { name: 'Ngemplak', url: '/ngemplak.geojson' },
        { name: 'Ngaglik', url: '/ngaglik.geojson' },
        { name: 'Sleman', url: '/sleman.geojson' },
        { name: 'Tempel', url: '/tempel.geojson' },
        { name: 'Turi', url: '/turi.geojson' },
        { name: 'Pakem', url: '/pakem.geojson' },
        { name: 'Cangkringan', url: '/cangkringan.geojson' },
      ]

      const promises = subdistricts.map(subdistrict => {
        return fetch(subdistrict.url)
          .then(response => response.json())
          .then(data => {
            const layer = L.geoJSON(data, {
              style: {
                fillColor: '#ff7800',
                color: this.darkenColor('#ff7800'),
                weight: 2,
                opacity: 1,
                fillOpacity: 0.5,
              },
            }).addTo(this.map)

            this.subdistrictLayers[subdistrict.name] = layer

            layer.on({
              mouseover: e => {
                e.target.setStyle({ weight: 3 })
                if (this.valueMarkers[subdistrict.name]) {
                  this.valueMarkers[subdistrict.name].bringToFront()
                }
              },
              mouseout: e => {
                const key = `${subdistrict.name.toLowerCase()}_${this.selectedMonth}`
                const value = parseFloat(this.monthValues[key]) || 0
                const color = this.getColorForValue(value)

                e.target.setStyle({
                  color: this.darkenColor(color),
                  weight: 2,
                })
              },
            })
          })
          .catch(err =>
            console.error(`Error loading ${subdistrict.name} GeoJSON:`, err),
          )
      })

      Promise.all(promises).then(() => {
        this.updateSubdistrictValues()
      })
    },
  },
}
</script>

<style>
.month-control {
  background: white;
  padding: 5px;
  border-radius: 4px;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.4);
}

.month-select {
  padding: 5px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 3px;
  outline: none;
}

.image-control {
  background: rgba(255, 255, 255, 0.5);
  padding: 5px;
  border-radius: 4px;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.4);
}

.image-control img {
  display: block;
  max-width: 100%;
  height: auto;
}

.leaflet-interactive {
  transition: all 0.3s ease;
}
</style>
