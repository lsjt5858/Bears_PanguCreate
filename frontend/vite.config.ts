import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  // 基础路径 - 对于根目录部署使用 '/'
  base: '/',
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    // 输出目录
    outDir: 'dist',
    // 生成 sourcemap 便于调试
    sourcemap: false,
    // 资源文件目录
    assetsDir: 'assets',
    // 清空输出目录
    emptyOutDir: true,
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true,
      },
    },
  },
})

