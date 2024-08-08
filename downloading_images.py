import tkinter as tk
from tkinter import ttk, messagebox
from google_images_search import GoogleImagesSearch
from credentials import developers_api_key, project_cx
import os


gis = GoogleImagesSearch(developers_api_key, project_cx)

def download_images():
    query = search_query.get()
    num_images = int(num_images_var.get())
    file_type = file_type_var.get()
    img_size = img_size_var.get()
    safe_search = safe_search_var.get()

    download_path = os.path.join('C:/Users/nimit/Download_google_images', query)
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    search_params = {
        'q': query,
        'num': num_images,
        'fileType': file_type,
        'imgSize': img_size,
        'safe': safe_search
    }

    try:
        gis.search(search_params=search_params)
        for image in gis.results():
            image.download(download_path) 
        messagebox.showinfo("Success", f"{num_images} images downloaded successfully to {download_path}!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("Google Image Downloader")


ttk.Label(root, text="Search Query:").grid(row=0, column=0, padx=10, pady=5)
search_query = ttk.Entry(root, width=30)
search_query.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(root, text="Number of Images:").grid(row=1, column=0, padx=10, pady=5)
num_images_var = tk.StringVar(value="10")
num_images_entry = ttk.Entry(root, textvariable=num_images_var, width=10)
num_images_entry.grid(row=1, column=1, padx=10, pady=5)


ttk.Label(root, text="File Type:").grid(row=2, column=0, padx=10, pady=5)
file_type_var = tk.StringVar()
file_type_dropdown = ttk.Combobox(root, textvariable=file_type_var, values=["jpg", "png", "gif"], width=10)
file_type_dropdown.grid(row=2, column=1, padx=10, pady=5)
file_type_dropdown.current(0) 


ttk.Label(root, text="Image Size:").grid(row=3, column=0, padx=10, pady=5)
img_size_var = tk.StringVar()
img_size_dropdown = ttk.Combobox(root, textvariable=img_size_var, values=["large", "medium", "icon"], width=10)
img_size_dropdown.grid(row=3, column=1, padx=10, pady=5)
img_size_dropdown.current(0)  


ttk.Label(root, text="Safe Search:").grid(row=4, column=0, padx=10, pady=5)
safe_search_var = tk.StringVar()
safe_search_dropdown = ttk.Combobox(root, textvariable=safe_search_var, values=["high", "medium", "off"], width=10)
safe_search_dropdown.grid(row=4, column=1, padx=10, pady=5)
safe_search_dropdown.current(0)  


download_button = ttk.Button(root, text="Download Images", command=download_images)
download_button.grid(row=5, column=0, columnspan=2, padx=10, pady=20)


root.mainloop()



