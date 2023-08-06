import sys


def get_environment_type():
    if 'google.colab' in sys.modules:
        from google.colab import drive
        drive.mount('drive')
        return 'colab'
    elif 'kaggle_secrets' in sys.modules:
        return 'kaggle'
    return 'local'


