import { fileURLToPath, URL } from 'node:url'
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import DefineOptions from 'unplugin-vue-define-options/vite'

// 设置环境变量目录
const envDir = './env'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const ENV = loadEnv(mode, envDir)
  const proxyConf = {
    '/api': {
      target: 'http://127.0.0.1:8080',
      changeOrigin: true,
      rewrite: (path) => path.replace(ENV.VITE_BASE_PATH, '/')
    }
  }

  return {
    base: ENV.VITE_BASE_PATH,
    envDir,
    plugins: [
      vue(),
      DefineOptions(),
    ],
    server: {
      cors: true,
      host: '0.0.0.0',
      port: Number(ENV.VITE_APP_PORT),
      strictPort: true,
      proxy: proxyConf,
    },
    build: {
      outDir: 'dist/ui',
      sourcemap: false,  // 生产环境中禁用 sourcemap
      minify: 'esbuild', // 使用 esbuild 进行代码压缩
      rollupOptions: {
        output: {
          manualChunks(id) {
            if (id.includes('node_modules')) {
              return id.toString().split('node_modules/')[1].split('/')[0].toString();
            }
          }
        }
      }
    },
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
    optimizeDeps: {
      include: ['vue', 'vue-router'],  // 预构建常用依赖
    },
    cacheDir: './node_modules/.vite_cache',  // 设置缓存目录
  }
})
