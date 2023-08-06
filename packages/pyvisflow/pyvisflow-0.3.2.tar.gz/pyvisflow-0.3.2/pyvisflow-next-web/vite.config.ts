import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import removePlotlyScript from "./src/plugins/removePlotlyScript";

// https://vitejs.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      '~/': `${path.resolve(__dirname, 'src')}/`,
    },
  },
  plugins: [vue(),

  AutoImport({
    resolvers: [ElementPlusResolver()],
  }),
  Components({
    resolvers: [ElementPlusResolver()],
  }),
  removePlotlyScript(),
  ],
  build: {
    // sourcemap: true,
    target: 'esnext',
    assetsInlineLimit: 488280,

    rollupOptions: {
      // external: ['plotly.js-dist'],
      output: {
        // file: '../pyvisflow/template/bundle.js',
        format: 'iife',
        name: 'MyBundle'
      }
    }
  }
})
