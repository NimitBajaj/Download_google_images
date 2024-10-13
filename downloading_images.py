from google_images_search import GoogleImagesSearch
from credentials import project_cx, developers_api_key, email, password
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from io import BytesIO
import zipfile


gis = GoogleImagesSearch(developers_api_key, project_cx)

class GoogleImageEmailer:
    def __init__(self, root):
        self.root = root
        self.root.title("Google Images to Email")
        self.root.geometry("600x400")
        self.root.config(bg="#ffffff")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Google Images to Email", font=("Helvetica", 16, "bold"), bg="#ffffff").pack(pady=20)

        tk.Label(self.root, text="Search Query:", bg="#ffffff").pack(pady=5)
        self.search_query = tk.Entry(self.root, width=40, borderwidth=2)
        self.search_query.pack(pady=5)

        tk.Label(self.root, text="Number of Images:", bg="#ffffff").pack(pady=5)
        self.num_images_var = tk.StringVar(value="10")
        self.num_images_entry = tk.Entry(self.root, textvariable=self.num_images_var, width=10, borderwidth=2)
        self.num_images_entry.pack(pady=5)

        tk.Label(self.root, text="Your Email Address:", bg="#ffffff").pack(pady=5)
        self.email_entry = tk.Entry(self.root, width=40, borderwidth=2)
        self.email_entry.pack(pady=5)

        self.send_button = tk.Button(self.root, text="Send via Email", command=self.download_images, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), borderwidth=2)
        self.send_button.pack(pady=20)

        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=10)

    def send_email_with_zip(self, email_address, zip_data):
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        sender_email = email
        sender_password = password

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email_address
        msg['Subject'] = 'Downloaded Images'

        msg.attach(MIMEText('Here are the images you requested in a ZIP file.', 'plain'))

        part = MIMEApplication(zip_data.getvalue(), Name='images.zip')
        part['Content-Disposition'] = 'attachment; filename="images.zip"'
        msg.attach(part)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

    def download_images(self):
        query = self.search_query.get()
        num_images = int(self.num_images_var.get())
        email_address = self.email_entry.get()

        search_params = {
            'q': query,
            'num': num_images,
            'fileType': 'jpg',
            'imgSize': 'medium',
            'safe': 'high'
        }

        try:
            gis.search(search_params=search_params)
            self.progress_bar["maximum"] = num_images

            # Create a ZIP file in memory
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for i, image in enumerate(gis.results(), start=1):
                    img_data = BytesIO()
                    try:
                        image.download(img_data)
                        img_name = f"{query}_{i}.jpg"
                        img_data.seek(0)  
                        zip_file.writestr(img_name, img_data.read())  
                    except Exception as e:
                        print(f"Error downloading image {i}: {e}")
                        continue

                    
                    self.progress_bar["value"] = i
                    self.root.update_idletasks()

            zip_buffer.seek(0)  

            self.send_email_with_zip(email_address, zip_buffer)
            messagebox.showinfo("Success", f"{num_images} images sent successfully to {email_address}!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = GoogleImageEmailer(root)
    root.mainloop()



