FROM node:18-alpine

WORKDIR /app

COPY package.json .

RUN npm install

RUN npm i -g vite

COPY . .

EXPOSE 3000

CMD [ "npm", "run", "start" ]