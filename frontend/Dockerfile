# Use node alpine for small image
FROM node:18-alpine

ENV NPM_CONFIG_OPTIONAL=false

WORKDIR /app

COPY package.json package-lock.json ./
# skip optional deps (like rollup-native) to avoid missing native binaries
RUN npm install --omit=optional
# install missing Rollup native binding so vite build works
RUN npm install @rollup/rollup-linux-x64-musl --no-save

COPY . .

# Build the static assets
RUN npm run build

# Serve them via a simple static server
RUN npm install -g serve

EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]

