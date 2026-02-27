import os
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

class ResumeHandler:
    def __init__(self, upload_dir):
        self.upload_dir = upload_dir
        self.resume_path = os.path.join(upload_dir, "resume.pdf")

    def create_sample_resume(self, name, email, phone, skills, experience):
        """Create a sample resume PDF"""
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        y = 750  # Starting y position
        
        # Header
        can.setFont("Helvetica-Bold", 16)
        can.drawString(50, y, name)
        y -= 20
        
        can.setFont("Helvetica", 12)
        can.drawString(50, y, f"Email: {email}")
        y -= 20
        can.drawString(50, y, f"Phone: {phone}")
        y -= 40
        
        # Skills
        can.setFont("Helvetica-Bold", 14)
        can.drawString(50, y, "Skills")
        y -= 20
        can.setFont("Helvetica", 12)
        for skill in skills:
            can.drawString(70, y, f"• {skill}")
            y -= 20
        y -= 20
        
        # Experience
        can.setFont("Helvetica-Bold", 14)
        can.drawString(50, y, "Experience")
        y -= 20
        can.setFont("Helvetica", 12)
        for exp in experience:
            can.drawString(70, y, f"• {exp}")
            y -= 20
            
        can.save()
        
        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        
        # Create a new PDF with the generated content
        new_pdf = PdfReader(packet)
        output = PdfWriter()
        output.add_page(new_pdf.pages[0])
        
        # Save the PDF
        Path(self.upload_dir).mkdir(parents=True, exist_ok=True)
        with open(self.resume_path, "wb") as output_file:
            output.write(output_file)
            
        return self.resume_path

    def get_resume_path(self):
        """Get the path of the current resume"""
        return self.resume_path if os.path.exists(self.resume_path) else None

# Example usage
if __name__ == "__main__":
    handler = ResumeHandler("uploads")
    sample_resume = handler.create_sample_resume(
        name="John Doe",
        email="john@example.com",
        phone="(555) 123-4567",
        skills=[
            "Python", "JavaScript", "React", "Flask",
            "SQL", "Git", "AWS", "Docker"
        ],
        experience=[
            "Senior Software Engineer at Tech Corp (2020-Present)",
            "Full Stack Developer at Web Solutions (2018-2020)",
            "Junior Developer at StartUp Inc (2016-2018)"
        ]
    )
    print(f"Sample resume created at: {sample_resume}")