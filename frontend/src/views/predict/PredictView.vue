<template>
  <div class="mx-auto max-w-7xl text-center py-10">
    <h1 class="text-3xl font-bold mb-12">
      Prediksi Demam Berdarah Dengue (DBD) Wilayah Kabupaten Sleman
    </h1>

    <!-- Dropdown untuk jenis prediksi -->
    <div class="mb-4">
      <label for="modelType" class="block mb-1 font-semibold"
        >Jenis Prediksi:</label
      >
      <select
        v-model="modelType"
        id="modelType"
        class="border px-3 py-2 rounded"
      >
        <option disabled value="">-- Pilih Jenis Prediksi --</option>
        <option value="sleman">Kabupaten Sleman</option>
        <option value="kapanewon">Per Kapanewon</option>
      </select>
    </div>

    <!-- Input CSV -->
    <input type="file" accept=".csv" @change="handleFileUpload" class="mb-4" />
    <br />
    <button
      :disabled="!csvFile || !modelType"
      @click="submitCsv"
      class="bg-blue-800 text-white font-semibold px-4 py-2 rounded hover:bg-blue-700"
    >
      Prediksi Sekarang
    </button>

    <!-- Hasil Prediksi -->
    <div v-if="predictions.length > 0" class="mt-8 overflow-x-auto">
      <h3 class="text-xl font-semibold mb-2">Hasil Prediksi</h3>
      <table class="min-w-full border-collapse border border-gray-300">
        <thead class="bg-gray-200">
          <tr>
            <!-- Tampilkan kolom sub_district jika model kecamatan -->
            <th v-if="modelType === 'kapanewon'" class="border px-4 py-2">
              Kapanewon
            </th>
            <th class="border px-4 py-2">Tanggal</th>
            <th class="border px-4 py-2">Suhu Minimum (°C)</th>
            <th class="border px-4 py-2">Kelembapan (%)</th>
            <th class="border px-4 py-2">Curah Hujan (mm)</th>
            <th class="border px-4 py-2">Prediksi Kasus</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in predictions" :key="index">
            <td v-if="modelType === 'kapanewon'" class="border px-4 py-2">
              {{ row.sub_district }}
            </td>
            <td class="border px-4 py-2">{{ row.date }}</td>
            <td class="border px-4 py-2">{{ row.temperature_min_celsius }}</td>
            <td class="border px-4 py-2">{{ row.humidity_avg_percentage }}</td>
            <td class="border px-4 py-2">{{ row.precipitation_mm }}</td>
            <td class="border px-4 py-2 font-bold text-red-600">
              {{ Math.round(row.predicted_cases) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PredictView',
  data() {
    return {
      csvFile: null,
      predictions: [],
      modelType: '',
    }
  },
  methods: {
    handleFileUpload(event) {
      this.csvFile = event.target.files[0]
    },
    async submitCsv() {
      if (!this.csvFile || !this.modelType) {
        alert('Mohon pilih jenis prediksi dan unggah file CSV.')
        return
      }

      const formData = new FormData()
      formData.append('file', this.csvFile)

      // Tentukan endpoint berdasarkan jenis model
      let endpoint = ''
      if (this.modelType === 'sleman') {
        endpoint = 'http://localhost:5000/predict/sleman'
      } else if (this.modelType === 'kapanewon') {
        endpoint = 'http://localhost:5000/predict/kapanewon'
      }

      try {
        const response = await axios.post(endpoint, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        console.log('Predictions from backend:', response.data)

        this.predictions = response.data
      } catch (error) {
        console.error('Gagal memproses file:', error)
        alert('Terjadi kesalahan saat memproses file.')
      }
    }

  },
  components: {},
}
</script>
