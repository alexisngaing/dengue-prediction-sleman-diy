<template>
  <div class="mx-auto max-w-7xl text-center py-10">
    <h1 class="text-3xl font-bold mb-4">
      Peringatan Dini Demam Berdarah Dengue Wilayah Kabupaten Sleman
    </h1>
    <div>
      <h2 class="text-xl font-medium pb-6">
        Prediksi Angka Insiden DBD Bulanan dan Prediksi Risiko DBD Berdasarkan
        Iklim Bulanan
      </h2>
    </div>
    <p class="pb-10">
      Peta prediksi angka insiden menunjukkan perkiraan jumlah kasus DBD yang
      mungkin terjadi. Semakin tinggi angka insiden, semakin tinggi pula risiko
      terjadinya wabah DBD di wilayah tersebut. Peta prediksi risiko DBD
      berdasarkan iklim menunjukkan perkiraan risiko DBD berdasarkan kondisi
      iklim (curah hujan RR, kelembapan RH, suhu rata-rata Tavg). Semakin tinggi
      risiko, semakin besar kemungkinan kondisi iklim mendukung pertumbuhan
      nyamuk Aedes aegypti.
    </p>
    <div class="space-x-4 pb-10">
      <h3 class="pb-2">Hasil kolaborasi dari:</h3>
      <img
        src="/public/images/Lambang_Kabupaten_Sleman.png"
        alt="Dinkes Sleman"
        class="inline-block w-14 h-auto"
      />
      <img
        src="/public/images/Logo_BMKG.png"
        alt="BMKG"
        class="inline-block w-14 h-auto"
      />
      <img
        src="/public/images/uajy.png"
        alt="UAJY"
        class="inline-block w-14 h-auto"
      />
    </div>
    <div class="border border-gray-300 rounded-lg p-6 mb-10">
      <h2 class="text-lg font-bold">Prediksi Angka Insiden</h2>
      <p class="text-sm text-gray-600 pb-4">Update: 30 April 2025</p>
      <div class="flex justify-center space-x-4">
        <div class="text-center">
          <h3 class="pb-2 font-semibold">
            Prediksi Angka Insiden DBD Bulanan Per Kapanewon
          </h3>
          <p class="text-sm text-gray-600 pb-4">(Per 10.000 Penduduk)</p>
          <PrediksiAngkaInsiden />
        </div>
        <div class="">
          <h3 class="pb-2 font-semibold">
            Prediksi Angka Insiden DBD Bulanan: Kabupaten Sleman
          </h3>
          <p class="text-sm text-gray-600 pb-4">(Per 100.000 Penduduk)</p>
          <PrediksiAngkaInsidenSlemanAll />
        </div>
      </div>
    </div>

    <!-- <div class="border border-gray-300 rounded-lg p-6 mb-10">
      <h2 class="text-lg font-bold">
        Prediksi Secara Keseluruhan Kabupaten Sleman
      </h2>
      <p class="text-sm text-gray-600 pb-4">Update: 30 April 2025</p>
      <div class="flex justify-center space-x-4">
        <div class="text-center">
          <h3 class="pb-2 font-semibold">
            Prediksi Risiko DBD Berdasarkan Iklim Bulanan
          </h3>
          <PrediksiIklim />
        </div>
        <div class="">
          <h3 class="pb-2 font-semibold">
            Prediksi Risiko DBD Berdasarkan Iklim Bulanan
          </h3>
          <PrediksiIklimSlemanAll />
        </div>
      </div>
    </div> -->

    <div class="">
      <h2 class="font-bold text-lg pb-4">
        Rekomendasi Tindak Lanjut Berdasarkan Kelas Angka Insiden
      </h2>
      <div class="flex space-x-4 max-w-sm justify-center mx-auto">
        <img src="/public/images/aman.png" alt="aman" />
        <img src="/public/images/waspada.png" alt="waspada" />
        <img src="/public/images/awas.png" alt="awas" />
      </div>
    </div>
  </div>
</template>

<script>
import PrediksiAngkaInsiden from '@/views/map/PrediksiAngkaInsidenView.vue'
import PrediksiIklim from '@/views/map/PrediksiIklimView.vue'
import PrediksiAngkaInsidenSlemanAll from '@/views/map/PrediksiAngkaInsidenSlemanAllView.vue'
import PrediksiIklimSlemanAll from '@/views/map/PrediksiIklimSlemanAllView.vue'
export default {
  components: {
    PrediksiAngkaInsiden,
    PrediksiIklim,
    PrediksiAngkaInsidenSlemanAll,
    PrediksiIklimSlemanAll,
  },
  name: 'DashboardView',
}
</script>
