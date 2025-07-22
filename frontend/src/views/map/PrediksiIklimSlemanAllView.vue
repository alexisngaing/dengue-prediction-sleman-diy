<template>
  <div class="relative z-0">
    <div id="map4" style="height: 500px; width: 500px"></div>
  </div>
</template>

<script>
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

export default {
  name: 'PrediksiIklimSlemanAll',
  data() {
    return {
      selectedMonth: 'Agustus', // Set Agustus as default
      map: null,
      centerMarker: null,
      monthValues: {
        Agustus: '70',
        September: '50',
        Oktober: '35',
      },
      geoJsonLayer: null,
    }
  },
  mounted() {
    this.initMap()
    this.loadGeoJSON()
  },
  methods: {
    initMap() {
      this.map = L.map('map4').setView([-7.6896, 110.3831], 10.5)

      L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
      }).addTo(this.map)

      this.createDropdownControl()

      // Set initial marker with August value
      this.centerMarker = L.marker([-7.6896, 110.3831], {
        icon: this.createNumberIcon(this.monthValues.Agustus),
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
          select.innerHTML = `
            <option value="">Pilih Bulan</option>
            <option value="Agustus" selected>Agustus 2025</option>
            <option value="September">September 2025</option>
            <option value="Oktober">Oktober 2025</option>
          `

          // Set the selected value to Agustus
          select.value = 'Agustus'

          select.addEventListener('change', e => {
            this.selectedMonth = e.target.value
            this.updateCenterNumber()
            this.updateFillColor()
          })

          return container
        },
      })

      new MonthControl({ position: 'topright' }).addTo(this.map)
    },

    addKeterangan() {
      const Keterangan = L.Control.extend({
        onAdd: () => {
          const container = L.DomUtil.create('div', 'image-control')
          const img = L.DomUtil.create('img', '', container)
          img.src = 'images/keterangan_iklim.png'
          img.style.width = '140px'
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
        if (num < 10)
          bgColor = '#ffffff' // white
        else if (num >= 10 && num < 20)
          bgColor = '#0000ff' // Dark Blue
        else if (num >= 20 && num < 30)
          bgColor = '#007fff' // Light Blue
        else if (num >= 30 && num < 40)
          bgColor = '#00ffff' // Cyan
        else if (num >= 40 && num < 50)
          bgColor = '#7fff7f' // Light Green
        else if (num >= 50 && num < 60)
          bgColor = '#ffff00' // Yellow
        else if (num >= 60 && num < 70)
          bgColor = '#ffc800' // Orange
        else if (num >= 70 && num < 80)
          bgColor = '#ff7f00' // Dark Orange
        else if (num >= 80 && num < 90)
          bgColor = '#ff3f00' // Light Red
        else if (num >= 90) bgColor = '#b40000' // Dark Red
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
        ">${value}%</div>`,
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

      if (value < 10)
        fillColor = '#ffffff' // white
      else if (value >= 10 && value < 20)
        fillColor = '#0000ff' // Dark Blue
      else if (value >= 20 && value < 30)
        fillColor = '#007fff' // Light Blue
      else if (value >= 30 && value < 40)
        fillColor = '#00ffff' // Cyan
      else if (value >= 40 && value < 50)
        fillColor = '#7fff7f' // Light Green
      else if (value >= 50 && value < 60)
        fillColor = '#ffff00' // Yellow
      else if (value >= 60 && value < 70)
        fillColor = '#ffc800' // Orange
      else if (value >= 70 && value < 80)
        fillColor = '#ff7f00' // Dark Orange
      else if (value >= 80 && value < 90)
        fillColor = '#ff3f00' // Light Red
      else if (value >= 90) fillColor = '#b40000' // Dark Red

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
                  Bulan: <b>${this.selectedMonth} 2025</b><br>
                  Probabilitas Kecocokan: <b>${
                    value < 10
                      ? '< 10%'
                      : value < 20
                        ? '10%-20%'
                        : value < 30
                          ? '20%-30%'
                          : value < 40
                            ? '30%-40%'
                            : value < 50
                              ? '40%-50%'
                              : value < 60
                                ? '50%-60%'
                                : value < 70
                                  ? '60%-70%'
                                  : value < 80
                                    ? '70%-80%'
                                    : value < 90
                                      ? '80%-90%'
                                      : '>90%'
                  }</b><br>
                  Tingkat Risiko: <b>${
                    value < 40 ? 'Rendah' : value < 70 ? 'Sedang' : 'Tinggi'
                  }</b>
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
                  if (currentValue < 10) currentColor = '#ffffff'
                  else if (currentValue >= 10 && currentValue < 20)
                    currentColor = '#0000ff'
                  else if (currentValue >= 20 && currentValue < 30)
                    currentColor = '#007fff'
                  else if (currentValue >= 30 && currentValue < 40)
                    currentColor = '#00ffff'
                  else if (currentValue >= 40 && currentValue < 50)
                    currentColor = '#7fff7f'
                  else if (currentValue >= 50 && currentValue < 60)
                    currentColor = '#ffff00'
                  else if (currentValue >= 60 && currentValue < 70)
                    currentColor = '#ffc800'
                  else if (currentValue >= 70 && currentValue < 80)
                    currentColor = '#ff7f00'
                  else if (currentValue >= 80 && currentValue < 90)
                    currentColor = '#ff3f00'
                  else if (currentValue >= 90) currentColor = '#b40000'

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
