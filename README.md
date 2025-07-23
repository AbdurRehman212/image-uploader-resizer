# Image Uploader & Resizer (Flask + AWS + Docker)

A Flask-based web application that allows users to upload images, resize them, and store the resized images in AWS S3. The app provides an easy-to-use frontend to upload and resize images with different scale percentages and supports direct downloads from S3.

This application is deployed on **AWS EC2**, is **Dockerized**, and utilizes **AWS S3** for storage.

## 🚀 Features

- Upload and resize images (supports `.png`, `.jpg`, `.jpeg`, `.gif` formats)
- Resize images to user-defined percentages (100%, 75%, 50%)
- Store resized images in an **AWS S3 bucket**
- Directly download resized images via a link
- Dockerized deployment for easy setup

## 🌍 Technologies Used

- **Backend**: Flask (Python)
- **Image Processing**: Pillow
- **Cloud Storage**: AWS S3 (using `boto3` library)
- **Deployment**: Docker
- **Frontend**: HTML, CSS, JavaScript
- **Version Control**: Git, GitHub

## 📦 Installation

### 1. Clone the Repository

Clone this repository to your local machine or EC2 instance:

```bash
git clone https://github.com/AbdurRehman212/image-uploader-resizer.git
cd image-uploader-resizer
