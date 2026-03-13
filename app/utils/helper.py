import os
from django.utils.text import get_valid_filename
import datetime
from datetime import datetime as dt_datetime, date as dt_date, time as dt_time

class Helper:
    def __init__(self):
        # Path: root uploads/ directory
        self.upload_path = 'uploads'
        self.allowed_extensions = {'png', 'jpg', 'jpeg'}
        
        # Ensure the directory exists
        if not os.path.exists(self.upload_path):
            os.makedirs(self.upload_path)

    def is_allowed_file(self, filename):
        """Checks if the file extension is allowed."""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def upload_image(self, image):
        """Saves image with its original (but secured) name."""
        filename = getattr(image, 'filename', getattr(image, 'name', None))
        if image and filename and self.is_allowed_file(filename):
            # get_valid_filename removes spaces and dangerous characters
            filename = get_valid_filename(filename)
            
            full_path = os.path.join(self.upload_path, filename)
            
            if hasattr(image, 'save') and not hasattr(image, 'chunks'):
                image.save(full_path)
            else:
                with open(full_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
            
            return filename
        return None

    def update_image(self, new_image, old_filename):
        """Deletes the old file and uploads the new one."""
        # Only proceed if the new image is valid
        new_filename = getattr(new_image, 'filename', getattr(new_image, 'name', None))
        if new_image and new_filename and self.is_allowed_file(new_filename):
            # 1. Remove the old file from the folder if it exists
            if old_filename:
                old_file_path = os.path.join(self.upload_path, old_filename)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
            
            # 2. Upload the new image
            return self.upload_image(new_image)
        
        return None
    def format_to_date(self, date_str):
        """
        Converts string to a date object for models.DateField()
        Input: '2026-03-12' -> Output: date(2026, 3, 12)
        """
        if not date_str:
            return None
        if isinstance(date_str, dt_date):
            return date_str
        try:
            # Standard HTML5 date input format: YYYY-MM-DD
            return dt_datetime.strptime(str(date_str), '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return None

    def format_to_time(self, time_str):
        """
        Converts string to a time object for models.TimeField()
        Input: '14:30' -> Output: time(14, 30)
        """
        if not time_str:
            return None
        if isinstance(time_str, dt_time):
            return time_str
        try:
            # Standard HTML5 time input format: HH:MM
            return dt_datetime.strptime(str(time_str), '%H:%M').time()
        except (ValueError, TypeError):
            return None    
