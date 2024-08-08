from google_images_search import GoogleImagesSearch
from credentials import developers_api_key, project_cx

gis = GoogleImagesSearch(developers_api_key, project_cx)


search_params = {
    'q': 'puppies',  
    'num': 10,  
    'fileType': 'jpg',  
    'imgSize': 'large',  
    'safe': 'high'  
}


gis.search(search_params=search_params)

for image in gis.results():
    image.download('C:/Users/nimit/Download_google_images/Downloaded_files') 



