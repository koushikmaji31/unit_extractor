from pyngrok import ngrok

public_url = ngrok.connect(8000)
print("Public URL:", public_url)

input("Press Enter to terminate...")
ngrok.disconnect(public_url)
