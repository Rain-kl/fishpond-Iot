import {defineConfig, loadEnv} from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
    // 加载环境变量
    const env = loadEnv(mode, process.cwd(), '')
    
    // 获取环境变量中的 AI 服务地址，默认为本地开发环境地址
    const aiServiceUrl = env.AI_SERVICE_URL || 'http://127.0.0.1:10099'
    
    console.log('AI Service URL:', aiServiceUrl)
    
    return {
        plugins: [vue()],
        resolve: {
            alias: {
                '@': path.resolve(__dirname, './src')
            }
        },
        server: {
            proxy: {
                // 将/api开头的请求代理到目标服务器
                '/api': {
                    target: 'http://127.0.0.1:10086',
                    changeOrigin: true, // 改变请求头中的host和origin
                    secure: false, // 接受自签名证书
                    // rewrite: (path) => path.replace(/^\/api/, '/api') // 如果后端API也是以/api开头，可以不需要重写
                },
                // 将/ai开头的请求代理到手势识别服务器
                '/ai': {
                    target: aiServiceUrl,
                    changeOrigin: true,
                    secure: false
                }
            }
        },
        // 定义客户端可以使用的环境变量
        define: {
            'import.meta.env.AI_SERVICE_URL': JSON.stringify(aiServiceUrl)
        }
    }
})
