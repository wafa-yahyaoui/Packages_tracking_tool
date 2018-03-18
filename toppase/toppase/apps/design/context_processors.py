from toppase.config.settings import My_SERVER_URL_



def global_settings(request):
    # return any necessary values
    return {
        'MY_SERVER_URL': My_SERVER_URL_,
}
