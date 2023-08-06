from johnnycanencrypt.johnnycanencrypt import Johnny

with open("files/store/kushal_updated_key.asc", "rb") as f:
    data = f.read()

j = Johnny(data)

res = j.verify_file("msg.txt.asc".encode("utf-8"))
print(res)
