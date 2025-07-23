<template>
  <div class="relative z-0">
    <div id="map3" style="height: 500px; width: 500px"></div>
  </div>
</template>

<script>
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

export default {
  name: 'PrediksiAngkaInsidenSlemanAll',
  data() {
    return {
      selectedMonth: 'Januari 2025', // Set Agustus as default
      map: null,
      centerMarker: null,
      monthValues: {},
      geoJsonLayer: null,
    }
  },
  mounted() {
    this.fetchPrediction().then(() => {
      this.initMap()
      this.loadGeoJSON()
      // this.createDropdownControl() // Pindahkan ke sini
  })
  },
  methods: {
    async fetchPrediction() {
      try {
        const response = await fetch('http://localhost:5000/all-predictions')
        const data = await response.json()

        this.allPredictions = data

        data.forEach(item => {
          const month = this.formatMonthToIndonesian(item.date)
          this.monthValues[month] = parseFloat(item.incidence_rate).toFixed(2)
        })

        // Pilih bulan terbaru
        const latest = data[data.length - 1]
        this.selectedMonth = this.formatMonthToIndonesian(latest.date)

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
      this.map = L.map('map3').setView([-7.6896, 110.3831], 10.5)

      L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
      }).addTo(this.map)

      this.createDropdownControl()

      this.centerMarker = L.marker([-7.6896, 110.3831], {
        icon: this.createNumberIcon(this.monthValues.Agustus), // Set initial value for Agustus
        zIndexOffset: 1000,
      }).addTo(this.map)

      this.addKeterangan()
    },

    createDropdownControl() {
      const MonthControl = L.Control.extend({
        onAdd: () => {
          const container = L.DomUtil.create('div', 'month-control')
          L.DomEvent.disableClickPropagation(container)

          const select = L.DomUtil.create('select', 'month-select', container)

          let optionsHtml = `<option value="">Pilih Bulan</option>`
         
          const filteredMonths = Object.keys(this.monthValues).filter(m => m.includes('2025'))
          
          for (const month of filteredMonths) {
            const selected = month === this.selectedMonth ? 'selected' : ''
            optionsHtml += `<option value="${month}" ${selected}>${month}</option>`
          }

          select.innerHTML = optionsHtml
          select.value = this.selectedMonth

          select.addEventListener('change', e => {
            this.selectedMonth = e.target.value
            this.updateCenterNumber()
            this.updateFillColor()
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

    createNumberIcon(value) {
      let bgColor = '#ffffff'
      if (value) {
        const num = parseFloat(value)
        if (num < 3) bgColor = '#4CAF50'
        else if (num >= 3 && num < 10) bgColor = '#FFC107'
        else if (num >= 10) bgColor = '#F44336'
      }

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
          color: ${value && parseFloat(value) >= 10 ? 'white' : 'black'};
        ">${value}</div>`,
        className: '',
        iconSize: [40, 40],
      })
    },

    updateCenterNumber() {
      const value = this.monthValues[this.selectedMonth] || ''
      this.centerMarker.setIcon(this.createNumberIcon(value))
    },

    updateFillColor() {
      if (!this.geoJsonLayer || !this.selectedMonth) return

      const value = parseFloat(this.monthValues[this.selectedMonth]) || 0
      let fillColor = '#ff7800'

      if (value < 3) fillColor = '#4CAF50'
      else if (value >= 3 && value < 10) fillColor = '#FFC107'
      else if (value >= 10) fillColor = '#F44336'

      this.geoJsonLayer.setStyle({
        fillColor: fillColor,
        color: this.darkenColor(fillColor),
      })
    },

    darkenColor(color) {
      const factor = 0.7
      const r = parseInt(color.substr(1, 2), 16) * factor
      const g = parseInt(color.substr(3, 2), 16) * factor
      const b = parseInt(color.substr(5, 2), 16) * factor
      return `rgb(${Math.round(r)}, ${Math.round(g)}, ${Math.round(b)})`
    },

    loadGeoJSON() {
      fetch('/sleman_all.geojson')
        .then(response => response.json())
        .then(data => {
          this.geoJsonLayer = L.geoJSON(data, {
            style: {
              color: this.darkenColor('#ff7800'),
              weight: 2,
              opacity: 1,
              fillColor: '#ff7800',
              fillOpacity: 0.5,
            },
            onEachFeature: (feature, layer) => {
              if (feature.properties) {
                const value =
                  parseFloat(this.monthValues[this.selectedMonth]) || 0
                const popupContent = `
                  <b>${feature.properties.name || 'Kabupaten Sleman'}</b><br>
                  Bulan: <b>${this.selectedMonth}</b><br>
                  Angka Insiden: <b>${value}</b><br>
                  Keterangan: <b>${value < 3 ? 'Aman' : value < 10 ? 'Waspada' : 'Awas'}</b>
                `
                layer.bindPopup(popupContent)
              }
              layer.on({
                mouseover: e =>
                  e.target.setStyle({
                    color: '#000000',
                    weight: 3,
                  }),
                mouseout: e => {
                  const currentValue =
                    parseFloat(this.monthValues[this.selectedMonth]) || 0
                  let currentColor = '#ff7800'
                  if (currentValue < 3) currentColor = '#4CAF50'
                  else if (currentValue >= 3 && currentValue < 10)
                    currentColor = '#FFC107'
                  else if (currentValue >= 10) currentColor = '#F44336'

                  e.target.setStyle({
                    color: this.darkenColor(currentColor),
                    weight: 2,
                  })
                },
              })
            },
          }).addTo(this.map)

          // Update the fill color for Agustus after loading
          this.updateFillColor()
        })
        .catch(err => console.error('Error loading GeoJSON:', err))
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
