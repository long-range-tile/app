FROM alpine:latest as build-frontend
WORKDIR /build
RUN apk add nodejs yarn
ADD package.json yarn.lock ./
RUN yarn install --frozen-lockfile
ADD src ./src
ADD public ./public
RUN yarn run build

FROM alpine:latest
WORKDIR /app
RUN apk add python3-dev py3-pip gcc musl-dev g++
ADD api/requirements.txt ./
RUN pip install -r requirements.txt
ADD api ./
COPY --from=build-frontend /build/build ./static
EXPOSE 5000
CMD ["/usr/bin/python3", "./app.py"]
