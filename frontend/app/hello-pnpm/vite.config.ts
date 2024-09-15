import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // --hostと同義
    host: true,
    // 立ち上げる際のポートを変更できます。
    port: 5173
  }
})
