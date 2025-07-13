# streamlit_app.py
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

# Custom CSS styling
st.markdown("""
<style>
/* Main container styling */
.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%);
    background-attachment: fixed;
    padding: 2rem;
}

/* Header styling */
h1 {
    color: #2c3e50;
    border-bottom: 2px solid #3498db;
    padding-bottom: 10px;
}

/* Button styling */
.stButton>button {
    background: linear-gradient(135deg, #3498db 0%, #2c3e50 100%);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 10px 24px;
    font-weight: bold;
    transition: all 0.3s ease;
    margin-top: 15px;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

/* Text area styling */
.stTextArea textarea {
    border-radius: 10px;
    border: 1px solid #ddd;
    padding: 15px;
    box-shadow: inset 0 1px 2px rgba(0,0,0,0.1);
    min-height: 300px;
}

/* Metric styling */
.stMetric {
    background-color: white;
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    text-align: center;
}

/* Card styling */
.stMarkdown {
    background-color: white;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

/* Column gap */
[data-testid="column"] {
    background-color: transparent;
    padding: 10px;
}

/* Divider styling */
hr {
    border-top: 1px solid #ddd;
    margin: 30px 0;
}

/* Footer styling */
footer {
    text-align: center;
    padding: 20px;
    color: #7f8c8d;
    font-size: 0.9rem;
}

/* Progress bar */
.stProgress > div > div > div {
    background-color: #3498db;
}
</style>
""", unsafe_allow_html=True)

# Function to simulate job description analysis
def analyze_job_description(job_desc):
    # Simulate processing time
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.02)
        progress_bar.progress(percent_complete + 1)
    time.sleep(0.5)
    
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
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.03)
        progress_bar.progress(percent_complete + 1)
    time.sleep(0.5)
    
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
                col3.metric("Tone Match", analysis['tone_analysis'].split("-")[0].strip())
                
                # Keywords section
                st.subheader("🔑 Key Skills Analysis")
                st.markdown("**Matched Keywords:**")
                st.write(", ".join(analysis['matched_keywords']) or "None")
                
                st.markdown("**Skills to Add:**")
                st.write(", ".join(analysis['missing_keywords']) or "None")
                
                # Suggestions
                st.subheader("💡 Optimization Suggestions")
                for i, suggestion in enumerate(analysis['suggestions'], 1):
                    st.markdown(f"{i}. {suggestion}")
    
    with col2:
        st.subheader("📄 Resume Content")
        resume_text = st.text_area("Paste your resume here:", 
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
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.set_facecolor('#f0f2f6')
                fig.patch.set_facecolor('#f0f2f6')
                ax.set_xlim(0, 100)
                ax.set_ylim(0, 1)
                
                # Draw gauge
                score = resume_analysis['score']
                ax.barh(0.5, score, height=0.3, color='#4CAF50')
                ax.barh(0.5, 100-score, left=score, height=0.3, color='#e0e0e0')
                ax.text(score/2, 0.55, f"{score}%", 
                        ha='center', va='center', fontsize=24, color='white', fontweight='bold')
                ax.text(50, 0.2, "Resume Match Score", 
                        ha='center', va='center', fontsize=12, color='#2c3e50')
                ax.axis('off')
                
                st.pyplot(fig, use_container_width=True)
                
                # Strengths and weaknesses
                col1, col2 = st.columns(2)
                
                with col1:
                    with st.expander("✅ Strengths", expanded=True):
                        for strength in resume_analysis['strengths']:
                            st.markdown(f"- {strength}")
                
                with col2:
                    with st.expander("⚠️ Weaknesses", expanded=True):
                        for weakness in resume_analysis['weaknesses']:
                            st.markdown(f"- {weakness}")
                
                # Optimization tips
                with st.expander("💡 Optimization Tips", expanded=True):
                    for i, tip in enumerate(resume_analysis['optimization_tips'], 1):
                        st.markdown(f"{i}. {tip}")
                
                # Download optimized resume
                st.markdown("---")
                st.subheader("📥 Download Optimized Resume")
                
                # Create a mock PDF file for download
                pdf_data = BytesIO()
                pdf_data.write(resume_text.encode())
                pdf_data.seek(0)
                
                st.download_button(
                    label="Download Optimized Resume (PDF)",
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
        <div style="background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h4>1. Analyze Job Description</h4>
            <p>Our AI scans the job description to identify key skills, qualifications, and keywords.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h4>2. Evaluate Your Resume</h4>
            <p>We compare your resume against the job requirements to identify gaps and opportunities.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h4>3. Get Tailored Suggestions</h4>
            <p>Receive specific recommendations to optimize your resume for each application.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px; color: #7f8c8d;">
        <p>AI Resume Optimizer • Created with Streamlit • Hosted on GitHub</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
