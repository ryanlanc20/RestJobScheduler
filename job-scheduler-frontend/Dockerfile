FROM node:latest
COPY . .
WORKDIR /
RUN npm install
RUN npm install serve
RUN npm run build
CMD ["npx","serve","./build"]
EXPOSE 3000