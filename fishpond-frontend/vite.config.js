import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      // 将/api开头的请求代理到目标服务器
      '/api': {
        target: 'http://127.0.0.1:10086',
        changeOrigin: true, // 改变请求头中的host和origin
        secure: false, // 接受自签名证书
        // rewrite: (path) => path.replace(/^\/api/, '/api') // 如果后端API也是以/api开头，可以不需要重写
      }
    }
  }
})
