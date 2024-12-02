import kagglehub

def download_mental_health_dataset():
    try:
        # Download latest version
        path = kagglehub.dataset_download("thedevastator/uncover-global-trends-in-mental-health-disorder")
        return path
    except Exception as e:
        raise RuntimeError(f"Error downloading mental health dataset: {e}")

def download_crime_dataset():
    try:
        # Download latest version
        path = kagglehub.dataset_download("melissamonfared/crime-trends-and-operations")
        return path
    except Exception as e:
        raise RuntimeError(f"Error downloading crime dataset: {e}")
