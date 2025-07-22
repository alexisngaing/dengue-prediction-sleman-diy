<script setup>
import { RouterView } from 'vue-router'
import Navbar from '@/views/layouts/AppNavbar.vue'
import Footer from '@/views/layouts/AppFooter.vue'
</script>

<template>
  <Navbar />
  <RouterView />
  <Footer />
</template>

<style scoped></style>
