import kagglehub


def download_mental_health_dataset() -> str:
    # Download latest version
    path = kagglehub.dataset_download("thedevastator/uncover-global-trends-in-mental-health-disorder")

    return path

def download_crime_dataset() -> str:
    # Download latest version
    path = kagglehub.dataset_download("melissamonfared/crime-trends-and-operations")

    return path