# Python Binance Data Miner

## Intro

A very simple docker container for mining live binance data into SQL database.

---

## How to use

- edit docker-compose.dev.yml
  - To change the symbol
    - change SYMBOL
  - To add more python job
    - copy container and renamed it

```
$ docker-compose build
$ docker-compose up
```

- To run in Portainer

  - build your own image with

  ```
  $ docker save [your image name] > [your image name].tar
  ```

  - upload exported image to Portainer
  - edit docker-compose.portainer.yml
    - update image name to [your image name]
  - upload to stacks in Portainer

- To connect to SQL server
  ```
  {
      host="Your docker host ip",
      user="root",
      password="password",
      database="crypto"
  }
  ```
