export default {
  data() {
    return {
      lastScrollTop: 0,
      isShrunk: false
    }
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll)
  },
  beforeDestroy() {
    window.removeEventListener('scroll', this.handleScroll)
  },
  methods: {
    handleScroll() {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop
      this.isShrunk = scrollTop > this.lastScrollTop
      this.lastScrollTop = scrollTop <= 0 ? 0 : scrollTop
    }
  }
}
