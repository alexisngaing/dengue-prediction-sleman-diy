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
      selectedMonth: 'Agustus',
      map: null,
      subdistrictLayers: {}, // Stores subdistrict polygon layers
      valueMarkers: {}, // Stores value markers for each subdistrict
      monthValues: {
        Agustus: {
          Gamping: 5.5,
          Godean: 8.2,
          Moyudan: 5.7,
          Minggir: 2.3,
          Seyegan: 3.1,
          Mlati: 4.5,
          Depok: 6.0,
          Berbah: 2.5,
          Prambanan: 1.0,
          Kalasan: 3.0,
          Ngemplak: 4.0,
          Ngaglik: 2.0,
          Sleman: 3.5,
          Tempel: 5.0,
          Turi: 2.0,
          Pakem: 1.5,
          Cangkringan: 3.0,
        },
        September: {
          Gamping: 4.0,
          Godean: 6.8,
          Moyudan: 4.1,
          Minggir: 1.9,
          Seyegan: 2.5,
          Mlati: 3.8,
          Depok: 5.2,
          Berbah: 1.8,
          Prambanan: 6.5,
          Kalasan: 2.0,
          Ngemplak: 3.5,
          Ngaglik: 1.5,
          Sleman: 2.8,
          Tempel: 4.0,
          Turi: 1.0,
          Pakem: 2.0,
          Cangkringan: 1.5,
        },
        Oktober: {
          Gamping: 2.3,
          Godean: 7.5,
          Moyudan: 10.2,
          Minggir: 3.8,
          Seyegan: 1.5,
          Mlati: 2.0,
          Depok: 4.0,
          Berbah: 4.5,
          Prambanan: 2.0,
          Kalasan: 5.0,
          Ngemplak: 6.0,
          Ngaglik: 3.0,
          Sleman: 1.0,
          Tempel: 2.5,
          Turi: 3.5,
          Pakem: 4.0,
          Cangkringan: 5.5,
        },
      },
    }
  },
  mounted() {
    this.initMap()
    this.loadGeoJSON()
  },
  methods: {
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
          select.innerHTML = `
            <option value="">Pilih Bulan</option>
            <option value="Agustus" selected>Agustus 2025</option>
            <option value="September">September 2025</option>
            <option value="Oktober">Oktober 2025</option>
          `

          select.addEventListener('change', e => {
            this.selectedMonth = e.target.value
            this.updateSubdistrictValues()
          })

          select.value = 'Agustus' // Set default value

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
        iconAnchor: [20, 20], // Center the icon
      })
    },

    updateSubdistrictValues() {
      if (!this.selectedMonth) return

      Object.keys(this.subdistrictLayers).forEach(name => {
        const value = this.monthValues[this.selectedMonth]?.[name] || 0

        // Update polygon color
        const color = this.getColorForValue(value)
        this.subdistrictLayers[name].setStyle({
          fillColor: color,
          color: this.darkenColor(color),
          fillOpacity: 0.7,
        })

        // Update or create value marker
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

        // Update popup content
        const popupContent = `
          <b>${name}</b><br>
          Bulan: <b>${this.selectedMonth} 2025</b><br>
          Angka Insiden: <b>${value}</b><br>
          Keterangan: <b>${value < 3 ? 'Aman' : value < 10 ? 'Waspada' : 'Awas'}</b>
        `
        this.subdistrictLayers[name].bindPopup(popupContent)
      })
    },

    getSubdistrictCenter(layer) {
      // Get the center point of the subdistrict polygon
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
      // Subdistricts data - update URLs to match your GeoJSON files
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

      // Load each subdistrict GeoJSON
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

            // Store layer reference
            this.subdistrictLayers[subdistrict.name] = layer

            // Add hover effects
            layer.on({
              mouseover: e => {
                e.target.setStyle({ weight: 3 })
                if (this.valueMarkers[subdistrict.name]) {
                  this.valueMarkers[subdistrict.name].bringToFront()
                }
              },
              mouseout: e => {
                const currentValue =
                  this.monthValues[this.selectedMonth]?.[subdistrict.name] || 0
                const color = this.getColorForValue(currentValue)
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
        // After all layers are loaded, update values for the default month
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
