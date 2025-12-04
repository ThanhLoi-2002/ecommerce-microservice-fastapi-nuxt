// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  components: [
    {
      path: '~/components',
      pathPrefix: false,
    },
  ],
  modules: ['@nuxtjs/tailwindcss', '@pinia/nuxt', '@vueuse/nuxt',],

  pinia: {
    storesDirs: ['./app/stores/**']
  },

  runtimeConfig: {

    //private: is accessible only on the server
    // API_URL: process.env.JWT_TOKEN_KEY,
    // REFRESH_TOKEN_KEY: process.env.REFRESH_TOKEN_KEY,
    // DATABASE_URL: process.env.DATABASE_URL,
    public: {
      // public:is accessible on server and client
      API_URL: process.env.API_URL
    },

  },
})