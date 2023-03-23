# Dockerfile

FROM node:18-alpine

ARG NODE_ENV
ENV NODE_ENV $NODE_ENV

ARG PUBLIC_API_URL
ENV PUBLIC_API_URL $PUBLIC_API_URL

WORKDIR /app
COPY package.json  ./
RUN npm install 

COPY . .
RUN npm run build

CMD ["node", "build"]

