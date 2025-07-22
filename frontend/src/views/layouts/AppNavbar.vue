<template>
  <header
    class="flex flex-wrap sm:justify-start sm:flex-nowrap w-full text-sm py-12"
  >
    <nav
      class="bg-white fixed w-full z-20 top-0 start-0 border-b border-black-600 shadow-lg transition-all duration-300 ease-in-out px-4"
      :class="isShrunk ? 'h-16 py-1' : 'h-24 py-5'"
    >
      <div
        class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto"
      >
        <router-link
          to="/"
          class="flex items-center space-x-3 rtl:space-x-reverse"
        >
          <img src="/images/logo.png" class="max-h-14" alt="Logo Sistem" />
        </router-link>
        <div class="flex md:order-1 space-x-3 md:space-x-3 rtl:space-x-reverse">
          <!-- <h1>Oleh: Alexis Divasonda Sigat Ngaing</h1> -->
          <router-link to="/predict" class="font-semibold"
            ><h1>Prediksi</h1></router-link
          >
        </div>
      </div>
    </nav>
  </header>
</template>

<script>
import NavbarScroll from '@/scripts/NavbarScroll'

export default {
  name: 'AppNavbar',
  mixins: [NavbarScroll],
  data() {
    return {
      showMenu: false,
      showUserDropdown: false,
    }
  },
  methods: {
    toggleNavbar: function () {
      this.showMenu = !this.showMenu
    },
    toggleUserDropdown: function () {
      this.showUserDropdown = !this.showUserDropdown
    },
  },
}
</script>
