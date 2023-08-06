from openwebpos import open_web_pos

application = open_web_pos()

if __name__ == '__main__':
    try:
        application.run()
    except RecursionError as re:
        print("Unable to start OpenWebPOS. Please check your configuration.")
        print("Error/s:" + str(re))
