import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import time

# Set page configuration
st.set_page_config(
    page_title="AI Resume Optimizer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Call the CSS file
local_css("style.css")

# Function to simulate job description analysis
def analyze_job_description(job_desc):
    # Simulate processing time
    time.sleep(2)
    
    # Generate mock analysis
    keywords = ["Python", "Machine Learning", "Data Analysis", "AWS", "SQL", "TensorFlow", "Project Management"]
    matched = [kw for kw in keywords if kw.lower() in job_desc.lower()]
    unmatched = [kw for kw in keywords if kw.lower() not in job_desc.lower()]
    
    return {
        "match_percentage": min(100, len(matched) * 15),
        "matched_keywords": matched,
        "missing_keywords": unmatched[:3],
        "suggestions": [
            "Highlight your experience with AWS cloud services in the Skills section",
            "Add a project involving TensorFlow to demonstrate ML expertise",
            "Include specific metrics for your data analysis projects (e.g., 'improved efficiency by 25%')"
        ],
        "tone_analysis": "Technical and results-oriented - matches well with your resume",
        "complexity": "Moderate technical level - good match for your experience"
    }

# Function to simulate resume analysis
def analyze_resume(resume_text, job_desc):
    # Simulate processing time
    time.sleep(3)
    
    # Generate mock analysis
    return {
        "score": 78,
        "strengths": [
            "Strong technical skills section",
            "Clear project descriptions",
            "Good educational background"
        ],
        "weaknesses": [
            "Lack of quantifiable achievements",
            "Limited cloud computing experience",
            "Could use more industry-specific keywords"
        ],
        "optimization_tips": [
            "Add 2-3 more quantifiable achievements in your experience section",
            "Include AWS certification if available",
            "Tailor skills section to match the job description more closely"
        ]
    }

# Function to create a sample resume
def create_sample_resume():
    return """
John Doe
San Francisco, CA | (555) 123-4567 | john.doe@email.com | linkedin.com/in/johndoe

SUMMARY
Data Scientist with 3+ years of experience in machine learning and data analysis. 
Skilled in Python, SQL, and statistical modeling. Seeking to leverage data-driven 
insights to drive business decisions at Tech Innovations Inc.

EXPERIENCE
Data Scientist, ABC Tech | Jan 2021 - Present
- Developed machine learning models to predict customer churn with 85% accuracy
- Created data pipelines to process large datasets using Python and SQL
- Collaborated with cross-functional teams to implement data-driven solutions

Data Analyst Intern, XYZ Corp | Jun 2020 - Dec 2020
- Performed data analysis to identify market trends and customer preferences
- Created interactive dashboards using Tableau for business stakeholders
- Assisted in A/B testing experiments to optimize marketing campaigns

EDUCATION
B.S. in Computer Science
University of California, Berkeley | 2016 - 2020
GPA: 3.7/4.0

SKILLS
- Programming: Python, R, SQL
- Machine Learning: Scikit-learn, TensorFlow
- Data Visualization: Tableau, Matplotlib
- Tools: Git, Docker, AWS

PROJECTS
Customer Segmentation Model
- Developed clustering model to segment customers into 5 distinct groups
- Implemented using Python and scikit-learn
"""

# Initialize session state
if 'job_desc' not in st.session_state:
    st.session_state.job_desc = ""
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = create_sample_resume()
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False

# Main application
def main():
    # Header
    st.title("📄 AI Resume Optimizer")
    st.markdown("### Enhance your resume to match job descriptions perfectly")
    st.write("Upload your resume and paste a job description to get AI-powered optimization suggestions")
    
    # Columns layout
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.subheader("🔍 Job Description Analysis")
        job_desc = st.text_area("Paste job description here:", 
                                height=300,
                                value="We are seeking a skilled Data Scientist with experience in Python, machine learning, and cloud platforms. The ideal candidate will have 3+ years of experience developing predictive models, working with large datasets, and deploying solutions on AWS. Strong communication skills and the ability to work in cross-functional teams are essential. Experience with TensorFlow and SQL is required.",
                                key="job_desc")
        
        if st.button("Analyze Job Description", use_container_width=True):
            with st.spinner("Analyzing job description..."):
                analysis = analyze_job_description(job_desc)
                st.session_state.jd_analysis = analysis
                st.session_state.analysis_done = True
                
                st.success("Analysis complete!")
                st.subheader("Job Description Insights")
                
                # Create metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("Match Potential", f"{analysis['match_percentage']}%", "Good")
                col2.metric("Key Skills", len(analysis['matched_keywords']), "Matched")
                col3.metric("Tone Analysis", analysis['tone_analysis'].split("-")[0].strip())
                
                # Keywords section
                st.subheader("🔑 Key Skills Analysis")
                st.markdown("**Matched Keywords:**")
                st.write(", ".join(analysis['matched_keywords']))
                
                st.markdown("**Skills to Add:**")
                st.write(", ".join(analysis['missing_keywords']))
                
                # Suggestions
                st.subheader("💡 Optimization Suggestions")
                for i, suggestion in enumerate(analysis['suggestions'], 1):
                    st.markdown(f"{i}. {suggestion}")
    
    with col2:
        st.subheader("📄 Resume Content")
        resume_text = st.text_area("Paste your resume here:", 
                                  height=300,
                                  value=st.session_state.resume_text,
                                  key="resume_text")
        
        st.markdown("---")
        st.subheader("🚀 Resume Optimization")
        
        if st.button("Optimize My Resume", use_container_width=True):
            if 'job_desc' not in st.session_state or not st.session_state.job_desc.strip():
                st.warning("Please enter a job description first")
                return
                
            with st.spinner("Analyzing and optimizing your resume..."):
                resume_analysis = analyze_resume(resume_text, st.session_state.job_desc)
                st.session_state.resume_analysis = resume_analysis
                st.session_state.analysis_done = True
                
                st.success("Resume analysis complete!")
                st.subheader("Resume Score")
                
                # Create a gauge chart for resume score
                fig, ax = plt.subplots(figsize=(6, 3))
                ax.axis('off')
                ax.set_xlim(0, 100)
                ax.set_ylim(0, 1)
                
                # Draw gauge
                ax.barh(0.5, resume_analysis['score'], height=0.3, color='#4CAF50')
                ax.barh(0.5, 100 - resume_analysis['score'], left=resume_analysis['score'], height=0.3, color='#f0f0f0')
                ax.text(resume_analysis['score']/2, 0.55, f"{resume_analysis['score']}%", 
                        ha='center', va='center', fontsize=20, color='white')
                ax.text(50, 0.2, "Resume Match Score", ha='center', va='center', fontsize=10)
                
                st.pyplot(fig)
                
                # Strengths and weaknesses
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("✅ Strengths")
                    for strength in resume_analysis['strengths']:
                        st.markdown(f"- {strength}")
                
                with col2:
                    st.subheader("⚠️ Weaknesses")
                    for weakness in resume_analysis['weaknesses']:
                        st.markdown(f"- {weakness}")
                
                # Optimization tips
                st.subheader("💡 Optimization Tips")
                for i, tip in enumerate(resume_analysis['optimization_tips'], 1):
                    st.markdown(f"{i}. {tip}")
                
                # Download optimized resume
                st.markdown("---")
                st.subheader("📥 Download Optimized Resume")
                st.markdown("""
                **Your optimized resume is ready!**
                
                Based on our analysis, we've created an enhanced version of your resume 
                tailored to the job description.
                """)
                
                # Create a mock PDF file for download
                pdf_data = BytesIO()
                pdf_data.write(b"Mock PDF content for optimized resume")
                pdf_data.seek(0)
                
                st.download_button(
                    label="Download Optimized Resume",
                    data=pdf_data,
                    file_name="optimized_resume.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

    # Footer
    st.markdown("---")
    st.markdown("### How It Works")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **1. Analyze Job Description**  
        Our AI scans the job description to identify key skills, 
        qualifications, and keywords.
        """)
    with col2:
        st.markdown("""
        **2. Evaluate Your Resume**  
        We compare your resume against the job requirements to 
        identify gaps and opportunities.
        """)
    with col3:
        st.markdown("""
        **3. Get Tailored Suggestions**  
        Receive specific recommendations to optimize your resume 
        for each application.
        """)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <p>AI Resume Optimizer • Created with Streamlit</p>
        <p>Easily host this application on GitHub Pages</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
