FROM node:18 AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

FROM node:18-slim

WORKDIR /usr/src/app

COPY --from=build /app/package*.json ./
RUN npm install

COPY --from=build /app /usr/src/app

EXPOSE 3000

CMD ["npm", "run", "start"]
