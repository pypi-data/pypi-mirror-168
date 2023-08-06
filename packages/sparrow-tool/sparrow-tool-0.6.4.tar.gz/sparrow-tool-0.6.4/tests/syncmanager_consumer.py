if __name__ == "__main":
    from sparrow.multiprocess.client import Client
    client = Client()
    print(client.get_data())
