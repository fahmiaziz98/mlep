# Usage for Development

if you run this app please
uncomment in thr application:

`shell
if __name__ == "__main__":
    uvicorn.run(get_app(), host="localhost", port=80)
`

and run cmd:
`shell
cd app-api
python -m api.application`

You can also go to "http://<your-ip>:80/api/v1/docs" to access the Swagger docs of the API, where you can easily see and test all your endpoints