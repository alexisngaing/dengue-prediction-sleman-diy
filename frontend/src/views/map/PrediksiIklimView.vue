<template>
  <div class="relative z-0">
    <div id="map2" style="height: 500px; width: 500px"></div>
  </div>
</template>

<script>
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

export default {
  name: 'PrediksiIklim',
  data() {
    return {
      selectedMonth: 'Agustus',
      map: null,
      subdistrictLayers: {},
      valueMarkers: {},
      monthValues: {
        Agustus: {
          Gamping: 90,
          Godean: 20,
          Moyudan: 15,
          Minggir: 5,
          Seyegan: 3,
          Mlati: 8,
          Depok: 12,
          Berbah: 2,
          Prambanan: 43,
          Kalasan: 35,
          Ngemplak: 69,
          Ngaglik: 12,
          Sleman: 91,
          Tempel: 55,
          Turi: 25,
          Pakem: 75,
          Cangkringan: 30,
        },
        September: {
          Gamping: 90,
          Godean: 45,
          Moyudan: 12,
          Minggir: 6,
          Seyegan: 4,
          Mlati: 10,
          Depok: 15,
          Berbah: 3,
          Prambanan: 50,
          Kalasan: 40,
          Ngemplak: 70,
          Ngaglik: 15,
          Sleman: 95,
          Tempel: 60,
          Turi: 30,
          Pakem: 80,
          Cangkringan: 35,
        },
        Oktober: {
          Gamping: 95,
          Godean: 50,
          Moyudan: 20,
          Minggir: 10,
          Seyegan: 5,
          Mlati: 15,
          Depok: 20,
          Berbah: 4,
          Prambanan: 55,
          Kalasan: 45,
          Ngemplak: 75,
          Ngaglik: 20,
          Sleman: 100,
          Tempel: 65,
          Turi: 35,
          Pakem: 85,
          Cangkringan: 40,
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
      this.map = L.map('map2').setView([-7.6896, 110.3831], 10.5)

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

          select.value = 'Agustus'

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

    createValueIcon(value) {
      const num = parseFloat(value) || 0
      let bgColor = '#ffffff'

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
        ">${value}%</div>`,
        className: '',
        iconSize: [40, 40],
        iconAnchor: [20, 20],
      })
    },

    updateSubdistrictValues() {
      if (!this.selectedMonth) return

      Object.keys(this.subdistrictLayers).forEach(name => {
        const value = this.monthValues[this.selectedMonth]?.[name] || 0

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
          Bulan: <b>${this.selectedMonth} 2025</b><br>
          Probabilitas Kecocokan: <b>${value < 10 ? '< 10%' : value < 20 ? '10%-20%' : value < 30 ? '20%-30%' : value < 40 ? '30%-40%' : value < 50 ? '40%-50%' : value < 60 ? '50%-60%' : value < 70 ? '60%-70%' : value < 80 ? '70%-80%' : value < 90 ? '80%-90%' : '>90%'}</b><br>
          Tingkat Risiko: <b>${value < 40 ? 'Rendah' : value < 70 ? 'Sedang' : 'Tinggi'}</b>
        `
        this.subdistrictLayers[name].bindPopup(popupContent)
      })
    },

    getSubdistrictCenter(layer) {
      const bounds = layer.getBounds()
      return bounds.getCenter()
    },

    getColorForValue(value) {
      if (value < 10)
        return '#ffffff' // white
      else if (value >= 10 && value < 20)
        return '#0000ff' // Dark Blue
      else if (value >= 20 && value < 30)
        return '#007fff' // Light Blue
      else if (value >= 30 && value < 40)
        return '#00ffff' // Cyan
      else if (value >= 40 && value < 50)
        return '#7fff7f' // Light Green
      else if (value >= 50 && value < 60)
        return '#ffff00' // Yellow
      else if (value >= 60 && value < 70)
        return '#ffc800' // Orange
      else if (value >= 70 && value < 80)
        return '#ff7f00' // Dark Orange
      else if (value >= 80 && value < 90)
        return '#ff3f00' // Light Red
      else if (value >= 90) return '#b40000' // Dark Red
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
