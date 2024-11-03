FROM node:16-alpine as build

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

# Add this line to see what files are in the build directory
RUN npm run build && ls -la build/

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
# Add this line to verify files are copied
RUN ls -la /usr/share/nginx/html/

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]