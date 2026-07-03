import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tsconfigPaths from 'vite-tsconfig-paths'
import { TanStackRouterVite } from '@tanstack/router-plugin/vite'
import path from 'path'

export default defineConfig({
  plugins: [
    TanStackRouterVite({
      routesDirectory: './src/routes',
      generatedRouteTree: './src/routeTree.gen.ts',
    }),
    react(),
    tsconfigPaths()
  ],
  base: '/pixel-perfect-grids/',
  build: {
    outDir: path.resolve(__dirname, '../FrontEnd/public/pixel-perfect-grids'),
    emptyOutDir: true,
    chunkSizeWarningLimit: 2000
  }
})
